from typing import Type

from discord import HTTPException, Forbidden
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from cogs._cog_base import CogBase


class MainCog(CogBase):
    @command()
    async def sync(self, ctx: Context) -> None:

        if await self.check_is_user_banned(ctx.author.id):
            return

        if not await self.check_is_private_channel(ctx) or not await self.check_is_superuser(ctx):
            return

        try:
            await self.bot.tree.sync()

        except (HTTPException, Forbidden) as e:

            self.logger.warning(f'An error occurred while command tree syncing: "{e}"')

            await ctx.send(
                'Не удалось синхронизировать дерево команд, попробуйте ещё раз или обратитесь в поддержку'
            )

        else:

            self.logger.info('Command tree synced')

            await ctx.send(
                'Дерево команд синхронизированно, до появления видимого эффекта может пройти некоторое время'
            )


async def get_cog() -> Type[Cog]:
    return MainCog
