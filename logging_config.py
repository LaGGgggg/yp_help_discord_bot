from logging import getLogger, Logger
from logging.config import dictConfig


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
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


dictConfig(LOGGING_CONFIG)


def get_logger(name: str | None = None) -> Logger:
    return getLogger(name)
