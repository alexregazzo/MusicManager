from __future__ import annotations
import typing


class Album(typing.TypedDict):
    album_type: str
    artists: typing.List[Artist]
    available_markets: typing.List[str]
    copyrights: typing.List[Copyright]
    external_ids: ExternalId
    external_urls: ExternalUrl
    genres: typing.List[str]
    href: str
    id: str
    images: typing.List[Image]
    label: str
    name: str
    popularity: int
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestriction
    tracks: typing.List[SimplifiedTrack]
    type: str
    uri: str


class AlbumRestriction(typing.TypedDict):
    reason: str


class Artist(typing.TypedDict):
    external_urls: ExternalUrl
    followers: Followers
    genres: typing.List[str]
    href: str
    id: str
    images: typing.List[Image]
    name: str
    popularity: int
    type: str
    uri: str


class AudioFeatures(typing.TypedDict):
    acousticness: float
    analysis_url: str
    danceability: float
    duration_ms: int
    energy: float
    id: str
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: str
    speechiness: float
    tempo: float
    time_signature: int
    track_href: str
    type: str
    uri: str
    valence: float


class Category(typing.TypedDict):
    href: str
    icons: typing.List[Image]
    id: str
    name: str


class Context(typing.TypedDict):
    external_urls: ExternalUrl
    href: str
    type: str
    uri: str


class Copyright(typing.TypedDict):
    text: str
    type: str


class CurrentlyPlayingContext(typing.TypedDict):
    actions: Disallows
    context: Context or None
    currently_playing_type: str
    device: Device
    is_playing: bool
    item: Track or Episode or None
    progress_ms: int or None
    repeat_state: str
    shuffle_state: str
    timestamp: int


class CurrentlyPlaying(typing.TypedDict):
    context: Context or None
    currently_playing_type: str
    is_playing: bool
    item: Track or Episode or None
    progress_ms: int or None
    timestamp: int


class Cursor(typing.TypedDict):
    after: str
    # before: str


class CursorPaging(typing.TypedDict):
    cursors: Cursor
    href: str
    items: typing.List[object]
    limit: int
    next: str or None
    total: int


class Device(typing.TypedDict):
    id: str or None
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: str
    volume_percent: int or None


class Devices(typing.TypedDict):
    devices: typing.List[Device]


class Disallows(typing.TypedDict):
    interrupting_playback: bool
    pausing: bool
    resuming: bool
    seeking: bool
    skipping_next: bool
    skipping_prev: bool
    toggling_repeat_context: bool
    toggling_repeat_track: bool
    toggling_shuffle: bool
    transferring_playback: bool


class Episode(typing.TypedDict):
    audio_preview_url: str or None
    description: str
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    is_externally_hosted: bool
    is_playable: bool
    # language: str
    languages: typing.List[str]
    name: str
    release_date: str
    release_date_precision: str
    resume_point: ResumePoint
    show: SimplifiedShow
    type: str
    uri: str


class Error(typing.TypedDict):
    message: str
    status: int


class ExplicitContentSettings(typing.TypedDict):
    filter_enabled: bool
    filter_locked: bool


class ExternalId(typing.TypedDict):
    ean: str
    isrc: str
    upc: str


class ExternalUrl(typing.TypedDict):
    spotify: str


class Followers(typing.TypedDict):
    href: str or None
    total: int


class Image(typing.TypedDict):
    height: int or None
    url: str
    width: int or None


class LinkedTrack(typing.TypedDict):
    external_urls: ExternalUrl
    href: str
    id: str
    type: str
    uri: str


class Paging(typing.TypedDict):
    href: str
    items: typing.List[object]
    limit: int
    next: str or None
    offset: int
    previous: str or None
    total: int


class PlayHistory(typing.TypedDict):
    context: Context
    played_at: str
    track: SimplifiedTrack


class PlayerError(typing.TypedDict):
    message: str
    reason: str
    status: int


class Playlist(typing.TypedDict):
    collaborative: bool
    description: str or None
    external_urls: ExternalUrl
    followers: Followers
    href: str
    id: str
    images: typing.List[Image]
    name: str
    owner: PublicUser
    public: bool or None
    snapshot_id: str
    tracks: typing.List[PlaylistTrack] or None
    type: str
    uri: str


