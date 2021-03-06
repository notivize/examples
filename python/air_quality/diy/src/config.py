from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./diy.db"
    gmail_user: str = "arthur@notivize.com"
    gmail_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
