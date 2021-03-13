from __future__ import annotations

import utils
from .base import Base
from .exceptions import *

logger = utils.get_logger(__file__)


class User(Base):
    def __init__(self, *,
                 use_username: str,
                 use_email: str = None,
                 use_password_salt: str,
                 use_password: str,
                 use_created_datetime: str):
        self.use_username = use_username
        self.use_email = use_email
        self.use_password_salt = use_password_salt
        self.use_password = use_password
        self.use_created_datetime = use_created_datetime

    def check_password(self, password: str) -> bool:
        return utils.hash_password(password, self.use_password_salt)[0] == self.use_password

    @classmethod
    def table_pk(cls) -> str:
        return "use_username"

    @classmethod
    def create(cls, *,
               use_username: str,
               use_email: str = None,
               use_password_salt: str,
               use_password: str,
               onExistRaiseError: bool = True
               ) -> User:

        use_created_datetime = utils.get_current_timestamp_str()
        try:
            cls._insert(use_username=use_username,
                        use_email=use_email,
                        use_password_salt=use_password_salt,
                        use_password=use_password,
                        use_created_datetime=use_created_datetime)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise

        return cls.get(use_username=use_username)
