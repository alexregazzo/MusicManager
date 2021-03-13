from __future__ import annotations

import typing

import spotify.hints
import utils
from .base import Base
from .exceptions import *

logger = utils.get_logger(__file__)


class Album_Image(Base):
    def __init__(self, *,
                 albima_url: str,
                 alb_id: str,
                 albima_width: int = None,
                 albima_height: int = None):
        self.albima_url = albima_url
        self.alb_id = alb_id
        self.albima_width = albima_width
        self.albima_height = albima_height

    @classmethod
    def table_pk(cls) -> str:
        return "albima_url"

    @classmethod
    def create(cls, *,
               albima_url: str,
               alb_id: str,
               albima_width: int = None,
               albima_height: int = None,
               onExistRaiseError: bool = True
               ) -> Album_Image:
        try:
            cls._insert(albima_url=albima_url,
                        alb_id=alb_id,
                        albima_width=albima_width,
                        albima_height=albima_height)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(albima_url=albima_url)

    @classmethod
    def createMultipleRaw(cls, alb_id: str, rawImages: typing.List[spotify.hints.Image],
                          onExistRaiseError: bool = True) -> typing.List[Album_Image]:
        return [cls.create(alb_id=alb_id,
                           albima_url=rawImage["url"],
                           albima_width=rawImage["width"],
                           albima_height=rawImage["height"],
                           onExistRaiseError=onExistRaiseError) for rawImage in rawImages]
