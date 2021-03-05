from pydantic import BaseSettings


class Settings(BaseSettings):
    notivize_api_key: str
    notivize_api_url: str = "https://events-api.notivize.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
