from contextlib import contextmanager
import sqlite3
import logging


log = logging.getLogger(__name__)


@contextmanager
def session(src):
    conn = None
    try:
        conn = sqlite3.connect(src)
        conn.row_factory = sqlite3.Row
        yield conn.cursor()
    except Exception as E:
        log.error(repr(E))
        if conn:
            conn.rollback()
            conn.close()
    finally:
        if conn:
            # log.info('db connection closed')
            conn.close()
