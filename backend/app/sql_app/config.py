from fastapi.param_functions import Depends
from pydantic import BaseSettings

class Settings(BaseSettings):
    UDB: str = "sqlite:///./user.db"
    MDB: str = "sqlite:///./main.db"
    DDB: str = "sqlite:///./dummy.db"
    sqlite_args: str = '{"check_same_thread": False}'

    class Config:
        env_file = ".env" 
        env_file_encoding = 'utf-8'

# def get_settings():
#     return Settings()

# def get_setting(param, settings = Settings):
#     # array = []
#     # for i in settings:
#         # array.append(i)
#         # if i[0] == param:
#             # return i[1]
#     return Settings.sqlite_args

    
# async def get_variablo(settings = Settings):
#     return await settings.sqlite_args