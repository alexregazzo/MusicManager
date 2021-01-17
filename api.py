from flask import Blueprint, redirect, request, session, url_for, g, Response
from functools import wraps
import database.objects
import database.objects.exceptions
import utils
import settings
import json

apiv1 = Blueprint('apiv1', __name__, template_folder=settings.TEMPLATES_FOLDER_PATH, static_folder=settings.STATIC_FOLDER_PATH)
logger = utils.get_logger(__file__)


def api_ensure_response(f):
    @wraps(f)
    def request_wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if response is not None:
            return response
        return Response(response="Sem resposta", status=500)

    return request_wrapper


def api_authenticate(f):
    @api_ensure_response
    @wraps(f)
    def api_auth(*args, **kwargs):
        tokenapp_access_token = request.args.get('token', None)
        if tokenapp_access_token is None:
            return Response("Token não informado", status=401)
        try:
            tokenapp = database.objects.TokenApp.get(tok_access_token=tokenapp_access_token)
        except database.objects.exceptions.ObjectDoesNotExistError:
            return Response("Token inválido", status=401)
        else:
            if tokenapp.tok_active:
                return f(*args, tokenapp=tokenapp, **kwargs)
            else:
                return Response("Acesso negado", status=403)

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
            return Response("Formato ou valor do 'limit' incorreto", status=400)

    histories = list(database.objects.History.getAll(use_username=tokenapp.use_username, limit=limit, order_by=[("his_played_at", "DESC")]))
    return Response(json.dumps(histories, default=lambda x: x.json(), indent=2), status=200, mimetype="apiv1lication/json")


@apiv1.route("/api/v1/auth/user/signup", methods=["POST"])
@api_ensure_response
def api_v1_auth_user_signup():
    try:
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']
    except KeyError:
        return Response("Usuário e/ou senha não informado", status=400)

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
                user = database.objects.User.create(use_username=use_username, use_email=use_email, use_password_salt=use_password_salt, use_password=use_password)
            except Exception as e:
                logger.exception(e)
            else:
                try:
                    tokenapp = database.objects.TokenApp.create(use_username=user.use_username)
                except Exception as e:
                    logger.exception(e)
                else:
                    return Response(tokenapp.tok_access_token, status=201)
        else:
            return Response("Email já existe", status=400)
    except Exception as e:
        logger.exception(e)
    else:
        return Response("Usuário já existe", status=400)
    return Response("Erro desconhecido", status=400)


@apiv1.route("/api/v1/auth/token/get", methods=["POST"])
@api_ensure_response
def api_v1_auth_token_get():
    try:
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']
    except KeyError:
        return Response("Usuário e/ou senha não informado", status=400)

    try:
        user = database.objects.User.get(use_username=use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        return Response("Usuário ou senha incorreto", status=400)
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
                return Response(tokenapp.tok_access_token, status=200)
        else:
            return Response("Usuário ou senha incorreto", status=400)
    return Response("Erro desconhecido", status=400)


@apiv1.route("/api/v1/auth/spotify/token")
@api_authenticate
def api_v1_auth_spotify_token(tokenapp:database.objects.TokenApp):
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
        return Response("false", status=200)
    else:
        return Response("true", status=200)


@apiv1.route("/api/v1/auth/spotify/delete")
@api_authenticate
def api_v1_auth_spotify_delete(tokenapp: database.objects.TokenApp):
    try:
        tokenspotify = database.objects.TokenSpotify.get(use_username=tokenapp.use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        return Response("Token não encontrado", status=404)
    else:
        tokenspotify.delete()
        return Response(status=200)
