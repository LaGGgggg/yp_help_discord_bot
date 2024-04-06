from typing import Type

from discord import Attachment
from discord.message import Message
from discord.ext.commands import Cog, hybrid_command
from discord.ext.commands.context import Context

from cogs._cog_base import CogBase
from views import QuestionThemeMenuView, SendAnonymousMessageView, SendAnonymousImageView
from models_utils import get_question_by_discord_channel_id


class QuestionCog(CogBase):

    @hybrid_command(description='Создание нового вопроса')
    async def new_question(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        await ctx.send('Выберите тип вопроса', view=QuestionThemeMenuView(self.bot, self.bot_settings))

    @hybrid_command(description='Отмечает текущий вопрос как решённый')
    async def complete_current_question(self, ctx: Context) -> None:

        question = await get_question_by_discord_channel_id(ctx.channel.id)

        if not question:

            await ctx.reply('Вопрос не найден, убедитесь, что пишите эту команду в ветке с вопросом', ephemeral=True)

            return

        await question.fetch_related('creator')

        if ctx.author.id != question.creator.discord_id and not await self.check_is_superuser(ctx, False):

            await self.send_privileges_error_message(ctx)

            return

        if question.is_completed:

            await ctx.reply('Вопрос уже помечен как завершённый', ephemeral=True)

            return

        question.is_completed = True

        await question.save(update_fields=('is_completed',))

        await ctx.channel.edit(name=f'[РЕШЕНО] {ctx.channel.name}')

        success_message = 'Вопрос помечен как решённый'

        await ctx.channel.send(success_message)
        await ctx.reply(success_message, ephemeral=True)

    @hybrid_command(description='Отправляет анонимное сообщение')
    async def send_anonymous_message(self, ctx: Context) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        view = SendAnonymousMessageView(self.bot, self.bot_settings)

        view_add_select_ui_result = await view.add_select_ui(ctx.author.id)

        if view_add_select_ui_result is not True:

            await ctx.send(view_add_select_ui_result)

            return

        await ctx.send('Выбирайте вопрос и отправляйте сообщение', view=view)

    @hybrid_command(description='Отправляет анонимное фото')
    async def send_anonymous_photo(self, ctx: Context, image_file: Attachment) -> None:

        if not await self.check_is_private_channel(ctx):
            return

        if not image_file:

            await ctx.send('Прикрепите к этой команде изображение, которое хотите отослать')

            return

        if image_file.content_type not in ('image/jpeg', 'image/jpg', 'image/png'):

            await ctx.send('Пожалуйста, прикрепите **изображение** в одном из форматов: jpeg, jpg, png')

            return

        view = SendAnonymousImageView(self.bot, self.bot_settings, image_file.url)

        view_add_select_ui_result = await view.add_select_ui(ctx.author.id)

        if view_add_select_ui_result is not True:

            await ctx.send(view_add_select_ui_result)

            return

        await ctx.send('Выбирайте вопрос и отправляйте изображение', view=view)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:

        # don't respond to ourselves
        if message.author == self.bot.user:
            return

        channel_question = await get_question_by_discord_channel_id(message.channel.id)

        if channel_question and not channel_question.is_completed:

            await channel_question.fetch_related('creator')

            question_creator_user_id = channel_question.creator.discord_id

            # don't respond to question creator
            if message.author.id == question_creator_user_id:
                return

            question_creator_user = self.bot.get_user(question_creator_user_id)

            if not question_creator_user:
                question_creator_user = await self.bot.fetch_user(question_creator_user_id)

            await question_creator_user.send(
                f'Новое [сообщение]({message.jump_url}) в вопросе {message.channel.jump_url}:\n```{message.content}```'
                '\nP.S. Вы можете ответить на него через бота'
            )


async def get_cog() -> Type[Cog]:
    return QuestionCog
