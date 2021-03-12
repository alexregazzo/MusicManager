from __future__ import annotations
import spotify
import spotify.hints
import typing
import utils
import datetime
from .base import SpotifyBase

logger = utils.get_logger(__file__)


class SpotifyClient(SpotifyBase):
    TOKEN = None
    TOKEN_EXPIRATION_DATETIME = None

    @classmethod
    def isTokenExpired(cls) -> bool:
        return cls.TOKEN_EXPIRATION_DATETIME is None or datetime.datetime.now() > cls.TOKEN_EXPIRATION_DATETIME

    @classmethod
    def getClientCredentialsFlow(cls) -> spotify.hints.ClientCredentialFlowSuccessResponse:
        return cls.makeRequest(*spotify.CLIENT_CREDENTIALS_FLOW_ENDOPOINT, data={
            "grant_type": "client_credentials",
            "client_id": spotify.CLIENT_ID,
            "client_secret": spotify.CLIENT_SECRET
        })

    @classmethod
    def request(cls,
                method: str,
                url: str,
                *,
                params: dict = None,
                data: dict = None,
                headers: dict = None,
                ignore_text_response: bool = False
                ) -> bool or dict or list or None:
        if cls.isTokenExpired():
            if not cls.getToken():
                return None
        nheaders = {'Authorization': f'Bearer {cls.TOKEN}'}
        nheaders.update(headers if headers is not None else {})
        return cls.makeRequest(url=url, method=method, params=params, data=data, headers=nheaders,
                               ignore_text_response=ignore_text_response)

    @classmethod
    def getToken(cls) -> bool:
        data = cls.getClientCredentialsFlow()
        if data is None:
            return False
        cls.TOKEN = data["access_token"]
        cls.TOKEN_EXPIRATION_DATETIME = datetime.datetime.now() + datetime.timedelta(seconds=data["expires_in"])
        return True

    @classmethod
    def getSeveralTracks(cls, ids=typing.List[str]) -> spotify.hints.GetSeveralTracksResponse:
        assert len(ids) <= 50
        return cls.request(*spotify.GET_SEVERAL_TRACKS_ENDPOINT, params={"ids": ",".join(ids)})

    @classmethod
    def getMultipleAlbums(cls, ids=typing.List[str]) -> spotify.hints.GetMultipleAlbumsResponse:
        assert len(ids) <= 50
        return cls.request(*spotify.GET_MULTIPLE_ALBUMS_ENDPOINT, params={"ids": ",".join(ids)})

    @classmethod
    def getAlbum(cls, id: str) -> spotify.hints.Album:
        return cls.request(spotify.GET_ALBUM_ENDPOINT[0], spotify.GET_ALBUM_ENDPOINT[1].format(id=id))

    @classmethod
    def getTrack(cls, id: str) -> spotify.hints.Track:
        return cls.request(spotify.GET_TRACK_ENDPOINT[0], spotify.GET_TRACK_ENDPOINT[1].format(id=id))
