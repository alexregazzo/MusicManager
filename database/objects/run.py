from __future__ import annotations
from .base import Base
import utils

logger = utils.get_logger(__file__)


class Run(Base):
    TYPE_GET_HISTORY = "get_history"
    TYPE_MAKE_PLAYLIST = "make_playlist"
    TYPE_FOLLOWS_PLAYLIST_CHECK = "check_if_follow_playlist"
    TYPE_FOLLOW_PLAYLIST = "follow_playlist"

    def __init__(self, *,
                 run_id: int,
                 use_username: str,
                 run_type: str,
                 run_success: int,
                 run_message: str = None,
                 run_error_type: str = None,
                 run_traceback: str = None,
                 run_datetime: str):
        self.run_id = run_id
        self.use_username = use_username
        self.run_type = run_type
        self.run_success = run_success
        self.run_message = run_message
        self.run_error_type = run_error_type
        self.run_traceback = run_traceback
        self.run_datetime = run_datetime

    @classmethod
    def create(cls, *,
               use_username: str,
               run_type: str,
               run_success: int,
               run_message: str = None,
               run_error_type: str = None,
               run_traceback: str = None,
               run_datetime: str
               ) -> Run:
        return cls.get(
            run_id=cls._insert(use_username=use_username,
                               run_type=run_type,
                               run_success=run_success,
                               run_message=run_message,
                               run_error_type=run_error_type,
                               run_traceback=run_traceback,
                               run_datetime=run_datetime))
