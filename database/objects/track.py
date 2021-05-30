from __future__ import annotations

import typing

import spotify.hints
import utils
from spotify.client import SpotifyClient
from .album import Album
from .artist import Artist
from .base import Base
from .exceptions import *
from .track_artist import Track_Artist

logger = utils.get_logger(__file__)


class Track(Base):
    def __init__(self, *,
                 tra_id: str,
                 tra_duration_ms: int,
                 tra_href: str,
                 tra_name: str,
                 tra_preview_url: str,
                 tra_uri: str,
                 alb_id: str = None,
                 **kwargs):
        self.tra_id = tra_id
        self.tra_duration_ms = tra_duration_ms
        self.tra_href = tra_href
        self.tra_name = tra_name
        self.tra_preview_url = tra_preview_url
        self.tra_uri = tra_uri
        self.alb_id = alb_id
        self._artists = None

    def __eq__(self, other: typing.Union[Track, str]) -> bool:
        if type(other) is Track:
            return self.tra_id == other.tra_id
        elif type(other) is str:
            return self.tra_id == other
        else:
            raise NotImplementedError(F"Cannot compare Track with '{type(other)}'")

    @classmethod
    def create(cls, *,
               tra_id: str,
               tra_duration_ms: int,
               tra_href: str,
               tra_name: str,
               tra_preview_url: str,
               tra_uri: str,
               alb_id: str = None,
               onExistRaiseError: bool = True
               ) -> Track:

        try:
            cls._insert(tra_id=tra_id,
                        tra_duration_ms=tra_duration_ms,
                        tra_href=tra_href,
                        tra_name=tra_name,
                        tra_preview_url=tra_preview_url,
                        tra_uri=tra_uri,
                        alb_id=alb_id)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(tra_id=tra_id)

    @property
    def artists(self) -> typing.List[Artist]:
        if self._artists is None:
            links = Track_Artist.getAll(tra_id=self.tra_id)
            artists = []
            for link in links:
                artists.append(Artist.get(art_id=link.art_id))
            self._artists = artists
        return self._artists

    def json(self, *args) -> dict:
        addons = {
            "track_artists": lambda: {"artists": self.artists},
            "track_album": lambda: {"album": self.album}
        }

        jsonobj = {"tra_id": self.tra_id,
                   "tra_duration_ms": self.tra_duration_ms,
                   "tra_href": self.tra_href,
                   "tra_name": self.tra_name,
                   "tra_preview_url": self.tra_preview_url,
                   "tra_uri": self.tra_uri,
                   "json_arguments": list(addons.keys())}
        for arg in args:
            if arg in addons:
                jsonobj.update(addons[arg]())

        return jsonobj

    @property
    def album(self):
        if self.alb_id is None:
            self.requestAlbum()
        return Album.get(alb_id=self.alb_id)

    def requestAlbum(self):
        raw_track = SpotifyClient.getTrack(self.tra_id)
        album = Album.createRawSimplified(raw_track["album"], onExistRaiseError=False)
        self.alb_id = album.alb_id
        self.update()

    @classmethod
    def createSimplifiedRaw(cls, *, simpleRawTrack: spotify.hints.SimplifiedTrack,
                            onExistRaiseError: bool = True) -> Track:
        tra_id = simpleRawTrack["id"]
        try:
            track = cls.create(tra_id=simpleRawTrack["id"],
                               tra_duration_ms=simpleRawTrack["duration_ms"],
                               tra_href=simpleRawTrack["href"],
                               tra_name=simpleRawTrack["name"],
                               tra_preview_url=simpleRawTrack["preview_url"],
                               tra_uri=simpleRawTrack["uri"],
                               onExistRaiseError=onExistRaiseError)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
            track = Track.get(tra_id=tra_id)
        raw_artists = simpleRawTrack["artists"]
        if Artist.createMultipleRaw(raw_artists=raw_artists, onExistRaiseError=onExistRaiseError):
            artists_ids = [raw_artist["id"] for raw_artist in raw_artists]
            Track_Artist.createMultiple(tra_id=tra_id, art_ids=artists_ids)
        return track
