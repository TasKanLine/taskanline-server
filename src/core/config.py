from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class Core(BaseModel):
    HOST: str = "localhost"
    PORT: int = 8000


class PostgresConfig(BaseModel):
    HOST: str | None = None
    PORT: int | None = None
    USER: str = "postgres"
    PASSWORD: str = "password"
    DATABASE: str = "database"

    def url(self) -> str:
        u = self.USER
        p = self.PASSWORD
        return f"postgresql+asyncpg://{u}:{p}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class SQLiteSettings(BaseModel):
    DATABASE: str = "database/db.sqlite3"

    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DATABASE}"


class Settings(BaseSettings):
    core: Core = Core()
    db: PostgresConfig = PostgresConfig()
    db_test: SQLiteSettings = SQLiteSettings()

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", env_file_encoding="utf-8"
    )


settings = Settings()
