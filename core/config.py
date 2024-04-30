from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    access_token_expire_minutes: int
    algorithm: str
    database_host: str
    database_name: str
    database_password: str
    database_port: int
    database_username: str
    secret_key: str
    redis_host: str
    redis_password: str
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()