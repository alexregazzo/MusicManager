from __future__ import annotations
from .base import Base
from .exceptions import *
from .album_image import Album_Image
from spotify import SpotifyClient
import spotify.hints
import utils
import typing

logger = utils.get_logger(__file__)


class Album(Base):
    def __init__(self, *,
                 alb_id: str,
                 alb_href: str,
                 alb_name: str,
                 alb_uri: str):
        self.alb_id = alb_id
        self.alb_href = alb_href
        self.alb_name = alb_name
        self.alb_uri = alb_uri

    @classmethod
    def create(cls, *,
               alb_id: str,
               alb_href: str,
               alb_name: str,
               alb_uri: str,
               onExistRaiseError: bool = True
               ) -> Album:
        try:
            cls._insert(alb_id=alb_id,
                        alb_href=alb_href,
                        alb_name=alb_name,
                        alb_uri=alb_uri)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(alb_id=alb_id)

    def requestImages(self):
        raw_album = SpotifyClient.getAlbum(self.alb_id)
        Album_Image.createMultipleRaw(alb_id=self.alb_id, rawImages=raw_album["images"], onExistRaiseError=False)

    @property
    def images(self) -> typing.List[Album_Image]:
        results = Album_Image.getAll(alb_id=self.alb_id)
        if len(results) == 0:
            self.requestImages()
            results = Album_Image.getAll(alb_id=self.alb_id)
        return results

    def json(self) -> dict:
        return {"alb_id": self.alb_id,
                "alb_href": self.alb_href,
                "alb_name": self.alb_name,
                "alb_uri": self.alb_uri,
                "images": self.images}

    @classmethod
    def createRawSimplified(cls, rawAlbum: spotify.hints.SimplifiedAlbum, onExistRaiseError: bool = True) -> Album:
        try:
            cls.create(alb_id=rawAlbum["id"],
                       alb_href=rawAlbum["href"],
                       alb_name=rawAlbum["name"],
                       alb_uri=rawAlbum["uri"],
                       onExistRaiseError=onExistRaiseError)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        Album_Image.createMultipleRaw(alb_id=rawAlbum["id"], rawImages=rawAlbum["images"], onExistRaiseError=onExistRaiseError)
        return cls.get(alb_id=rawAlbum["id"])
