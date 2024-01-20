from typing import Type

from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from cogs._cog_base import CogBase
from models import QuestionStatistics
from models_utils import get_question_by_discord_channel_id


class StatisticsCog(CogBase):
    @command(description='Просмотреть статистику бота')
    async def get_bot_statistics(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        if not await self.check_is_superuser(ctx):
            return

        questions_statistics = await QuestionStatistics.filter(requests__gt=10).order_by('-requests')

        if questions_statistics:

            message = 'Вот список самых популярных (по запросам в боте) вопросов:\n'

            for question_statistics in questions_statistics:
                question = await get_question_by_discord_channel_id(question_statistics.discord_channel_id)

                question_channel = self.bot.get_channel(question.discord_channel_id)

                message += (
                    f'{question_statistics.requests} - [{question.get_thread_name()}]({question_channel.jump_url})'
                    f"  {question.pub_date.strftime('%d.%m.%y')}  ***{'' if question.is_completed else 'не '}решён***\n"
                )

            message += '*Число слева от вопроса - количество запросов'

        else:
            message = 'Не удалось найти подходящую статистику'

        await ctx.send(message)


async def get_cog() -> Type[Cog]:
    return StatisticsCog
