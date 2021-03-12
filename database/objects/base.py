from __future__ import annotations
from database import Database
import database
from .exceptions import *
import typing
import utils
import sqlite3

T = typing.TypeVar('T', bound='Base')
logger = utils.get_logger(__file__)


class Base:
    def database_params(self) -> dict:
        dic = dict()
        for k, v in self.__dict__.items():
            if k[0] != "_":
                dic[k] = v
        return dic

    def json(self, *args):
        return self.database_params()

    def __repr__(self) -> str:
        return F"""<{type(self).__name__}: {"  ".join([F"{k}={v}" for k, v in self.__dict__.items()])}>"""

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def table_pk(cls) -> str:
        return F"""{"".join([x[:3] for x in cls.table_name().split("_")])}_id"""

    @classmethod
    def _insert(cls, **kwargs) -> int:
        try:
            with Database() as db:
                return db.insert(database.utils.make_insert(*kwargs.keys(), t_name=cls.table_name()), **kwargs)
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ObjectAlreadyExistError()
            else:
                logger.warning(f"Problem adding {cls.table_name()}: {e}")
                raise

    @classmethod
    def _select(cls, order_by: typing.List[typing.Tuple[str, str]] = None, limit: int = None, **kwargs) -> list:
        with Database() as db:
            sql = database.utils.make_select(*kwargs.keys(), t_name=cls.table_name())
            if order_by is not None:
                print(sql)
                sql += " ORDER BY " + ", ".join([F"{ob[0]} {ob[1].upper()}" for ob in order_by])
                print(sql)

            if limit is not None:
                assert type(limit) is int
                sql += F" LIMIT {limit}"
            return db.select(sql, **kwargs)

    def update(self, **kwargs) -> None:
        existing_keys = list(self.__dict__.keys())
        new_keys = list(kwargs.keys())
        if all([nk in existing_keys for nk in new_keys]):
            self.__dict__.update(kwargs)
            return self._update()
        else:
            raise CreationOfNewAttributesNotAllowedError()

    def _update(self) -> None:
        with Database() as db:
            return db.update(
                database.utils.make_update(set_list=list(self.database_params().keys()), where_list=[self.table_pk()],
                                           t_name=self.table_name()), **self.database_params())

    def delete(self) -> None:
        return self._delete()

    def _delete(self):
        with Database() as db:
            return db.delete(database.utils.make_delete(self.table_pk(), t_name=self.table_name()),
                             **self.database_params())

    @classmethod
    def get(cls, **kwargs) -> T:
        try:
            # noinspection PyArgumentList
            return cls(**(cls._select(**kwargs)[0]))
        except IndexError:
            raise ObjectDoesNotExistError()

    @classmethod
    def getAll(cls, limit: int = None, order_by: typing.List[typing.Tuple[str, str]] = None, **kwargs) -> typing.List[
        T]:
        # noinspection PyArgumentList
        return [cls(**x) for x in cls._select(**kwargs, order_by=order_by, limit=limit)]
