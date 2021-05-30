from flask import Blueprint

import settings
from .website import website

web = Blueprint('web', __name__, template_folder=settings.TEMPLATES_FOLDER_PATH,
                static_folder=settings.STATIC_FOLDER_PATH)

web.register_blueprint(website)

# TODO: remake website
# TODO: move authentication website part to a separate file (and update its references on 'url_for')
