from sqlite3.dbapi2 import SQLITE_ABORT
from urllib.parse import quote

from pydantic_core.core_schema import ComputedField
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, computed_field

class Core(BaseModel):
    HOST: str = "localhost"
    PORT: int = 8000


class PostgresConfig(BaseModel):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "password"
    DATABASE: str = "database"

    @computed_field
    def url(self) -> str:
        u = self.USER
        p = self.PASSWORD
        return f"postgresql://{u}:{p}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class SQLiteSettings(BaseModel):
    DATABASE: str = "database.sqlite"

    @computed_field
    def url(self) -> str:
        return f"sqlite:///{self.DATABASE}"


class Settings(BaseSettings):
    code: Core
    db: PostgresConfig
    db_test: SQLiteSettings

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", env_file_encoding="utf-8")
