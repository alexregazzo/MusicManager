from __future__ import annotations

import json
import typing

import database.objects
import spotify
import spotify.hints
import utils
from .base import SpotifyBase

logger = utils.get_logger(__file__)


class SpotifyUser(SpotifyBase):
    def __init__(self, *, token: database.objects.TokenSpotify):
        self.token = token

    def request(self,
                method: str,
                url: str,
                *,
                params: dict = None,
                data: dict = None,
                headers: dict = None,
                ignore_text_response: bool = False) -> bool or dict or list or None:
        self.checkToken()

        nheaders = {'Authorization': f'Bearer {self.token.tok_access_token}'}
        nheaders.update(headers if headers is not None else {})
        return self.makeRequest(url=url, method=method, params=params, data=data, headers=nheaders,
                                ignore_text_response=ignore_text_response)

    def refreshToken(self) -> None:
        data = self.makeRequest(*spotify.REFRESH_TOKEN_ENDPOINT,
                                data={
                                    "grant_type": "refresh_token",
                                    "client_id": spotify.CLIENT_ID,
                                    "client_secret": spotify.CLIENT_SECRET,
                                    "refresh_token": self.token.tok_refresh_token
                                })
        self.token.update(
            tok_access_token=data["access_token"],
            tok_token_type=data["token_type"],
            tok_expires_in=data["expires_in"],
            tok_scope=data["scope"],
            tok_last_updated_datetime=utils.get_current_timestamp_str())

    def checkToken(self) -> bool:
        if self.token.expired:
            if not self.refreshToken():
                return False
        return True

    def next(self, dados: typing.Dict) -> list or None:
        return self.request("GET", dados["next"])

    def getCurrentUserRecentlyPlayedTracks(self) -> spotify.hints.CursorPagingRecentlyPlayedTracksResponse:
        return self.request(*spotify.CURRENT_USER_RECENTLY_PLAYED_TRACKS_ENDPOINT, params={"limit": 50})

    def getCurrentUserProfile(self) -> spotify.hints.PrivateUser:
        return self.request(*spotify.CURRENT_USER_PROFILE_ENDPOINT)

    def getCurrentUserPlaylists(self) -> spotify.hints.PagingCurrentUserPlaylistsResponse:
        return self.request(*spotify.GET_CURRENT_USER_PLAYLISTS, params={"limit": 50})

    def getPlaylist(self, playlist_id: str) -> spotify.hints.Playlist:
        return self.request(spotify.GET_PLAYLIST_ENDPOINT[0],
                            spotify.GET_PLAYLIST_ENDPOINT[1].format(playlist_id=playlist_id))

    def getSavedTracks(self):
        return self.request(spotify.GET_USER_SAVED_TRACKS_ENDPOINT[0], spotify.GET_USER_SAVED_TRACKS_ENDPOINT[1], params={"limit": 50})

    def changePlaylistDetails(self, playlist_id: str, name: str = None, public: bool = None, collaborative: bool = None,
                              description: str = None) -> bool:
        data = {}
        if name is not None:
            data["name"] = name
        if public is not None:
            data["public"] = public
        if collaborative is not None:
            data["collaborative"] = collaborative
        if description is not None:
            data["description"] = description
        return self.request(
            spotify.CHANGE_DETAILS_ENDPOINT[0],
            spotify.CHANGE_DETAILS_ENDPOINT[1].format(playlist_id=playlist_id),
            data=json.dumps(data), ignore_text_response=True)

    def reorderOrReplacePlaylistItems(self, playlist_id: str, uris: typing.List[str]) -> bool:
        return all([self.request(
            spotify.REORDER_OR_REPLACE_PLAYLIST_ITEMS_ENDPOINT[0],
            spotify.REORDER_OR_REPLACE_PLAYLIST_ITEMS_ENDPOINT[1].format(playlist_id=playlist_id),
            params={"uris": ",".join(uris[i:i + 100])},
            ignore_text_response=True) for i in range(0, len(uris), 100)])

    def addToPlaylist(self, playlist_id: str, uris: typing.List[str], position: int = None) -> bool:
        extraParams = {}
        if position is not None:
            extraParams["position"] = position
        return all([self.request(
            spotify.ADD_TO_PLAYLIST_ENDPOINT[0],
            spotify.ADD_TO_PLAYLIST_ENDPOINT[1].format(playlist_id=playlist_id),
            params={"uris": ",".join(uris[i:i + 50]), **extraParams},
            ignore_text_response=True) for i in range(0, len(uris), 50)])

    def checkIfUsersFollowPlaylist(self, playlist_id: str, users: typing.List[str]) -> typing.List[bool]:
        results = []
        for i in range(0, len(users), 5):
            results.extend(self.request(
                spotify.CHECK_IF_USERS_FOLLOW_PLAYLIST_ENDPOINT[0],
                spotify.CHECK_IF_USERS_FOLLOW_PLAYLIST_ENDPOINT[1].format(playlist_id=playlist_id),
                params={"ids": ",".join(users[i:i + 5])}))
        return results

    def followPlaylist(self, playlist_id: str, public: bool = True) -> bool:
        return self.request(
            spotify.FOLLOW_PLAYLIST_ENDPOINT[0],
            spotify.FOLLOW_PLAYLIST_ENDPOINT[1].format(playlist_id=playlist_id),
            data=json.dumps({"public": public}),
            ignore_text_response=True)

    def createPlaylist(self, playlist_name: str, public: bool = True, collaborative: bool = False,
                       description: str = None) -> spotify.hints.Playlist:
        return self.request(*spotify.CREATE_PLAYLIST_ENDPOINT,
                            data=json.dumps({
                                "name": playlist_name,
                                "public": public,
                                "collaborative": collaborative,
                                "description": description
                            }))
