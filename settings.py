from os import environ
from dataclasses import dataclass

from dotenv import load_dotenv

from exceptions import IncorrectSettingsSetupError, IncorrectEnvVarSetupError


@dataclass
class Settings:

    BOT_TOKEN: str
    HELP_FORUM_CHANNEL_ID: int
    DB_URL: str
    COGS_DIR_NAME: str
    SUPERUSERS_IDS: list[int]
    DEBUG: bool


def get_settings() -> Settings:

    load_dotenv()

    received_env_vars = {}

    for env_var_name, env_var_type in Settings.__annotations__.items():

        env_var_value = environ.get(env_var_name)

        if not env_var_value:
            raise IncorrectEnvVarSetupError(f'{env_var_name} environment variable not found, set it')

        if env_var_type is str:
            pass

        elif env_var_type is int:
            env_var_value = int(env_var_value)

        elif env_var_type is bool:
            env_var_value = env_var_value.lower() == 'true'

        # This works, "is" - not. list[int] == list[int] -> True; list[str] == list[int] -> False
        elif env_var_type == list[int]:
            env_var_value = [int(i) for i in env_var_value.split(',')]

        else:
            raise IncorrectSettingsSetupError(f'Unknown environment variable type found: {env_var_type}')

        received_env_vars[env_var_name] = env_var_value

    return Settings(**received_env_vars)
