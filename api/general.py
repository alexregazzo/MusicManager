import json
from functools import wraps

from flask import request, Response

import database.objects
import database.objects.exceptions


def makeAPIResponse(*, data: any = None, status: int = None, error_message: str = None, user_displayable: bool = False,
                    include_in_json: list = None):
    if include_in_json is None:
        include_in_json = []
    if status is None:
        if error_message is None:
            if data is not None:
                status = 200
            else:
                status = 400
        else:
            status = 400

    if status >= 300 and error_message is None:
        error_message = "Erro desconhecido"

    return Response(json.dumps({
        "user_displayable": user_displayable,
        "success": status < 300,
        "status": status,
        "data": data,
        "error_message": error_message}, default=lambda x: x.json(*include_in_json), indent=2, ensure_ascii=False
    ), status=status, mimetype="application/json")


def api_ensure_response(f):
    @wraps(f)
    def request_wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            if response is not None:
                return response
            return makeAPIResponse(error_message="Sem resposta da função", status=500)
        except Exception as e:
            print(e)
            return makeAPIResponse(error_message="Erro interno de servidor", status=500, user_displayable=True)

    return request_wrapper


def api_authenticate(f):
    @api_ensure_response
    @wraps(f)
    def api_auth(*args, **kwargs):
        tokenapp_access_token = request.args.get('token', None)
        if tokenapp_access_token is None:
            return makeAPIResponse(error_message="Token não informado", status=401, user_displayable=True)
        try:
            tokenapp = database.objects.TokenApp.get(tok_access_token=tokenapp_access_token)
        except database.objects.exceptions.ObjectDoesNotExistError:
            return makeAPIResponse(error_message="Token inválido", status=401, user_displayable=True)
        else:
            if tokenapp.tok_active:
                return f(*args, tokenapp=tokenapp, **kwargs)
            else:
                return makeAPIResponse(error_message="Acesso negado", status=403, user_displayable=True)

    return api_auth
