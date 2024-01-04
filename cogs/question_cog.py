from typing import Type

from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from cogs._cog_base import CogBase
from views import QuestionThemeMenuView
from models import get_question_by_discord_channel_id


class QuestionCog(CogBase):

    @command()
    async def new_question(self, ctx: Context) -> None:
        await ctx.send('Выберите тип вопроса', view=QuestionThemeMenuView(self.bot, self.bot_settings))

    @command()
    async def complete_current_question(self, ctx: Context) -> None:

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


async def get_cog() -> Type[Cog]:
    return QuestionCog
