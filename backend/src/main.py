from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import init_routers
from config.db import db
from config.logger import configure_logging
from core.middleware import init_middlewares
from envs import Env


app = FastAPI(title="Memories is what we share")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_routers(app)


@app.on_event("startup")
async def on_startup() -> None:
    init_middlewares(app)
    db.init_db()
    configure_logging(log_type=Env.logger.LOG_TYPE, log_level=Env.logger.LOG_LEVEL)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    ...
