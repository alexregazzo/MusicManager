# from typing import TypedDict
# import typing
#
#
# class TrackObject(TypedDict):
#     pass
#
#
# class RawAlbum(TypedDict):
#     pass
#
#
# class RawArtist(TypedDict):
#     external_urls: dict
#     href: str
#     id: str
#     name: str
#     type: str
#     uri: str
#
#
# class RawTrack(TypedDict):
#     album: RawAlbum
#     artists: typing.List[RawArtist]
#     available_markets: typing.List[str]
#     disc_number: int
#     duration_ms: int
#     explicit: bool
#     external_ids: dict
#     external_urls: dict
#     href: str
#     id: str
#     is_local: bool
#     name: str
#     popularity: int
#     preview_url: str
#     track_number: int
#     type: str
#     uri: str
#
#
# class RawHistory(TypedDict):
#     track: RawTrack
#     played_at: str
#     context: dict
#
#
# class RawToken(TypedDict):
#     access_token: str
#     token_type: str
#     scope: str
#     expires_in: int
#     refresh_token: str
#
#
# class RawImage(TypedDict):
#     width: int or None
#     height: int or None
#     url: str
#
#
# class RawUser(TypedDict):
#     display_name: str
#     external_urls: dict
#     followers: str
#     href: str
#     id: str
#     images: typing.List[RawUserPlaylists]
#     type: str
#     uri: str
#
#
# class RawUserPlaylists(TypedDict):
#     pass
