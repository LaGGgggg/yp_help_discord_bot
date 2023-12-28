from typing import Type, Callable

from discord import ui, Interaction, TextStyle
from tortoise.transactions import atomic

from models import QuestionThemeLesson, QuestionProject, QuestionAnother, QuestionBase, get_user_model_by_discord_id


class QuestionBaseModal(ui.Modal):

    context = ui.TextInput(
        label='Описание проблемы', placeholder='опишите вашу проблему', min_length=10, style=TextStyle.long, row=4
    )

    def __init__(self, init_new_forum_channel_thread: Callable):

        self.init_new_forum_channel_thread = init_new_forum_channel_thread

        super().__init__()

    @atomic()
    async def process_question_creation(self, interaction: Interaction, question_model: Type[QuestionBase], **kwargs):

        user = await get_user_model_by_discord_id(interaction.user.id)

        question = await question_model.create(creator=user, **kwargs)

        thread = await self.init_new_forum_channel_thread(question.get_thread_name(), question.get_thread_description())

        question.discord_channel_id = thread.id

        await question.save(update_fields=('discord_channel_id',))

        await interaction.response.send_message(
            f'Ваш вопрос успешно создан, ссылка на тему: {thread.jump_url}\n'
            'Вы можете отсылать сообщения в тему анонимно через бота'
        )


class QuestionThemeLessonModal(QuestionBaseModal, title='Вопрос по теме и уроку'):

    theme = ui.TextInput(label='Тема', placeholder='введите номер темы числом', min_length=1, max_length=3,
                         style=TextStyle.short)
    lesson = ui.TextInput(label='Урок', placeholder='введите номер урока числом', min_length=1, max_length=3,
                          style=TextStyle.short)

    async def on_submit(self, interaction: Interaction) -> None:

        theme = self.theme.value
        lesson = self.lesson.value

        if theme.isnumeric() and lesson.isnumeric():
            await self.process_question_creation(
                interaction, QuestionThemeLesson, theme=theme, lesson=lesson, context=self.context.value
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

    async def on_submit(self, interaction: Interaction) -> None:

        await self.process_question_creation(
            interaction, QuestionProject, project_name=self.project_name, context=self.context.value
        )

        await super().on_submit(interaction)


class QuestionAnotherModal(QuestionBaseModal, title='Вопрос по "другому"'):
    async def on_submit(self, interaction: Interaction) -> None:

        await self.process_question_creation(interaction, QuestionAnother, context=self.context.value)

        await super().on_submit(interaction)
