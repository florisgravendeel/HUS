from pydantic import BaseSettings


class Settings(BaseSettings):
    UDB: str = "sqlite:///./users.db"
    MDB: str = "sqlite:///./main.db"
    DDB: str = "sqlite:///./dummy.db"

    class Config:
        env_file = ".env"