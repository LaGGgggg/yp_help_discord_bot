from discord import ui, SelectOption, Interaction, Thread
from discord.ext.commands import Bot

from modals import QuestionThemeLessonModal, QuestionProjectModal, QuestionAnotherModal, SendAnonymousMessageModal
from settings import Settings
from models import (
    get_all_questions, get_user_model_by_discord_id, QuestionThemeLesson, QuestionProject, QuestionAnother
)


class QuestionThemeMenuView(ui.View):

    def __init__(self, bot: Bot, bot_settings: Settings):

        self.bot = bot
        self.bot_settings = bot_settings

        super().__init__()

    @ui.select(
        cls=ui.Select,
        placeholder='Выберите тип вопроса',
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label='Тема и урок',
                description='Вопрос, касающийся определённой темы и урока',
                value='theme_lesson',
            ),
            SelectOption(
                label='Проект',
                description='Вопрос, касающийся определённого проекта (домашки)',
                value='project',
            ),
            SelectOption(
                label='Другое',
                description='Если не подошли остальные варианты',
                value='another',
            ),
        ],
    )
    async def select(self, interaction: Interaction, select: ui.Select) -> None:

        selected_value = select.values[0]

        if selected_value == 'theme_lesson':

            return_modal = QuestionThemeLessonModal(self.bot, self.bot_settings)
            selected_value_formatted = 'тема и урок'

        elif selected_value == 'project':

            return_modal = QuestionProjectModal(self.bot, self.bot_settings)
            selected_value_formatted = 'проект'

        elif selected_value == 'another':

            return_modal = QuestionAnotherModal(self.bot, self.bot_settings)
            selected_value_formatted = 'другое'

        else:

            await interaction.response.defer()

            await interaction.followup.send(
                'Произошла ошибка, пожалуйста, попробуйте ещё раз или свяжитесь с поддержкой'
            )

            await interaction.followup.edit_message(
                interaction.message.id,
                content='Произошла ошибка при выборе',
                view=None,
            )

            return

        await interaction.response.send_modal(return_modal)

        await interaction.followup.edit_message(
            interaction.message.id,
            content=f'Выбран тип: {selected_value_formatted}',
            view=None,
        )


class SendAnonymousMessageView(ui.View):

    def __init__(self, bot: Bot, bot_settings: Settings):

        self.bot = bot
        self.bot_settings = bot_settings
        self.question_select = None

        super().__init__()

    async def select_callback(self, interaction: Interaction) -> None:

        target_question_type, target_question_id = self.question_select.values[0].split('&')

        if target_question_type == QuestionThemeLesson.QUESTION_TYPE:
            target_question = await QuestionThemeLesson.get(id=target_question_id)

        elif target_question_type == QuestionProject.QUESTION_TYPE:
            target_question = await QuestionProject.get(id=target_question_id)

        elif target_question_type == QuestionAnother.QUESTION_TYPE:
            target_question = await QuestionAnother.get(id=target_question_id)

        else:

            await interaction.response.defer()

            await interaction.followup.send(
                'Произошла ошибка, пожалуйста, попробуйте ещё раз или свяжитесь с поддержкой'
            )

            return

        target_thread: Thread = self.bot.get_channel(target_question.discord_channel_id)

        await interaction.response.send_modal(SendAnonymousMessageModal(self.bot, self.bot_settings, target_thread))

        await interaction.followup.edit_message(
            interaction.message.id,
            content=f'Выбрана отправка анонимного сообщения в {target_thread.jump_url}',
            view=None,
        )

    async def add_select_ui(self, user_discord_id: int) -> bool | str:
        """
        :return: True if success, else error message
        """

        user_question_choices = await get_all_questions(
            creator=await get_user_model_by_discord_id(user_discord_id), is_completed=False
        )

        if not user_question_choices:
            return 'Не удалось получить незавершённые вопросы'

        select_options = []

        for question in user_question_choices:
            select_options.append(
                SelectOption(
                    label=question.get_thread_name(),
                    description=question.get_context_short(),
                    value=f'{question.QUESTION_TYPE}&{question.id}',
                )
            )

        self.question_select = ui.Select(
            placeholder='Выберите вопрос, в который хотите отправить сообщение',
            min_values=1,
            max_values=1,
            options=select_options,
        )

        self.question_select.callback = self.select_callback

        self.add_item(self.question_select)

        return True
