import logging
LOG_FMT = '[%(levelname)s][%(module)s %(funcName)s %(lineno)d] %(message)s'
LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)
SDL_DATE_FMT = '%Y-%m-%d %H:%M:%S'
ISO_8601_FMT = '%Y%m%dT%H%M%SZ'
