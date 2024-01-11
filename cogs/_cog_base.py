from typing import Callable
from logging import Logger

from discord.ext.commands import Cog

from settings import Settings


class CogBase(Cog):

    def __init__(self, bot, get_logger_function: Callable[[str], Logger], bot_settings: Settings) -> None:

        self.bot = bot
        self.logger = get_logger_function(__name__)
        self.bot_settings = bot_settings

    @Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info(f'Cog ({self.__cog_name__}) logged on as {self.bot.user}')
