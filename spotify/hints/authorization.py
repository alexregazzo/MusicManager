from __future__ import annotations

import typing


class AuthenticationError(typing.TypedDict):
    error: str
    error_description: str


class RefreshTokenSuccessResponse(typing.TypedDict):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class ClientCredentialFlowSuccessResponse(typing.TypedDict):
    access_token: str
    token_type: str
    expires_in: int


class AuthorizationCodeFlowSuccess(typing.TypedDict):
    code: str
    state: str


class AuthorizationCodeFlowError(typing.TypedDict):
    error: str
    state: str
