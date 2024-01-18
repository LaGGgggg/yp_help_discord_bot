from os import environ
from dataclasses import dataclass

from dotenv import load_dotenv

from logging_config import get_logger


@dataclass
class Settings:

    BOT_TOKEN: str
    HELP_FORUM_CHANNEL_ID: int
    DB_URL: str
    COGS_DIR_NAME: str
    SUPERUSERS_IDS: list[int]


def get_settings() -> Settings | None:

    logger = get_logger(__name__)

    load_dotenv()

    received_env_vars = {}

    for env_var_name, env_var_type in Settings.__annotations__.items():

        env_var_value = environ.get(env_var_name)

        if not env_var_value:

            logger.error(f'{env_var_name} environment variable not found, set it') 

            return # TODO Я бы вместо ретурна тут рэйзил ошибку что конфиг гавно, переделайте

        else: # TODO Вот тут else уже не нужен будет, так как на 35ой вы ретурнитесь из функции

            if env_var_type is str: # TODO Пока не могу придумать как это лучше реализовать, но мне не нравится эта штука xD
                pass

            elif env_var_type is int:
                env_var_value = int(env_var_value)

            # This works, "is" - not. list[int] == list[int] -> True; list[str] == list[int] -> False
            elif env_var_type == list[int]:
                env_var_value = [int(i) for i in env_var_value.split(',')]

            else:

                logger.error(f'Unknown environment variable type found: {env_var_type}')

                return # TODO Аналогично 35ой

        received_env_vars[env_var_name] = env_var_value

    return Settings(**received_env_vars)

# TODO Оверол, очень хорошо сделано, я бы мб только еще ушел от конфига в пайтон файле к .cfg, но это уже потяжелее штука