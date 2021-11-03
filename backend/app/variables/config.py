from dotenv.main import find_dotenv
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    db_url = "sqlite:///./sql_app.db"
    mail_username = "trojo.mailtesting"
    mail_password = 'donthackme1'
    mail_from = 'trojo.mailtesting@gmail.com'
    mail_port = 587
    mail_server = 'smtp.gmail.com'
    mail_from_name = 'Super Official Mailing Server'

    class Config:
        env_file = "variables/.env"
        # if it does not work, check pathing, might be the reason.
        # find_dotenv() may help. (MAY...)
        # it currently works if the script is run from the 'app' folder
        #
        # also check if there are any other virtual environments running for this project, 
        # they tend to mess with eachother and only one of them obtains the .env file

@lru_cache()
def get_settings():
    return Settings()
    
settings = get_settings()