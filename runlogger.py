from __future__ import annotations

import json
import traceback

import database.objects
import spotify.exceptions
import utils

logger = utils.get_logger(__file__)


class RunLogger:
    def __init__(self, *,
                 use_username: str,
                 run_type: str,
                 suppress_errors: bool = False,
                 message_on_success: str = None):
        self.run_type = run_type
        self.use_username = use_username
        self.suppress_errors = suppress_errors
        self.message_on_success = message_on_success

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        run_datetime = utils.get_current_timestamp_str()
        if exc_val is None:
            run = database.objects.Run.create(use_username=self.use_username,
                                              run_type=self.run_type,
                                              run_success=1,
                                              run_message=self.message_on_success,
                                              run_datetime=run_datetime)
            logger.debug(F"Run success, reference id: {run.run_id} with type {run.run_type}")
        else:
            runmessage = str(exc_val)
            if exc_type == spotify.exceptions.RevokeRefreshTokenError:
                database.objects.TokenSpotify.get(use_username=self.use_username).delete()
                logger.critical("Removing Spotify authentication due to invalid refresh token")
                runmessage = "Spotify token removed due to invalid refresh token //// " + runmessage

            run = database.objects.Run.create(use_username=self.use_username,
                                              run_type=self.run_type,
                                              run_success=0,
                                              run_message=runmessage,
                                              run_error_type=str(exc_type),
                                              run_traceback=json.dumps(traceback.format_tb(exc_tb)),
                                              run_datetime=run_datetime)
            logger.error(
                F"Run failed, {'ERROR SUPPRESSED' if self.suppress_errors else 'error not suppressed'}', reference id: {run.run_id} with type {run.run_type}")

        return self.suppress_errors
