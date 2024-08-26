# MySQLdb imports
import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor
import contextlib
from typing import ContextManager

# -------------------------------------------------------------------------------- #
# ----------------------------- Def Connector/Cursor ----------------------------- #
@contextlib.contextmanager
def connection(*args, **kwargs) -> ContextManager[Connection]: # type: ignore    <-- | This clears the warning...  Black magic
    conn = MySQLdb.connect(*args, **kwargs)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()

@contextlib.contextmanager
def cursor(*args, **kwargs) -> ContextManager[Cursor]: # type: ignore
    with connection(*args, **kwargs) as conn:
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()