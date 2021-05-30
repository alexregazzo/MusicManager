from __future__ import annotations

import datetime
import hashlib
import logging
import logging.handlers
import os
import secrets
import sys
import typing

import requests

import settings


def containInListOfDict(search, array: list, dictKey) -> bool:
    for o in array:
        if o[dictKey] == search:
            return True
    return False


def parse_datetime(dt: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(dt, settings.DATETIME_STANDARD_FORMAT)
    except ValueError:
        return datetime.datetime.strptime(dt, settings.DATETIME_STANDARD_FORMAT2)


def get_current_timestamp() -> datetime.datetime:
    return datetime.datetime.utcnow()


def get_current_timestamp_str() -> str:
    return get_current_timestamp().strftime(settings.DATETIME_STANDARD_FORMAT)


def make_params(**params):
    return "&".join([F"""{k}={v}""" for k, v in params.items()])


def connected_to_internet():
    try:
        requests.get("https://google.com.br/")
        return True
    except:
        return False


def gen_salt(length: int = 20) -> str:
    return secrets.token_hex(length // 2)


def gen_token() -> str:
    return gen_salt(40)


def hash_password(password: str, salt: str = gen_salt()) -> typing.Tuple[str, str]:
    return hashlib.sha256(bytes(password + salt, 'utf8')).hexdigest(), salt


def get_logger(path: str, log_name: str = None, propagate: bool = False, always_debug: bool = True,
               max_size: typing.Union[int, None] = 5e6) -> logging.Logger:
    if log_name is None:
        log_name = os.path.splitext(os.path.relpath(path, settings.ROOT_DIRPATH).replace("\\", "_").replace("/", "_"))[
                       0] + ".log"
    logger_maker = logging.getLogger(log_name)
    if os.path.splitext(log_name)[1] != ".log":
        log_name += ".log"
    filepath = os.path.join(getLogRootPath(), log_name)
    logger_maker.setLevel(logging.DEBUG)
    if max_size is None:
        fh = logging.FileHandler(filepath, "w" if settings.DEVELOPMENT else "a", encoding='utf-8')
    else:
        fh = logging.handlers.RotatingFileHandler(filepath, "w" if settings.DEVELOPMENT else "a", maxBytes=max_size,
                                                  backupCount=5, encoding="UTF-8")
    fh.setLevel(logging.DEBUG if settings.DEVELOPMENT or always_debug else logging.INFO)
    fh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger_maker.addHandler(fh)
    # add global file
    logger_maker.addHandler(global_log_file)

    # add global info file
    logger_maker.addHandler(global_log_info_file)

    # log to console
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger_maker.addHandler(sh)
    if log_name == "database_database.log":
        sh.setLevel(logging.INFO)

    # CONSOLE ONLY INFO UP
    sh.setLevel(logging.INFO)

    logger_maker.propagate = propagate
    if settings.DEVELOPMENT:
        logger_maker.warning("DEVELOPMENT MODE")
    return logger_maker


def getLogRootPath() -> str:
    global LOG_ROOT_PATH
    if LOG_ROOT_PATH is None:
        index = 0
        path = os.path.join(settings.LOG_DIRPATH, "Run {index:03}")
        while os.path.exists(path.format(index=index)):
            index += 1
        path = path.format(index=index)
        os.makedirs(path, exist_ok=True)
        LOG_ROOT_PATH = path
    return LOG_ROOT_PATH


def getMultipleFromDict(dictionary: dict, keys: list, default: any = None):
    for key in keys:
        if key not in dictionary:
            return default
        dictionary = dictionary[key]
    return dictionary


CURRENT_DIRPATH = os.path.dirname(__file__)

LOG_ROOT_PATH = None

global_log_file = logging.handlers.RotatingFileHandler(os.path.join(getLogRootPath(), "global.log"),
                                                       "w" if settings.DEVELOPMENT else "a", maxBytes=int(5e6),
                                                       backupCount=5, encoding="UTF-8")
global_log_file.setLevel(logging.DEBUG)
global_log_file.setFormatter(logging.Formatter(settings.LOG_FORMAT))

global_log_info_file = logging.handlers.RotatingFileHandler(os.path.join(getLogRootPath(), "global_info.log"),
                                                            "w" if settings.DEVELOPMENT else "a", maxBytes=int(2e6),
                                                            backupCount=5, encoding="UTF-8")
global_log_info_file.setLevel(logging.INFO)
global_log_info_file.setFormatter(logging.Formatter(settings.LOG_FORMAT))

logger = get_logger(__file__)
CURRENT_DIRPATH = os.path.dirname(__file__)

if __name__ == "__main__":
    pass
