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

MAIL_USERNAME = check_env('MAIL_USERNAME', '')
MAIL_PASSWORD = check_env('MAIL_PASSWORD', '')
MAIL_FROM = check_env('MAIL_FROM', '')
MAIL_PORT = check_env('MAIL_PORT', '')
MAIL_SERVER = check_env('MAIL_SERVER', '')
MAIL_FROM_NAME = check_env('MAIL_FROM_NAME', '')