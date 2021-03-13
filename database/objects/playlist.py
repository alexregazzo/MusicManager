from __future__ import annotations

from .base import Base


class Playlist(Base):
    TYPE_SCORED_TRACKS = "scored_tracks"
    def __init__(self, *,
                 pla_id: int,
                 use_username: str,
                 pla_type: str,
                 pla_spotify_id: str = None):
        self.pla_id = pla_id
        self.use_username = use_username
        self.pla_type = pla_type
        self.pla_spotify_id = pla_spotify_id

    @classmethod
    def create(cls, *,
               use_username: str,
               pla_type: str,
               pla_spotify_id: str = None
               ) -> Playlist:
        ident = cls._insert(use_username=use_username,
                            pla_type=pla_type,
                            pla_spotify_id=pla_spotify_id)
        return cls.get(pla_id=ident)
