from pydantic import BaseSettings


class BaseEnv(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True
