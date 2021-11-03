from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    db_url = "sqlite:///./sql_app.db"
    mail_username = "no name"
    mail_password = 'donthackme1'
    mail_from = 'trojo.mailtesting@gmail.com'
    mail_port = 587
    mail_server = 'smtp.gmail.com'
    mail_from_name = 'Super Official Mailing Server'

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
    
settings = get_settings()