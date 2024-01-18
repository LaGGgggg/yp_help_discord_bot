from typing import Callable
from logging import Logger

from discord.abc import PrivateChannel
from discord.ext.commands import Cog
from discord.ext.commands.context import Context

from settings import Settings


class CogBase(Cog):

    def __init__(self, bot, get_logger_function: Callable[[str], Logger], bot_settings: Settings) -> None:

        self.bot = bot
        self.logger = get_logger_function(__name__)
        self.bot_settings = bot_settings

    @Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info(f'Cog ({self.__cog_name__}) logged on as {self.bot.user}')

    @staticmethod
    async def check_is_private_channel(ctx: Context) -> bool:

        if not isinstance(ctx.channel, PrivateChannel):

            await ctx.send('Убедитесь, что пишете боту в **личные** сообщения')

            return False

        else: # TODO Опять же, можно убрать else и вынести второй ретурн на один уровень вложенности выше
            return True

    async def check_is_superuser(self, ctx: Context) -> bool:

        if ctx.author.id in self.bot_settings.SUPERUSERS_IDS:
            return True

        else: # TODO Аналогично с 32ой

            await ctx.send('У вас нет прав для выполнения этой команды')

            return False
