from fastapi import FastAPI
from core.middleware.logging import RequestIdPlugin, RequestIpPlugin
from envs import Env
from starlette_context.middleware import ContextMiddleware


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        ContextMiddleware,
        plugins=(
            RequestIpPlugin(key=Env.logger.REQUEST_IP_HEADER),
            RequestIdPlugin(key=Env.logger.REQUEST_ID_HEADER, validate=False),
        ),
    )
