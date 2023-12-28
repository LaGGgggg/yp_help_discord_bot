from discord import Intents, Message, ForumChannel, Thread
from discord.ext.commands import Bot, context
from tortoise import Tortoise

from logging_config import get_logger
from settings import get_settings
from views import QuestionThemeMenuView


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

    async def init_new_forum_channel_thread(name: str, content: str) -> Thread:

        help_forum_channel: ForumChannel = bot.get_channel(bot_settings.HELP_FORUM_CHANNEL_ID)

        thread = await help_forum_channel.create_thread(name=name, content=content)

        return thread.thread

    @bot.command()
    async def new_question(ctx: context.Context) -> None:
        await ctx.send('Выберите тип вопроса', view=QuestionThemeMenuView(init_new_forum_channel_thread))

    bot.run(bot_settings.BOT_TOKEN)


if __name__ == '__main__':
    main()
