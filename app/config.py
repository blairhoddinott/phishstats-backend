from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "phishstats-backend"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://phishstats:phishstats@db:5432/phishstats"
    sync_database_url: str = "postgresql://phishstats:phishstats@db:5432/phishstats"
    echo_sql: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
