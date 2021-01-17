from __future__ import annotations
import typing
from .objects import Track, Album, Cursor, PlayHistory, SimplifiedPlaylist


class GetSeveralTracksResponse(typing.TypedDict):
    tracks: typing.List[Track or None]


class GetMultipleAlbumsResponse(typing.TypedDict):
    albums: typing.List[Album or None]


class CursorPagingRecentlyPlayedTracksResponse(typing.TypedDict):
    cursors: Cursor
    href: str
    items: typing.List[PlayHistory]
    limit: int
    next: str or None
    total: int


class PagingCurrentUserPlaylistsResponse(typing.TypedDict):
    href: str
    items: typing.List[SimplifiedPlaylist]
    limit: int
    next: str or None
    offset: int
    previous: str or None
    total: int
