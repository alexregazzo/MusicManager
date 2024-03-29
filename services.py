import datetime
import typing

import analytics.scorer
import database.objects
import database.objects.exceptions
import runlogger
import settings
import utils
from exceptions.serviceException import *
from spotify import SpotifyUser

logger = utils.get_logger(__file__)


def getEverybodyHistoryFromSpotify() -> None:
    try:
        logger.info("Execution start of history collection")
        tokens = database.objects.TokenSpotify.getAll()
        for token in tokens:
            with runlogger.RunLogger(use_username=token.use_username,
                                     run_type=database.objects.Run.TYPE_GET_HISTORY,
                                     suppress_errors=True):
                su = SpotifyUser(token=token)
                raw_histories = su.getCurrentUserRecentlyPlayedTracks()
                if raw_histories is not None:
                    database.objects.History.createMultipleRaw(use_username=token.use_username,
                                                               raw_histories=raw_histories["items"],
                                                               onExistRaiseError=False)
        logger.info("Execution end of history collection")
    except Exception as e:
        logger.exception(e)


def make_playlist_order_from_history(histories: typing.List[database.objects.History]) -> typing.List[str]:
    return [history.track.tra_uri for history in histories]


def make_everybody_playlists() -> None:
    try:
        scoredPlaylistMessage = utils.getMultipleFromDict(settings.SPOTIFY_DEFINITIONS, ["playlists", "scored_tracks", "description"])
        logger.info("Execution start of making playlists")

        tokens = database.objects.TokenSpotify.getAll()
        for token in tokens:
            with runlogger.RunLogger(use_username=token.use_username,
                                     run_type=database.objects.Run.TYPE_MAKE_PLAYLIST,
                                     suppress_errors=True):

                # Make sure everyone has a playlist of scored tracks
                playlist = database.objects.Playlist.getOrCreate(use_username=token.use_username,
                                                                 pla_type=database.objects.Playlist.TYPE_SCORED_TRACKS)

                su = SpotifyUser(token=token)
                # Create playlist if not exists
                if playlist.pla_spotify_id is None:
                    playlist_response = su.createPlaylist(playlist_name="MM Scored Tracks",
                                                          description=scoredPlaylistMessage + " Atualização em breve...")
                    playlist.update(pla_spotify_id=playlist_response["id"])

                weights = {}
                if playlist.pro_id is not None:
                    profile = database.objects.Profile.get(pro_id=playlist.pro_id)
                    weights = profile.toGenDict()
                scored_tracks = analytics.scorer.wrap_all_scores(token.use_username, **weights)
                if not su.reorderOrReplacePlaylistItems(playlist.pla_spotify_id,
                                                        uris=list(map(lambda x: x["track"].tra_uri, scored_tracks[:50]))):
                    raise CouldNotMakePlaylistError()
                su.changePlaylistDetails(playlist_id=playlist.pla_spotify_id,
                                         description=scoredPlaylistMessage + " Ultima atualização em: " + (
                                                 utils.get_current_timestamp() - datetime.timedelta(hours=3)).strftime(
                                             settings.DATETIME_STANDARD_SHOW_FORMAT) + " GMT-3 Pesos: " + str(weights))

        logger.info("Execution end of making playlists")
    except Exception as e:
        logger.exception(e)


def startServices():
    getEverybodyHistoryFromSpotify()
    make_everybody_playlists()


if __name__ == "__main__":
    # getEverybodyHistoryFromSpotify()
    make_everybody_playlists()
