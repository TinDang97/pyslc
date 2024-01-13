import os

from pydantic_settings import BaseSettings


# class postgres config
class PostgresConfig(
    BaseSettings,
    env_file_encoding="utf-8"
):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "pyslc"
    db_user: str = "pyslc"
    db_password: str = "pyslc"

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# class model config
class Settings(
    BaseSettings,
    env_prefix="pyslc_",
    env_file_encoding="utf-8",
):
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
    settings = Settings(env_file=".env")
else:
    settings = Settings(env_file="dev.env")
