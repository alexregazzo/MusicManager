class KnownError(Exception):
    pass


# ---------------------------------------------------------------------------------------------------- #


class KnownWebAppError(KnownError):
    pass


class WrongNewPasswordMatchError(KnownWebAppError):
    def __init__(self):
        super().__init__("Senhas não coincidem")


class WrongPasswordError(KnownWebAppError):
    def __init__(self):
        super().__init__("Senha incorreta!")


class UsernameAlreadyExistsError(KnownWebAppError):
    def __init__(self):
        super().__init__("Esse nome de usuário já existe!")
