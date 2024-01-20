from logging import getLogger, Logger
from logging.config import dictConfig
from pathlib import Path

from settings import get_settings


SETTINGS = get_settings()

BASE_DIR: Path = Path(__file__).resolve().parent
LOGS_DIR: Path = BASE_DIR / 'logs'

LOGS_DIR.mkdir(exist_ok=True)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{levelname}] [{asctime}] - "{message}"',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': LOGS_DIR / 'warning.log',
            'maxBytes': 1024 * 1024 * 100,  # 100 Mb
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console' if SETTINGS.DEBUG else 'file_warning'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

dictConfig(LOGGING_CONFIG)


def get_logger(name: str | None = None) -> Logger:
    return getLogger(name)
