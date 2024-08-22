from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=('.jwt.env', '.db.env'))

class PostgresSettings(CommonSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

class SqliteSettings(CommonSettings):
    database_url: str

sqlite_settings = SqliteSettings()

print(sqlite_settings)
