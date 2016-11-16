import logging

import logging
from logging.config import dictConfig
from settings import PROD

LOG_LEVEL = logging.INFO if PROD else logging.DEBUG

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
                  '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': LOG_LEVEL}
    },
    root={
        'handlers': ['h'],
        'level': LOG_LEVEL,
    },
)

dictConfig(logging_config)

logger = logging.getLogger()
logger.debug('often makes a very good meal of %s', 'visiting tourists')
