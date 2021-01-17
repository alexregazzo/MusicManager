from __future__ import annotations
from .base import Base
from .exceptions import *
import spotify.hints
from .artist import Artist
from .track_artist import Track_Artist
from .album import Album
import utils
import typing
from spotify.client import SpotifyClient

logger = utils.get_logger(__file__)


class Track(Base):
    def __init__(self, *,
                 tra_id: str,
                 tra_duration_ms: int,
                 tra_href: str,
                 tra_name: str,
                 tra_preview_url: str,
                 tra_uri: str,
                 alb_id: str = None):
        self.tra_id = tra_id
        self.tra_duration_ms = tra_duration_ms
        self.tra_href = tra_href
        self.tra_name = tra_name
        self.tra_preview_url = tra_preview_url
        self.tra_uri = tra_uri
        self.alb_id = alb_id
        self._artists = None

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

    def json(self) -> dict:
        return {"tra_id": self.tra_id,
                "tra_duration_ms": self.tra_duration_ms,
                "tra_href": self.tra_href,
                "tra_name": self.tra_name,
                "tra_preview_url": self.tra_preview_url,
                "tra_uri": self.tra_uri,
                "artists": self.artists,
                "album": self.album}

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
    def createSimplifiedRaw(cls, *, simpleRawTrack: spotify.hints.SimplifiedTrack, onExistRaiseError: bool = True) -> Track:
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
