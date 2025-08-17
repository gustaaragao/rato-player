from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # Postgres
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # MongoDB
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_DB_NAME: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str