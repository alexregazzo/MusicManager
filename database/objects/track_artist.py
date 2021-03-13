from __future__ import annotations

import typing

import utils
from .base import Base
from .exceptions import *

logger = utils.get_logger(__file__)


class Track_Artist(Base):
    def __init__(self, *,
                 traart_id: int,
                 tra_id: str,
                 art_id: str):
        self.traart_id = traart_id
        self.tra_id = tra_id
        self.art_id = art_id

    @classmethod
    def create(cls, *,
               tra_id: str,
               art_id: str) -> Track_Artist:

        return cls.get(traart_id=cls._insert(tra_id=tra_id, art_id=art_id))

    def __eq__(self, other: typing.Union[Track_Artist, dict]):
        if type(other) is Track_Artist:
            return other.tra_id == self.tra_id and other.art_id == self.art_id
        elif type(other) is dict:
            if "tra_id" in other and "art_id" in other:
                return other["tra_id"] == self.tra_id and other["art_id"] == self.art_id

        raise NotComparableObjectsError()

    @classmethod
    def createMultiple(cls, *, tra_id: str, art_ids: typing.List[str]) -> typing.List[Track_Artist]:
        results = []
        track_artist_links = cls.getAll(tra_id=tra_id)
        for art_id in art_ids:
            current_raw_track_artist = {"art_id": art_id, "tra_id": tra_id}
            try:
                index = track_artist_links.index(current_raw_track_artist)
                results.append(track_artist_links[index])
            except ValueError:
                results.append(cls.create(**current_raw_track_artist))
        return results
