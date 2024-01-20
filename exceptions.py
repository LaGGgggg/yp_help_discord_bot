class IncorrectEnvVarSetupError(Exception):

    def __init__(self, env_var_name: str = '') -> None:
        self.env_var_name = env_var_name

    def __str__(self) -> str:
        return f'Incorrect environment variable setup: {self.env_var_name}'


class IncorrectSettingsSetupError(Exception):

    def __init__(self, context: str = '') -> None:
        self.context = context

    def __str__(self) -> str:
        return f'Incorrect settings setup: {self.context}'
