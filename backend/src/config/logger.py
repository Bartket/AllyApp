import json
import logging
import sys

from loguru import logger
from envs import Env
from envs.logger import LogLevel, LogType
from starlette_context import context


class _InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def json_log_format(message) -> None:
    record = message.record
    exception = record["exception"]

    if exception is not None:
        exception = {
            "type": None if exception.type is None else exception.type.__name__,
            "value": exception.value,
            "traceback": bool(record["exception"].traceback),
        }

    log_content = {
        "time": record["time"],
        "level": record["level"].name,
        "message": record["message"],
        "extra": record["extra"],
        "exception": exception,
        "name": record["name"],
        "function": record["function"],
    }

    print(
        json.dumps(
            log_content,
            default=str,
        ),
        file=sys.stderr,
    )


class Formatter:
    def __init__(self) -> None:
        self.fmt = (
            "<level>{level: <8}</level> "
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
            "<blue>{extra}</blue> "
            "{name}:"
            "<cyan>{function}</cyan> - "
            "<level>{message}</level>"
            "<level>{exception}</level>"
        )

    def format(self, record: dict) -> str:
        return self.fmt + "\n"


class Patcher:
    @classmethod
    def patch(cls, record: dict) -> None:
        cls.add_id(record)
        if Env.logger.ADD_REQUEST_IP:
            cls.add_ip(record)

    @classmethod
    def add_ip(cls, record: dict) -> None:
        try:
            ip = context.get(Env.logger.REQUEST_IP_HEADER)
            if ip:
                record["extra"]["Request-IP"] = ip
        except RuntimeError:
            pass

    @classmethod
    def add_id(cls, record: dict) -> None:
        try:
            record["extra"]["Request-ID"] = context.get(Env.logger.REQUEST_ID_HEADER)
        except RuntimeError:
            pass


def log_factory(log_type: LogType, log_level: str) -> int:
    # Remove default handler
    logger.remove()
    if log_type == LogType.json:
        return logger.add(json_log_format, format="{message}", level=log_level)

    elif log_type == LogType.formatted:
        formatter = Formatter()
        return logger.add(
            sys.stderr, colorize=True, format=formatter.format, level=log_level
        )

    else:
        return logger.add(
            sys.stderr, format="{message}", serialize=True, level=log_level
        )


def configure_logging(log_level: LogLevel, log_type: LogType) -> dict:

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [_InterceptHandler()]

    log_factory(log_level=log_level.value, log_type=log_type)
    logger.configure(patcher=Patcher.patch)
    logging.getLogger("uvicorn.access").disabled = True

    return {
        "version": 1,
        "disable_existing_loggers": True,
        "loggers": {
            "uvicorn": {"level": log_level.value},
            "uvicorn.error": {"level": log_level.value},
            "uvicorn.access": {"level": log_level.value},
        },
    }
