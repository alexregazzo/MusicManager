from .baseException import KnownError


class KnownServiceError(KnownError):
    pass


class CouldNotMakePlaylistError(KnownServiceError):
    def __init__(self):
        super().__init__("Esse nome de usuário já existe!")
