from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./diy.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
