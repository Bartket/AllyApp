from pydantic import Field, PositiveInt
from envs.base import BaseEnv


class AppEnv(BaseEnv):
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: PositiveInt = Field(default=5000)
    RELOAD: bool = Field(default=False)
