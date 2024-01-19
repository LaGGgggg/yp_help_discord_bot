from typing import Type, Callable, Any

from discord import ui, Interaction, TextStyle, ForumChannel, Thread, Embed, ButtonStyle
from discord.ext.commands import Bot
from tortoise.transactions import atomic
from tortoise.exceptions import DoesNotExist
from thefuzz.fuzz import partial_ratio

from models import (
    QuestionThemeLesson,
    QuestionProject,
    QuestionAnother,
    QuestionBase,
    QuestionStatistics,
)
from models_utils import get_user_model_by_discord_id
from settings import Settings


class QuestionBaseModal(ui.Modal):

    context = ui.TextInput(
        label='Описание проблемы', placeholder='опишите вашу проблему', min_length=10, style=TextStyle.long, row=4
    )

    def __init__(self, bot: Bot, bot_settings: Settings):

        self.bot = bot
        self.bot_settings = bot_settings

        super().__init__()

    async def init_new_forum_channel_thread(self, name: str, content: str) -> Thread:

        help_forum_channel: ForumChannel = self.bot.get_channel(self.bot_settings.HELP_FORUM_CHANNEL_ID)

        thread = await help_forum_channel.create_thread(name=name, content=content)

        return thread.thread

    @atomic()
    async def process_question_creation(self, interaction: Interaction, question_model: Type[QuestionBase], **kwargs):

        user = await get_user_model_by_discord_id(interaction.user.id)

        # uniqueness check
        try:

            await question_model.get(**kwargs)

            await interaction.response.send_message('Не удалось создать вопрос, такой же уже существует')

            return

        except DoesNotExist:
            pass

        question = await question_model.create(creator=user, **kwargs)

        thread = await self.init_new_forum_channel_thread(question.get_thread_name(), question.get_thread_description())

        question.discord_channel_id = thread.id

        await question.save(update_fields=('discord_channel_id',))

        await QuestionStatistics.create(discord_channel_id=question.discord_channel_id)

        await interaction.response.send_message(
            f'Ваш вопрос успешно создан, ссылка на тему: {thread.jump_url}\n'
            'Вы можете отсылать сообщения в тему анонимно через бота'
        )

    async def process_user_question(
            self,
            interaction: Interaction,
            question_model: Type[QuestionBase],
            get_questions_function: Callable,
            get_questions_kwargs: dict[str, Any],
            create_question_kwargs: dict[str, Any],
            is_completed: bool = True,
    ) -> None:
        """
        Processes the user's question in the format:
        show all similar completed questions (retrieved from get_questions_function) ->
        show all similar unfinished questions -> create a new question.
        (if there are no completed/incomplete questions, skip this part)
        get_questions_function (async) must take a boolean argument (is_completed) that indicates whether the questions
        are complete and kwargs.
        """

        questions = await get_questions_function(is_completed=is_completed, **get_questions_kwargs)

        if questions:

            message = f"Вот список похожих {'' if is_completed else 'не'}решённых вопросов:\n"

            for question in questions:

                question_channel = self.bot.get_channel(question.discord_channel_id)

                message += f'[{question.get_thread_name()}]({question_channel.jump_url})\n'

                question_statistics = await QuestionStatistics.get(discord_channel_id=question.discord_channel_id)

                question_statistics.requests += 1

                await question_statistics.save()

            message_comment_template = 'Если вы не нашли ответ на свой вопрос, то можете '

            if is_completed:
                message += message_comment_template + 'посмотреть похожие, ещё не решённые вопросы'

            else:
                message += message_comment_template + 'создать новый вопрос'

        else:
            message = 'Не удалось найти похожие вопросы, вы можете создать новый'

        embed_message = Embed(description=message)

        next_button_view = ui.View()

        if is_completed and not questions:

            await self.process_user_question(
                interaction,
                question_model,
                get_questions_function,
                get_questions_kwargs,
                create_question_kwargs,
                is_completed=False,
            )

            return

        elif is_completed:

            next_button_view.add_item(ui.Button(label='Посмотреть нерешённые вопросы', style=ButtonStyle.primary))

            async def view_incomplete_questions_callback(callback_interaction: Interaction) -> None:
                await self.process_user_question(
                    callback_interaction,
                    question_model,
                    get_questions_function,
                    get_questions_kwargs,
                    create_question_kwargs,
                    is_completed=False,
                )

            next_button_view.children[0].callback = view_incomplete_questions_callback

        else:

            next_button_view.add_item(ui.Button(label='Создать новый вопрос', style=ButtonStyle.primary))

            async def create_question_callback(callback_interaction: Interaction) -> None:
                await self.process_question_creation(callback_interaction, question_model, **create_question_kwargs)

            next_button_view.children[0].callback = create_question_callback

        await interaction.response.send_message(embed=embed_message, view=next_button_view)


