import os
import sqlite3
import threading
import typing

CURRENT_DIRPATH = os.path.dirname(__file__)
TABLES_PATH = os.path.join(CURRENT_DIRPATH, "table.sql")
DATABASE_NAME = "data.db"
DATABASE_PATH = os.path.join(CURRENT_DIRPATH, "..", DATABASE_NAME)


class Database:
    lock = threading.Lock()
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = true;")
    with open(TABLES_PATH) as f:
        cursor.executescript(f.read())

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.lock.release()

    def insert(self, sql: str, ignore_errors: typing.List[str] = None, ignore_errors_contain: typing.List[str] = None,
               **kwargs) -> int:
        try:
            # print(sql, kwargs)
            self.cursor.execute(sql, kwargs)
            return self.cursor.lastrowid
        except Exception as e:
            if ignore_errors is not None:
                if str(e) in ignore_errors:
                    return 0
            if ignore_errors_contain is not None:
                for iec in ignore_errors_contain:
                    if iec in str(e):
                        return 0
            raise

    def select(self, sql: str, **kwargs) -> list:
        try:
            # print(sql, kwargs)
            self.cursor.execute(sql, kwargs)
            return self.cursor.fetchall()
        except Exception as e:
            raise

    def update(self, sql: str, **kwargs) -> None:
        try:
            # print(sql, kwargs)
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            raise

    def delete(self, sql: str, **kwargs) -> None:
        try:
            # print(sql, kwargs)
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            raise
