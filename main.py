from discord import Intents, Message
from discord.ext.commands import Bot, context
from tortoise import Tortoise

from logging_config import get_logger
from settings import get_settings
from views import QuestionThemeMenuView
from models import get_question_by_discord_channel_id


class CustomBot(Bot):
    async def setup_hook(self):

        await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['models']})

        await Tortoise.generate_schemas()


def main() -> None:

    # Preparation:

    logger = get_logger(__name__)

    bot_settings = get_settings()

    if not bot_settings:
        return

    # Setting up and launching a bot:

    intents = Intents.default()
    intents.message_content = True

    bot = CustomBot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready() -> None:
        logger.info(f'Logged on as {bot.user}')

    @bot.event
    async def on_message(message: Message) -> None:

        # don't respond to ourselves
        if message.author == bot.user:
            return

        await bot.process_commands(message)

    @bot.command()
    async def new_question(ctx: context.Context) -> None:
        await ctx.send('Выберите тип вопроса', view=QuestionThemeMenuView(bot, bot_settings))

    @bot.command()
    async def complete_current_question(ctx: context.Context) -> None:

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

    bot.run(bot_settings.BOT_TOKEN)


if __name__ == '__main__':
    main()
