import os

from pydantic_settings import BaseSettings, SettingsConfigDict


# class postgres config
class PostgresConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    name: str = "pyslc"
    user: str = "pyslc"
    password: str = "pyslc"

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


# class model config
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        env_prefix="pyslc_",
        env_file_encoding="utf-8",
        env_file=".env",
    )
    # Settings for the FastAPI application
    app_name: str = "pyslc-service"
    app_description: str = "A simple REST API for the pyslc library."
    app_version: str = "0.0.1"

    # Settings for the FastAPI application server
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # settings of the pyslc postgres database connection
    db = PostgresConfig()


# create an instance of the Settings class
if os.environ.get("PYSLC_ENV") == "production":
    settings = Settings(_env_file=".env")
else:
    settings = Settings(_env_file="dev.env")
