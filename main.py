from typing import Any
from logging import Logger
from os import environ

from dotenv import load_dotenv
from discord import Client, Intents

from logging_config import get_logger


class MyClient(Client):

    def __init__(self, logger: Logger, *, intents: Intents, **options: Any):

        self.logger = logger

        super().__init__(intents=intents, **options)

    async def on_ready(self):
        self.logger.info(f'Logged on as {self.user}')

    async def on_message(self, message):

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


def main() -> None:

    logger = get_logger(__name__)

    # Environment variables:

    load_dotenv()

    bot_token = environ.get('BOT_TOKEN')

    if not bot_token:

        logger.error('BOT_TOKEN environment variable not found, set it')

        return

    # Setting up and launching a bot:

    intents = Intents.default()
    intents.message_content = True

    client = MyClient(logger, intents=intents)
    client.run(bot_token)


if __name__ == '__main__':
    main()
