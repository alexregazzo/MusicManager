from flask import Blueprint

import settings
from .v1 import apiv1

apis = Blueprint('apis', __name__, template_folder=settings.TEMPLATES_FOLDER_PATH,
                 static_folder=settings.STATIC_FOLDER_PATH, url_prefix="/api")

apis.register_blueprint(apiv1)
