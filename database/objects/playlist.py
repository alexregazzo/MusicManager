from __future__ import annotations

from .base import Base


class Playlist(Base):
    def __init__(self, *,
                 pla_id: int,
                 use_username: str,
                 pro_id: int,
                 pla_spotify_id: str = None):
        self.pla_id = pla_id
        self.use_username = use_username
        self.pro_id = pro_id
        self.pla_spotify_id = pla_spotify_id

    @classmethod
    def create(cls, *,
               use_username: str,
               pro_id: int,
               pla_spotify_id: str = None
               ) -> Playlist:
        ident = cls._insert(use_username=use_username,
                            pro_id=pro_id,
                            pla_spotify_id=pla_spotify_id)
        return cls.get(pro_id=ident)
