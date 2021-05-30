import atexit
import datetime
import random

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

import api
import services
import settings
import utils
import web

logger = utils.get_logger(__file__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=services.startServices, trigger="interval", seconds=60)
services.startServices()
app = Flask(__name__, template_folder=settings.TEMPLATES_FOLDER_PATH, static_folder=settings.STATIC_FOLDER_PATH)
app.secret_key = utils.gen_salt(random.randint(20, 60))

app.register_blueprint(api.apis)
app.register_blueprint(web.web)


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
