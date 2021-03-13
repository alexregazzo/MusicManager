import typing

import database.objects
import runlogger
import utils
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
    return
    # try:
    #     logger.info("Execution start of making playlists")
    #     tokens = database.objects.TokenSpotify.get_all()
    #
    #     for token in tokens:
    #         with database.objects.RunLogger(use_username=token.use_username,
    #                                         run_type=database.objects.Run.RUN_TYPE_MAKE_PLAYLIST,
    #                                         suppress_errors=True):
    #             su = SpotifyUser(token=token)
    #             # if token.tok_playlist_id is None:
    #             #     playlist_raw = su.create_playlist(playlist_name="MusicManager")
    #             #     token.update(tok_playlist_id=playlist_raw["id"])
    #             #
    #             # if not su.replace_user_playlist_tracks(token.tok_playlist_id,
    #             #                                        uris=make_playlist_order_from_history(database.objects.History.get_all(use_username=token.use_username))):
    #             #     raise Exception("Unknown error while making the playlist")
    #     logger.info("Execution end of making playlists")
    # except Exception as e:
    #     logger.exception(e)


def startServices():
    getEverybodyHistoryFromSpotify()
    # make_everybody_playlists()


if __name__ == "__main__":
    getEverybodyHistoryFromSpotify()
    make_everybody_playlists()
