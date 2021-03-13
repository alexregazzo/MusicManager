import atexit
import datetime
import random
from functools import wraps

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, redirect, request, session, url_for, render_template, g

import api
import database.objects
import database.objects.exceptions
import services
import settings
import spotify.utils
import utils
from exceptions import *

scheduler = BackgroundScheduler()
scheduler.add_job(func=services.startServices, trigger="interval", seconds=60)
services.startServices()
app = Flask(__name__, template_folder=settings.TEMPLATES_FOLDER_PATH, static_folder=settings.STATIC_FOLDER_PATH)
app.register_blueprint(api.apiv1)

app.secret_key = utils.gen_salt(random.randint(20, 60))
# app.secret_key = "heythere"
logger = utils.get_logger(__file__)

AUTHENTICATION_LIST = []


def create_spotify_auth_process(use_username: str, use_state: str, fromapp: bool = False) -> None:
    global AUTHENTICATION_LIST
    new_auth_user_process = {"use_username": use_username, "use_state": use_state,
                             "time": utils.get_current_timestamp(), "fromapp": fromapp}
    logger.debug(F"Adding auth process: {new_auth_user_process}")
    AUTHENTICATION_LIST.append(new_auth_user_process)


def exist_spotify_auth_process(use_username: str, use_state: str) -> tuple:
    global AUTHENTICATION_LIST
    logger.debug(F"Looking for: {use_username} --> {use_state}")
    for auth_process in AUTHENTICATION_LIST[:]:
        if utils.get_current_timestamp() - auth_process["time"] > datetime.timedelta(
                seconds=settings.SPOTIFY_AUTH_TIMESPAN):
            logger.debug(F"Expired: {auth_process}")
            AUTHENTICATION_LIST.remove(auth_process)
            continue
        if auth_process["use_username"] == use_username and auth_process["use_state"] == use_state:
            logger.debug("Found!")

            return True, auth_process["fromapp"]
    logger.debug("Not found!")
    return False, False


def authenticate(f):
    @wraps(f)
    def auth_wrapper(*args, **kwargs):
        if "use_username" in session:
            try:
                g.user = database.objects.User.get(use_username=session["use_username"])
            except database.objects.exceptions.ObjectDoesNotExistError:
                logger.warning(F"User not found: {session['use_username']}")
            except Exception as e:
                logger.exception(e)
            else:
                return f(*args, **kwargs)
        return redirect(url_for("page_login"))

    return auth_wrapper


def unauthenticate(f):
    @wraps(f)
    def unauth_wrapper(*args, **kwargs):
        session.pop("use_username", None)
        g.user = None
        return f(*args, **kwargs)

    return unauth_wrapper


@app.route("/logout")
@unauthenticate
def logout():
    return redirect(url_for("page_login"))


@app.route("/")
def page_inicio():
    return redirect(url_for('page_login'))


@app.route("/login", methods=["GET", "POST"])
@unauthenticate
def page_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']

        try:
            user = database.objects.User.get(use_username=use_username)
        except database.objects.exceptions.ObjectDoesNotExistError:
            return render_template("login.html", error_message="Nome de usuário ou senha incorreta.")
        except Exception as e:
            logger.exception(e)
            return render_template("login.html",
                                   error_message="Um erro desconhecido ocorreu, por favor tente novamente mais tarde ou entre em contato.")
        else:
            use_password, _ = utils.hash_password(use_raw_password, user.use_password_salt)
            logger.debug(user)
            logger.debug(use_password)
            if user.use_password == use_password:
                logger.debug(f"User logged in: {user.use_username}")
                g.user = user
                session["use_username"] = user.use_username
                return redirect(url_for('page_overview'))


@app.route("/signup", methods=["GET", "POST"])
@unauthenticate
def page_signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        use_username = request.form['user_username']
        use_raw_password = request.form['user_password']
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
                    return render_template("signup.html",
                                           error_message="Erro ao criar usuário. Tente novamente mais tarde ou entre em contato.")
                else:
                    g.user = user
                    session["use_username"] = user.use_username
                    return redirect(url_for('page_overview'))
            else:
                return render_template("signup.html", error_message="Email já existe!")
        except Exception as e:
            logger.exception(e)
            return render_template("signup.html",
                                   error_message="Um erro desconhecido ocorreu, por favor tente novamente mais tarde ou entre em contato.")
        else:
            return render_template("signup.html", error_message="Nome de usuário já existe.")


@app.route("/logs")
@authenticate
def page_logs():
    history_runs = database.objects.Run.getAll(use_username=g.user.use_username,
                                               run_type=database.objects.Run.TYPE_GET_HISTORY,
                                               order_by=[("run_datetime", "DESC")], limit=10)

    make_playlist_runs = database.objects.Run.getAll(use_username=g.user.use_username,
                                                     run_type=database.objects.Run.TYPE_MAKE_PLAYLIST,
                                                     order_by=[("run_datetime", "DESC")], limit=10)

    return render_template("logs.html", history_runs=history_runs, make_playlist_runs=make_playlist_runs)


