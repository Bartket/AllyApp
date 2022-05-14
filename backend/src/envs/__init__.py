from envs.app import AppEnv
from envs.db import DBEnv
from envs.logger import LoggerEnv


class _Env:
    db: DBEnv = DBEnv()
    logger: LoggerEnv = LoggerEnv()
    app: AppEnv = AppEnv()


Env = _Env()
