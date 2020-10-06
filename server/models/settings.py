from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = "postgres://test:test@localhost:5432/test"
