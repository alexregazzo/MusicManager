import json

import settings

with open(settings.CONFIGS_PATH, 'r') as f:
    CONFIGS = json.load(f)

CLIENT_ID = CONFIGS["spotify"]["client_id"]
CLIENT_SECRET = CONFIGS["spotify"]["client_secret"]
SCOPES = " ".join(CONFIGS["spotify"]["scopes"])

GET_MULTIPLE_ALBUMS_ENDPOINT = "GET", "https://api.spotify.com/v1/albums"
GET_SEVERAL_TRACKS_ENDPOINT = "GET", "https://api.spotify.com/v1/tracks"
CLIENT_CREDENTIALS_FLOW_ENDOPOINT = "POST", "https://accounts.spotify.com/api/token"
AUTHORIZATION_CODE_FLOW_ENDPOINT = "GET", "https://accounts.spotify.com/authorize"
REFRESH_TOKEN_ENDPOINT = "POST", "https://accounts.spotify.com/api/token"
CURRENT_USER_RECENTLY_PLAYED_TRACKS_ENDPOINT = "GET", "https://api.spotify.com/v1/me/player/recently-played"
CURRENT_USER_PROFILE_ENDPOINT = "GET", "https://api.spotify.com/v1/me"
CREATE_PLAYLIST_ENDPOINT = "POST", "https://api.spotify.com/v1/me/playlists"
FOLLOW_PLAYLIST_ENDPOINT = "PUT", "https://api.spotify.com/v1/playlists/{playlist_id}/followers"
CHECK_IF_USERS_FOLLOW_PLAYLIST_ENDPOINT = "GET", "https://api.spotify.com/v1/playlists/{playlist_id}/followers/contains"
REORDER_OR_REPLACE_PLAYLIST_ITEMS_ENDPOINT = "PUT", "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
CHANGE_DETAILS_ENDPOINT = "PUT", "https://api.spotify.com/v1/playlists/{playlist_id}"
GET_PLAYLIST_ENDPOINT = "GET", "https://api.spotify.com/v1/playlists/{playlist_id}"
GET_CURRENT_USER_PLAYLISTS = "GET", "https://api.spotify.com/v1/me/playlists"
GET_ALBUM_ENDPOINT = "GET", "https://api.spotify.com/v1/albums/{id}"
GET_TRACK_ENDPOINT = "GET", "https://api.spotify.com/v1/tracks/{id}"
