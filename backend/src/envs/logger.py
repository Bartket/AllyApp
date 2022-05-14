from enum import Enum

from pydantic import Field
from envs.base import BaseEnv


class LogLevel(Enum):
    trace: str = "TRACE"
    info: str = "INFO"
    debug: str = "DEBUG"
    success: str = "SUCCESS"
    warning: str = "WARNING"
    error: str = "ERROR"
    critical: str = "CRITICAL"


class LogType(Enum):
    json: str = "json"
    stderr: str = "stderr"
    formatted: str = "formatted"


class LoggerEnv(BaseEnv):
    LOG_LEVEL: LogLevel = LogLevel.debug
    LOG_TYPE: LogType = LogType.formatted

    REQUEST_ID_HEADER: str = Field(
        "X-Request-Id", description="Override header name to extract request id"
    )
    REQUEST_IP_HEADER: str = Field(
        "X-Request-Ip", description="Override header name to extract request ip"
    )

    ADD_REQUEST_IP: bool = False
