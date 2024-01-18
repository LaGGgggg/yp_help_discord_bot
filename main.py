from importlib import import_module
from os import listdir

from discord import Intents
from discord.ext.commands import Bot
from tortoise import Tortoise

from logging_config import get_logger
from settings import get_settings, Settings


class CustomBot(Bot):

    def __init__(self, bot_settings: Settings, *args, **kwargs) -> None:

        self.bot_settings = bot_settings
        self.logger = get_logger(__name__)

        super().__init__(*args, **kwargs)

    async def setup_hook(self):

        await Tortoise.init(db_url=self.bot_settings.DB_URL, modules={'models': ['models']})

        await Tortoise.generate_schemas()

        for file_name in listdir(self.bot_settings.COGS_DIR_NAME):

            # skip all non-python files and supporting files (starts with "_")
            if '.py' not in file_name or file_name[0] == '_': # TODO Можно было еще использовать .startwith()

                self.logger.info(f'Non-cog file found, skip it: "{file_name}"')

                continue

            self.logger.info(f'Start cog file adding: "{file_name}"')

            try:

                cog_module = import_module(f"{self.bot_settings.COGS_DIR_NAME}.{file_name.rsplit('.py', 1)[0]}")

                cog_class = await cog_module.get_cog()

                await self.add_cog(cog_class(self, get_logger, self.bot_settings))
            # TODO вообще лучше не жрать все ошибки, вы конечно пишете их в логгер, но это энивей не панацея, если присутствует какая-то неизвестная ошибка,
            # при которой бот должен падать еще НА ЗАПУСКЕ, то пусть падает и разраб чинит все это
            except Exception as e: 
                self.logger.error(f'An error occurred while cog adding: {e}')

            else:
                self.logger.info(f'Cog file adding completed successfully')


def main() -> None: # TODO Вообще есть несколько лагерей, и я считаю что лучше не прописывать None типизацию, так как это по дефолту так

    # Preparation:

    bot_settings = get_settings()

    if not bot_settings:
        return

    # Setting up and launching a bot:

    intents = Intents.default()
    intents.message_content = True

    bot = CustomBot(bot_settings=bot_settings, command_prefix='/', intents=intents)

    bot.run(bot_settings.BOT_TOKEN)


if __name__ == '__main__':
    main()
