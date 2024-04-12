from typing import Type

from discord import HTTPException, Forbidden
from discord.ext.commands import Cog, command, hybrid_command
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

            await ctx.reply(
                'Не удалось синхронизировать дерево команд, попробуйте ещё раз или обратитесь в поддержку'
            )

        else:

            self.logger.info('Command tree synced')

            await ctx.reply(
                'Дерево команд синхронизированно, до появления видимого эффекта может пройти некоторое время'
            )

    async def _help_handler(self, ctx: Context) -> None:

        if await self.check_is_user_banned(ctx.author.id):
            return

        help_message = (
            'Привет! Я бот, который поможет вам быстро найти ответ на вопрос по учёбе.'
            ' Меня создал на мастерской проектов ваш однокурсник Никита.\n'
            'Я умею искать ответы на вопрос по похожим словам в коворкинге, а ещё могу помочь задать свой вопрос'
            ' анонимно, если вы стесняетесь задавать его от своего имени.\n'
            'У меня есть четыре команды, которые можно вызвать, написав слэш в личных сообщениях.'
            ' Начните с команды **/new_question**, чтобы задать свой вопрос.\n'
            'Если что-то осталось непонятным, можно посмотреть'
            ' [инструкцию](https://www.notion.so/6ebb18f9484f404db15078e13f6bd9e3?pvs=21).'
        )

        await ctx.reply(help_message)

    @command()
    async def start(self, ctx: Context) -> None:
        await self._help_handler(ctx)

    @hybrid_command(description='Справка по боту')
    async def help(self, ctx: Context) -> None:
        await self._help_handler(ctx)


async def get_cog() -> Type[Cog]:
    return MainCog
