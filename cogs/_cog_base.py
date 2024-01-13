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

        else:
            return True
