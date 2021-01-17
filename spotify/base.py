from __future__ import annotations
import requests
import utils
import spotify.exceptions

logger = utils.get_logger(__file__)


class SpotifyBase:

    @classmethod
    def makeRequest(cls, method, url, params: dict = None, data: dict = None, headers: dict = None,
                    ignore_text_response: bool = False) -> bool or dict or list or None:

        response = requests.request(url=url, method=method, data=data, params=params, headers=headers)
        if ignore_text_response:
            return response.ok

        data = response.json()

        if not response.ok:
            logger.warning(f"Problem ocurred during request to spotify {response.status_code} {data}")
            if data["error"]["message"] == "Permissions missing":
                logger.debug("Not allowed")
            raise spotify.exceptions.RequestError(data)

        return data