@app.route("/overview")
@authenticate
def page_overview():
    try:
        token = database.objects.TokenSpotify.get(use_username=g.user.use_username)
    except database.objects.exceptions.ObjectDoesNotExistError:
        token = None

    histories = database.objects.History.getAll(use_username=g.user.use_username, limit=10,
                                                order_by=[("his_played_at", "DESC")])

    return render_template("overview.html", **request.args, token=token, user=g.user, histories=histories)


@app.route("/settings", methods=["GET", "POST"])
@authenticate
def page_settings():
    if request.method == "GET":
        return render_template("settings.html", **request.args, user=g.user)
    else:
        try:
            updating = request.form.get("user_update_type")
            if updating == "username_and_email":
                user = g.user

                user_username = request.form.get("user_username")
                user_email = request.form.get("user_email", None)
                if user_email == "":
                    user_email = None
                user_password = request.form.get("user_password")

                if not user.check_password(user_password):
                    raise WrongPasswordError()

                try:
                    database.objects.User.get(use_username=user_username)
                except database.objects.exceptions.ObjectDoesNotExistError:
                    pass
                else:
                    raise UsernameAlreadyExistsError()

                user.update(use_email=user_email, use_username=user_username)

            elif updating == "new_password":
                user = g.user
                old_pass = request.form.get("user_password")
                new_pass = request.form.get("user_new_password")
                new_pass_confirm = request.form.get("user_new_password_confirm")
                if new_pass != new_pass_confirm:
                    raise WrongNewPasswordMatchError()
                if not user.check_password(old_pass):
                    raise WrongPasswordError()
                use_password, use_password_salt = utils.hash_password(new_pass)
                user.update(use_password=use_password, use_password_salt=use_password_salt)

                return render_template("settings.html", success_message="Senha atualizada com sucesso!", user=g.user)
        except KnownError as e:
            return render_template("settings.html", error_message=str(e), user=g.user)
        except Exception as e:
            logger.exception(e)
            return render_template("settings.html", error_message="Um erro desconhecido ocorreu", user=g.user)


@app.route('/spotify/authentication/acquire')
@authenticate
def spotify_authentication_acquire():
    fromapp = "fromapp" in request.args
    try:
        state = utils.gen_salt(random.randint(10, 50))
        use_username = g.user.use_username
        create_spotify_auth_process(use_username, state, fromapp=fromapp)
        return redirect(spotify.utils.makeSignInURL(
            client_id=spotify.CLIENT_ID,
            redirect_uri=url_for("spotify_authentication_response", _external=True),
            state=state,
            scope=spotify.SCOPES,
            show_dialog=settings.DEVELOPMENT))
    except Exception as e:
        logger.exception(e)
    return redirect(url_for("page_overview", error_message="Um erro ocorreu."))


@app.route("/spotify/authentication/response")
@authenticate
def spotify_authentication_response():
    use_username = g.user.use_username
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    exists, fromapp = exist_spotify_auth_process(use_username, state)
    if exists:
        if error is None:
            logger.debug("No error")
            requested_time_str = utils.get_current_timestamp_str()
            req = requests.post("https://accounts.spotify.com/api/token",
                                data={"grant_type": "authorization_code",
                                      "redirect_uri": url_for("spotify_authentication_response", _external=True),
                                      "client_id": spotify.CLIENT_ID,
                                      "client_secret": spotify.CLIENT_SECRET,
                                      "code": code})

            if req.ok:
                data = req.json()
                try:
                    database.objects.TokenSpotify.createRaw(rawToken=data, use_username=use_username,
                                                            requested_time_str=requested_time_str,
                                                            onExistRaiseError=False)
                except Exception as e:
                    logger.exception(e)
                else:
                    if fromapp:
                        return render_template("app_spotify_authenticated.html")
                    return redirect(url_for("page_overview", success_message="Conta vinculada com sucesso!"))
            else:
                logger.debug(F"Error executing code: {req.status_code}")
        else:
            if error == "access_denied":
                logger.warning("Acess denied")
            else:
                logger.warning(error)
    else:
        logger.warning("Auth process not found")
    if fromapp:
        return render_template("app_spotify_not_authenticated.html")
    return redirect(url_for("page_overview", error_message="Um erro ocorreu."))


@app.template_filter('formatdate')
def _jinja2_filter_datetime(date: str) -> str:
    return (utils.parse_datetime(date) - datetime.timedelta(hours=3)).strftime(settings.DATETIME_STANDARD_SHOW_FORMAT)


scheduler.start()
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    if settings.DEVELOPMENT:
        app.run(host="0.0.0.0",
                port=5003, debug=True)
    else:
        app.run(host="0.0.0.0",
                port=8765)
