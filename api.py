import json
from functools import wraps

from flask import Blueprint, redirect, request, session, url_for, g, Response

import data_statistics
import database.objects
import database.objects.exceptions
import settings
import track_scorer
import utils

apiv1 = Blueprint('apiv1', __name__, template_folder=settings.TEMPLATES_FOLDER_PATH,
                  static_folder=settings.STATIC_FOLDER_PATH)
logger = utils.get_logger(__file__)


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


@apiv1.route("/api/v1/history/get")
@api_authenticate
def api_v1_history_get(tokenapp: database.objects.TokenApp):
    limit = request.args.get("limit", None)
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 1:
                raise ValueError
        except ValueError:
            return makeAPIResponse(error_message="Formato ou valor do 'limit' incorreto")
    include_in_json = request.args.getlist("json")
    histories = list(database.objects.History.getAll(use_username=tokenapp.use_username, limit=limit,
                                                     order_by=[("his_played_at", "DESC")]))
    return makeAPIResponse(data=histories, include_in_json=include_in_json)


@apiv1.route("/api/v1/auth/user/signup", methods=["POST"])
@api_ensure_response
def api_v1_auth_user_signup():
    try:
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']
    except KeyError:
        return makeAPIResponse(error_message="Usuário e/ou senha não informado", user_displayable=True)

    use_email = request.form.get('user_email', None)
    if use_email == "":
        use_email = None
    use_password, use_password_salt = utils.hash_password(use_raw_password)

    try:
        database.objects.User.get(use_username=use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        try:
            if use_email is not None:
                database.objects.User.get(use_email=use_email)
            else:
                raise database.objects.exceptions.ObjectDoesNotExistError
        except database.objects.exceptions.ObjectDoesNotExistError:
            try:
                user = database.objects.User.create(use_username=use_username, use_email=use_email,
                                                    use_password_salt=use_password_salt, use_password=use_password)
            except Exception as e:
                logger.exception(e)
            else:
                try:
                    tokenapp = database.objects.TokenApp.create(use_username=user.use_username)
                except Exception as e:
                    logger.exception(e)
                else:
                    return makeAPIResponse(data=tokenapp.tok_access_token, status=201)
        else:
            return makeAPIResponse(error_message="Email já existe", user_displayable=True)
    except Exception as e:
        logger.exception(e)
    else:
        return makeAPIResponse(error_message="Usuário já existe", user_displayable=True)
    return makeAPIResponse(error_message="Erro desconhecido", user_displayable=True)


@apiv1.route("/api/v1/auth/token/get", methods=["POST"])
@api_ensure_response
def api_v1_auth_token_get():
    try:
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']
    except KeyError:
        return makeAPIResponse(error_message="Usuário e/ou senha não informado", user_displayable=True)

    try:
        user = database.objects.User.get(use_username=use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        return makeAPIResponse(error_message="Usuário ou senha incorreto", user_displayable=True)
    except Exception as e:
        logger.exception(e)
    else:
        use_password, _ = utils.hash_password(use_raw_password, user.use_password_salt)
        if user.use_password == use_password:
            try:
                tokenapp = database.objects.TokenApp.create(use_username=user.use_username)
            except Exception as e:
                logger.exception(e)
            else:
                return makeAPIResponse(data=tokenapp.tok_access_token, status=200)
        else:
            return makeAPIResponse(error_message="Usuário ou senha incorreto", user_displayable=True)
    return makeAPIResponse(error_message="Erro desconhecido", user_displayable=True)


@apiv1.route("/api/v1/auth/spotify/token")
@api_authenticate
def api_v1_auth_spotify_token(tokenapp: database.objects.TokenApp):
    user = database.objects.User.get(use_username=tokenapp.use_username)
    g.user = user
    session["use_username"] = user.use_username
    return redirect(url_for("spotify_authentication_acquire", fromapp="true"))


@apiv1.route("/api/v1/auth/spotify/get/exist")
@api_authenticate
def api_v1_auth_spotify_get_exist(tokenapp: database.objects.TokenApp):
    try:
        database.objects.TokenSpotify.get(use_username=tokenapp.use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        return makeAPIResponse(data=False)
    else:
        return makeAPIResponse(data=True)


@apiv1.route("/api/v1/auth/spotify/delete")
@api_authenticate
def api_v1_auth_spotify_delete(tokenapp: database.objects.TokenApp):
    try:
        tokenspotify = database.objects.TokenSpotify.get(use_username=tokenapp.use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        return makeAPIResponse(error_message="Token não encontrado", status=404, user_displayable=True)
    else:
        tokenspotify.delete()
        return makeAPIResponse(status=200)


@apiv1.route("/api/v1/stats/get")
@api_authenticate
def api_v1_stats_get(tokenapp: database.objects.TokenApp):
    timezone_offset_minutes = request.args.get("timezone_offset_minutes", None)
    if timezone_offset_minutes is None:
        return makeAPIResponse(error_message="'timezone_offset_minutes' não informado")

    if timezone_offset_minutes is not None:
        try:
            timezone_offset_minutes = int(timezone_offset_minutes)
        except ValueError:
            return makeAPIResponse(error_message="Formato do 'timezone_offset_minutes' incorreto deve ser int")

    response = {}
    include_in_json = request.args.getlist("json")
    queries = request.args.getlist("q")
    if not queries:
        return makeAPIResponse(error_message="Argumento 'q' não informado")
    if "weekdays" in queries:
        response["weekdays"] = data_statistics.weekdayStats(tokenapp, timezone_offset_minutes)
    if "hourly" in queries:
        response["hourly"] = data_statistics.hourlyStats(tokenapp, timezone_offset_minutes)

    return makeAPIResponse(data=response, include_in_json=include_in_json)


@apiv1.route("/api/v1/scores/get")
@api_authenticate
def api_v1_scores_get(tokenapp: database.objects.TokenApp):
    limit = request.args.get("limit", None)
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 1:
                raise ValueError
        except ValueError:
            return makeAPIResponse(error_message="Formato ou valor do 'limit' incorreto")

    timezone_offset_minutes = request.args.get("timezone_offset_minutes", None)
    if timezone_offset_minutes is None:
        return makeAPIResponse(error_message="'timezone_offset_minutes' não informado")

    include_in_json = request.args.getlist("json")

    if timezone_offset_minutes is not None:
        try:
            timezone_offset_minutes = int(timezone_offset_minutes)
        except ValueError:
            return makeAPIResponse(error_message="Formato do 'timezone_offset_minutes' incorreto deve ser int")

    return makeAPIResponse(
        data=track_scorer.wrap_all_scores(use_username=tokenapp.use_username, timezone_offset=timezone_offset_minutes,
                                          limit=limit),
        include_in_json=include_in_json)
