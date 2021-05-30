from __future__ import annotations

import typing

import spotify.hints
import utils
from .base import Base
from .exceptions import *

logger = utils.get_logger(__file__)


class Artist(Base):
    def __init__(self, *,
                 art_id: str,
                 art_href: str,
                 art_name: str,
                 art_uri: str):
        self.art_id = art_id
        self.art_href = art_href
        self.art_name = art_name
        self.art_uri = art_uri

    @classmethod
    def create(cls, *,
               art_id: str,
               art_href: str,
               art_name: str,
               art_uri: str,
               onExistRaiseError: bool = True
               ) -> Artist:
        try:
            cls._insert(art_id=art_id,
                        art_href=art_href,
                        art_name=art_name,
                        art_uri=art_uri)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(art_id=art_id)

    @classmethod
    def createMultipleRaw(cls, *, raw_artists=typing.List[spotify.hints.Artist], onExistRaiseError: bool = True) -> \
            typing.List[Artist]:
        results = []
        for raw_artist in raw_artists:
            try:
                artist = cls.create(art_id=raw_artist["id"],
                                    art_href=raw_artist["href"],
                                    art_name=raw_artist["name"],
                                    art_uri=raw_artist["uri"],
                                    onExistRaiseError=onExistRaiseError)
            except ObjectAlreadyExistError:
                if onExistRaiseError:
                    raise
                artist = Artist.get(art_id=raw_artist["id"])
            results.append(artist)
        return results
