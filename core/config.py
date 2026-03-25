import functools
import pathlib

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./core/.env")

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
    ENVIRONMENT: str = "local"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres_db"


    @property
    def postgres_dsn(self) -> str:
        database = self.POSTGRES_DB if self.ENVIRONMENT != "test" else f"{self.POSTGRES_DB}_test"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{database}"
        )


@functools.lru_cache
def settings() -> Settings:
    return Settings()
