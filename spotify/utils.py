import spotify


def makeSignInURL(*, client_id: str, redirect_uri: str, state: str, scope: str, show_dialog: bool = False) -> str:
    return F"{spotify.AUTHORIZATION_CODE_FLOW_ENDPOINT[1]}?" \
           F"client_id={client_id}&" \
           F"response_type=code&" \
           F"redirect_uri={redirect_uri}&" \
           F"state={state}&" \
           F"scope={scope}&" \
           F"show_dialog={'true' if show_dialog else 'false'}"
