class SpotifyError(Exception):
    pass


class RequestError(SpotifyError):
    pass


class RevokeRefreshTokenError(SpotifyError):
    pass
