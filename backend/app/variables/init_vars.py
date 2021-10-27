from os import environ as env
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def check_env(var_name: str, standard_value):
    if env.get(var_name) and ENV_FILE:
        return env.get(var_name)
    return standard_value

DB_URL = check_env('DB_URL', 'sqlite:///./sql_app.db')

MAIL_USERNAME = check_env('MAIL_USERNAME', 'trojo.mailtesting')
MAIL_PASSWORD = check_env('MAIL_PASSWORD', 'donthackme1')
MAIL_FROM = check_env('MAIL_FROM', 'trojo.mailtesting@gmail.com')
MAIL_PORT = check_env('MAIL_PORT', 587)
MAIL_SERVER = check_env('MAIL_SERVER', 'smtp.gmail.com')