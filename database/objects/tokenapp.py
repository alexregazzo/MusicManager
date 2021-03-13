from __future__ import annotations

import utils
from .base import Base


class TokenApp(Base):

    def __init__(self, *,
                 tok_id: int,
                 use_username: str,
                 tok_access_token: str,
                 tok_active: int,
                 tok_created_datetime: int,
                 ):
        self.tok_id = tok_id
        self.use_username = use_username
        self.tok_access_token = tok_access_token
        self.tok_active = tok_active
        self.tok_created_datetime = tok_created_datetime

    @classmethod
    def create(cls, *,
               use_username: str,
               tok_active: int = 1,
               ) -> TokenApp:
        tok_created_datetime = utils.get_current_timestamp_str()
        tok_access_token = utils.gen_token()
        return cls.get(
            tok_id=cls._insert(use_username=use_username,
                               tok_access_token=tok_access_token,
                               tok_active=tok_active,
                               tok_created_datetime=tok_created_datetime))
