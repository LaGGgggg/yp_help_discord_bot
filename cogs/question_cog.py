from typing import Type

from discord.message import Message
from discord.ext.commands import Cog, hybrid_command, command
from discord.ext.commands.context import Context

from cogs._cog_base import CogBase
from views import QuestionThemeMenuView, SendAnonymousMessageView
from models import get_question_by_discord_channel_id, get_all_questions, QuestionStatistics # TODO get_all_questions не используется


class QuestionCog(CogBase):
    # TODO Не уверен что нам нужны гибридные команды, но реализация зависит в итоге от вас
    @hybrid_command(description='Создание нового вопроса')
    async def new_question(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        await ctx.send('Выберите тип вопроса', view=QuestionThemeMenuView(self.bot, self.bot_settings))

    @hybrid_command(description='Отмечает текущий вопрос как решённый')
    async def complete_current_question(self, ctx: Context) -> None:
        # TODO думаю не очень хорошая идея позволять закрывать вопросы кому угодно, пусть это может сделать автор либо админ состав
        question = await get_question_by_discord_channel_id(ctx.channel.id)
        
        if not question:

            await ctx.send('Вопрос не найден, убедитесь, что пишите эту команду в ветке с вопросом')

            return

        if question.is_completed:

            await ctx.send('Вопрос уже помечен как завершённый')

            return

        question.is_completed = True

        await question.save(update_fields=('is_completed',))

        await ctx.channel.edit(name=f'[РЕШЕНО] {ctx.channel.name}')

        await ctx.send('Вопрос помечен как решённый')

    @hybrid_command(description='Отправляет анонимное сообщение')
    async def send_anonymous_message(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        view = SendAnonymousMessageView(self.bot, self.bot_settings)

        view_add_select_ui_result = await view.add_select_ui(ctx.author.id)

        if view_add_select_ui_result is not True:
            await ctx.send(view_add_select_ui_result)
            # TODO опять же, добавляем return и убираем else
        else:
            await ctx.send('Выбирайте вопрос и отправляйте сообщение', view=view)
    # TODO Стоило вынести стату всю в отдельную когу
    @command(description='Просмотреть статистику бота')
    async def get_bot_statistics(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        if not await self.check_is_superuser(ctx):
            return

        questions_statistics = await QuestionStatistics.filter(requests__gt=10).order_by('-requests')

        if questions_statistics:
            # TODO Вообще думаю можно было бы считать стату по именно номеру урока, но согласен, крайне туманные пожелания у нас вышли
            message = 'Вот список самых популярных (по запросам в боте) вопросов:\n'

            for question_statistics in questions_statistics:

                question = await get_question_by_discord_channel_id(question_statistics.discord_channel_id)

                question_channel = self.bot.get_channel(question.discord_channel_id)

                message += (
                    f'{question_statistics.requests} - [{question.get_thread_name()}]({question_channel.jump_url})'
                    f"  {question.pub_date.strftime('%d.%m.%y')}  ***{'' if question.is_completed else 'не'}решён***\n"
                )

            message += '*Число слева от вопроса - количество запросов'

        else:
            message = 'Не удалось найти подходящую статистику'

        await ctx.send(message)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:

        # don't respond to ourselves
        if message.author == self.bot.user:
            return

        channel_question = await get_question_by_discord_channel_id(message.channel.id)

        if channel_question and not channel_question.is_completed:

            await channel_question.fetch_related('creator')

            question_creator_user_id = channel_question.creator.discord_id

            question_creator_user = self.bot.get_user(question_creator_user_id)

            if not question_creator_user:
                question_creator_user = await self.bot.fetch_user(question_creator_user_id)

            await question_creator_user.send(
                f'Новое [сообщение]({message.jump_url}) в вопросе {message.channel.jump_url}:\n```{message.content}```'
                '\nP.S. Вы можете ответить на него через бота'
            )


async def get_cog() -> Type[Cog]:
    return QuestionCog
