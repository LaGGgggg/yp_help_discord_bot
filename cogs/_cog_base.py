from typing import Callable
from logging import Logger

from discord.abc import PrivateChannel
from discord.ext.commands import Cog
from discord.ext.commands.context import Context

from settings import Settings
from models_utils import get_user_model_by_discord_id


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

            await ctx.reply('Убедитесь, что пишете боту в **личные** сообщения', ephemeral=True)

            return False

        return True

    @staticmethod
    async def send_privileges_error_message(ctx: Context) -> None:
        await ctx.reply('У вас нет прав для выполнения этой команды', ephemeral=True)

    async def check_is_superuser(self, ctx: Context, is_send_error_message: bool = True) -> bool:

        if ctx.author.id in self.bot_settings.SUPERUSERS_IDS:
            return True

        if is_send_error_message:
            await self.send_privileges_error_message(ctx)

        return False

    @staticmethod
    async def check_is_user_banned(author_id: int) -> bool:

        user = await get_user_model_by_discord_id(author_id)

        return user.is_banned