class PlaylistTrack(typing.TypedDict):
    added_at: str or None
    added_by: PublicUser or None
    is_local: bool
    track: Track or Episode


class PlaylistTracksRef(typing.TypedDict):
    href: str
    total: int


class PrivateUser(typing.TypedDict):
    country: str
    display_name: str or None
    email: str
    explicit_content: ExplicitContentSettings
    external_urls: ExternalUrl
    followers: Followers
    href: str
    id: str
    images: typing.List[Image]
    product: str
    type: str
    uri: str


class PublicUser(typing.TypedDict):
    display_name: str or None
    external_urls: ExternalUrl
    followers: Followers
    href: str
    id: str
    images: typing.List[Image]
    type: str
    uri: str


class RecommendationSeed(typing.TypedDict):
    afterFilteringSize: int
    afterRelinkingSize: int
    href: str or None
    id: str
    initialPoolSize: int
    type: str


class Recommendations(typing.TypedDict):
    seeds: typing.List[RecommendationSeed]
    tracks: typing.List[SimplifiedTrack]


class ResumePoint(typing.TypedDict):
    fully_played: bool
    resume_position_ms: int


class SavedAlbum(typing.TypedDict):
    added_at: str
    album: Album


class SavedShow(typing.TypedDict):
    added_at: str
    show: SimplifiedShow


class SavedTrack(typing.TypedDict):
    added_at: str
    track: Track


class Show(typing.TypedDict):
    available_markets: typing.List[str]
    copyrights: typing.List[Copyright]
    description: str
    episodes: typing.List[SimplifiedEpisode]
    explicit: bool
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    is_externally_hosted: bool or None
    languages: typing.List[str]
    media_type: str
    name: str
    publisher: str
    type: str
    uri: str


class SimplifiedAlbum(typing.TypedDict):
    album_group: str
    album_type: str
    artists: typing.List[SimplifiedArtist]
    available_markets: typing.List[str]
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    name: str
    release_date: str
    release_date_precision: str
    restrictions: AlbumRestriction
    type: str
    uri: str


class SimplifiedArtist(typing.TypedDict):
    external_urls: ExternalUrl
    href: str
    id: str
    name: str
    type: str
    uri: str


class SimplifiedEpisode(typing.TypedDict):
    audio_preview_url: str or None
    description: str
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    is_externally_hosted: bool
    is_playable: bool
    # language: str
    languages: typing.List[str]
    name: str
    release_date: str
    release_date_precision: str
    resume_point: ResumePoint
    type: str
    uri: str


class SimplifiedPlaylist(typing.TypedDict):
    collaborative: bool
    description: str or None
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    name: str
    owner: PublicUser
    public: bool or None
    snapshot_id: str
    tracks: PlaylistTracksRef or None
    type: str
    uri: str


class SimplifiedShow(typing.TypedDict):
    available_markets: typing.List[str]
    copyrights: typing.List[Copyright]
    description: str
    explicit: bool
    external_urls: ExternalUrl
    href: str
    id: str
    images: typing.List[Image]
    is_externally_hosted: bool or None
    languages: typing.List[str]
    media_type: str
    name: str
    publisher: str
    type: str
    uri: str


class SimplifiedTrack(typing.TypedDict):
    artists: typing.List[SimplifiedArtist]
    available_markets: typing.List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrl
    href: str
    id: str
    is_local: bool
    is_playable: bool
    linked_from: LinkedTrack
    name: str
    preview_url: str
    restrictions: TrackRestriction
    track_number: int
    type: str
    uri: str


class Track(typing.TypedDict):
    album: SimplifiedAlbum
    artists: typing.List[Artist]
    available_markets: typing.List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalId
    external_urls: ExternalUrl
    href: str
    id: str
    is_local: bool
    is_playable: bool
    # linked_from
    name: str
    popularity: int
    preview_url: str or None
    restrictions: TrackRestriction
    track_number: int
    type: str
    uri: str


class TrackRestriction(typing.TypedDict):
    reason: str


class TuneableTrack(typing.TypedDict):
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    popularity: float
    speechiness: float
    tempo: float
    time_signature: int
    valence: float
