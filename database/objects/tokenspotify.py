from __future__ import annotations

import datetime

import spotify.hints
import utils
from .base import Base
from .exceptions import *


class TokenSpotify(Base):
    def __init__(self, *,
                 use_username: str,
                 tok_user_spotify_id: str = None,
                 tok_access_token: str,
                 tok_token_type: str,
                 tok_scope: str,
                 tok_expires_in: int,
                 tok_refresh_token: str,
                 tok_last_updated_datetime: str):
        self.use_username = use_username
        self.tok_user_spotify_id = tok_user_spotify_id
        self.tok_access_token = tok_access_token
        self.tok_token_type = tok_token_type
        self.tok_scope = tok_scope
        self.tok_expires_in = tok_expires_in
        self.tok_refresh_token = tok_refresh_token
        self.tok_last_updated_datetime = tok_last_updated_datetime

    @classmethod
    def table_pk(cls) -> str:
        return "use_username"

    @classmethod
    def create(cls, *,
               use_username: str,
               tok_user_spotify_id: str = None,
               tok_access_token: str,
               tok_token_type: str,
               tok_scope: str,
               tok_expires_in: int,
               tok_refresh_token: str,
               tok_last_updated_datetime: str,
               onExistRaiseError: bool = True
               ) -> TokenSpotify:

        try:
            cls._insert(use_username=use_username,
                        tok_user_spotify_id=tok_user_spotify_id,
                        tok_access_token=tok_access_token,
                        tok_token_type=tok_token_type,
                        tok_scope=tok_scope,
                        tok_expires_in=tok_expires_in,
                        tok_refresh_token=tok_refresh_token,
                        tok_last_updated_datetime=tok_last_updated_datetime)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(use_username=use_username)

    @classmethod
    def createRaw(cls, *,
                  rawToken: spotify.hints.RefreshTokenSuccessResponse,
                  use_username: str,
                  requested_time_str: str,
                  onExistRaiseError: bool = True,
                  onExistUpdate: bool = True
                  ) -> TokenSpotify:
        try:
            cls.create(use_username=use_username,
                       tok_access_token=rawToken["access_token"],
                       tok_token_type=rawToken["token_type"],
                       tok_scope=rawToken["scope"],
                       tok_expires_in=rawToken["expires_in"],
                       tok_refresh_token=rawToken["refresh_token"],
                       tok_last_updated_datetime=requested_time_str,
                       onExistRaiseError=onExistRaiseError)
            token = cls.get(use_username=use_username)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
            token = cls.get(use_username=use_username)
            if onExistUpdate:
                token.update(tok_access_token=rawToken["access_token"],
                             tok_token_type=rawToken["token_type"],
                             tok_scope=rawToken["scope"],
                             tok_expires_in=rawToken["expires_in"],
                             tok_refresh_token=rawToken["refresh_token"],
                             tok_last_updated_datetime=requested_time_str)
        return token

    @property
    def expired(self) -> bool:
        token_time = utils.parse_datetime(self.tok_last_updated_datetime)
        current_time = utils.get_current_timestamp() - datetime.timedelta(seconds=10)
        return token_time + datetime.timedelta(seconds=self.tok_expires_in) < current_time
