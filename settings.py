import os
import platform

DEVELOPMENT = platform.system() == "Windows"
ROOT_DIRPATH = os.path.dirname(__file__)
LOG_DIRPATH = os.path.join(ROOT_DIRPATH, "log")

KEYS_PATH = os.path.join(ROOT_DIRPATH, "keys.json")
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(threadName)s :: %(name)s %(lineno)d :: %(message)s"
DATETIME_STANDARD_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATETIME_STANDARD_FORMAT2 = "%Y-%m-%dT%H:%M:%SZ"
DATETIME_STANDARD_SHOW_FORMAT = "%d/%m/%Y %H:%M:%S"

TEMPLATES_FOLDER_PATH = os.path.join(ROOT_DIRPATH, "templates")
STATIC_FOLDER_PATH = os.path.join(ROOT_DIRPATH, "static")

SPOTIFY_AUTH_TIMESPAN = 600

CONFIGS_PATH = os.path.join(ROOT_DIRPATH, "configs.json")

os.makedirs(LOG_DIRPATH, exist_ok=True)
LOG_OUTPUT_TO_CONSOLE = DEVELOPMENT
