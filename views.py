from typing import Callable

from discord import ui, SelectOption, Interaction

from modals import QuestionThemeLessonModal, QuestionProjectModal, QuestionAnotherModal


class QuestionThemeMenuView(ui.View):

    def __init__(self, init_new_forum_channel_thread: Callable):

        self.init_new_forum_channel_thread = init_new_forum_channel_thread

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
            return_modal = QuestionThemeLessonModal(self.init_new_forum_channel_thread)

        elif selected_value == 'project':
            return_modal = QuestionProjectModal(self.init_new_forum_channel_thread)

        elif selected_value == 'another':
            return_modal = QuestionAnotherModal(self.init_new_forum_channel_thread)

        else:

            await interaction.response.defer()

            await interaction.followup.send(
                'Произошла ошибка, пожалуйста, попробуйте ещё раз или свяжитесь с поддержкой'
            )

            return

        await interaction.response.send_modal(return_modal)