class QuestionThemeLessonModal(QuestionBaseModal, title='Вопрос по теме и уроку'):

    theme = ui.TextInput(
        label='Тема', placeholder='введите номер темы числом', min_length=1, max_length=3, style=TextStyle.short
    )
    lesson = ui.TextInput(
        label='Урок', placeholder='введите номер урока числом', min_length=1, max_length=3, style=TextStyle.short
    )

    @staticmethod
    async def get_questions(is_completed: bool, theme: str, lesson: str) -> list[QuestionThemeLesson]:
        return await QuestionThemeLesson.filter(is_completed=is_completed, theme=theme, lesson=lesson)

    async def on_submit(self, interaction: Interaction) -> None:

        theme = self.theme.value
        lesson = self.lesson.value

        if theme.isnumeric() and lesson.isnumeric():

            search_question_kwargs = {
                'theme': theme,
                'lesson': lesson,
            }

            await self.process_user_question(
                interaction,
                QuestionThemeLesson,
                self.get_questions,
                search_question_kwargs,
                {'context': self.context.value, **search_question_kwargs},
            )

        else:
            await interaction.response.send_message('Тема и урок должны быть числовыми значениями')

        await super().on_submit(interaction)


class QuestionProjectModal(QuestionBaseModal, title='Вопрос по проекту'):

    project_name = ui.TextInput(
        label='Название проекта',
        placeholder='введите название проекта (например: "бот-визитка")',
        min_length=5,
        max_length=127,
        style=TextStyle.short,
    )

    @staticmethod
    async def get_questions(is_completed: bool, project_name: str) -> list[QuestionProject]:

        result = []

        async for question in QuestionProject.filter(is_completed=is_completed):

            question_ratio = partial_ratio(project_name, question.project_name)

            if question_ratio >= 70:
                result.append((question, question_ratio))

        # example: [[999, -32], [23, 99], [0, 0], [1, 23]] -> [23, 1, 0, 999]
        return [i[0] for i in sorted(result, key=lambda x: x[1], reverse=True)]

    async def on_submit(self, interaction: Interaction) -> None:

        search_question_kwargs = {'project_name': self.project_name.value}

        await self.process_user_question(
            interaction,
            QuestionProject,
            self.get_questions,
            search_question_kwargs,
            {'context': self.context.value, **search_question_kwargs},
        )

        await super().on_submit(interaction)


class QuestionAnotherModal(QuestionBaseModal, title='Вопрос по "другому"'):

    @staticmethod
    async def get_questions(is_completed: bool, context: str) -> list[QuestionAnother]:

        result = []

        async for question in QuestionAnother.filter(is_completed=is_completed):

            question_ratio = partial_ratio(context, question.context)

            if question_ratio >= 60:
                result.append((question, question_ratio))

        # example: [[999, -32], [23, 99], [0, 0], [1, 23]] -> [23, 1, 0, 999]
        return [i[0] for i in sorted(result, key=lambda x: x[1], reverse=True)]

    async def on_submit(self, interaction: Interaction) -> None:

        question_kwargs = {'context': self.context.value}

        await self.process_user_question(
            interaction, QuestionAnother, self.get_questions, question_kwargs, question_kwargs
        )

        await super().on_submit(interaction)


class SendAnonymousMessageModal(ui.Modal, title='Отправить анонимное сообщение'):

    message = ui.TextInput(
        label='Текст сообщения', placeholder='введите ваше сообщение', min_length=5, style=TextStyle.long
    )

    def __init__(self, bot: Bot, bot_settings: Settings, target_thread: Thread):

        self.bot = bot
        self.bot_settings = bot_settings
        self.target_thread = target_thread

        super().__init__()

    async def on_submit(self, interaction: Interaction) -> None:

        sent_message = await self.target_thread.send(f'Автор вопроса написал:\n{self.message.value}')

        await interaction.response.send_message(f'[Сообщение]({sent_message.jump_url}) успешно отправлено')

        await super().on_submit(interaction)
