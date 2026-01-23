from urllib.parse import quote
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


from typing import List


class Core(BaseModel):
    HOST: str = "localhost"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["*"]
    JWT_SECRET_KEY: str = "secret"


class PostgresConfig(BaseModel):
    HOST: str | None = None
    PORT: int | None = None
    USER: str = "postgres"
    PASSWORD: str = "password"
    DATABASE: str = "database"

    def url(self) -> str:
        u = quote(self.USER)
        p = quote(self.PASSWORD)
        return f"postgresql+asyncpg://{u}:{p}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class Settings(BaseSettings):
    core: Core = Core()
    db: PostgresConfig = PostgresConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
