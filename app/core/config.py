from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_username: str
    db_password: str
    db_database: str

    class Config:
        env_file = ".env"

settings = Settings()
