import logging
LOG_FMT = '[%(levelname)s][%(module)s %(funcName)s %(lineno)d] %(message)s'
LOG_LEVEL = logging.INFO
logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)
SDL_DATE_FMT = '%Y-%m-%d %H:%M:%S'
ISO_8601_FMT = '%Y%m%dT%H%M%SZ'
ADMIN_LANG = 'en-US'
CREATION_TOOL = 'sdltm2tmx'
VERSION = '2.0.0'
HEADER_ATTRS = {
    'creationtool': CREATION_TOOL,
    'creationtoolversion': VERSION,
    'datatype': 'PlainText',
    'segtype': 'sentence',
    'adminlang': ADMIN_LANG
}
TMX_VERSION = '1.4'
TMX_DTD_NAME = 'tmx14.dtd'
