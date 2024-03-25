import os
from typing import Optional

from pydantic import BaseModel, Field, field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "pyslc"
    schema_: str = Field("pyslc", alias="schema")

    uri: Optional[str] = None

    @field_validator("uri", mode="before")
    @classmethod
    def validate_uri(cls, field_value: Optional[str], values: ValidationInfo):
        if field_value:
            return field_value

        field_value_: PostgresDsn = PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("user"),
            password=values.data.get("password"),
            host=values.data.get("host"),
            port=values.data.get("port"),
            path=f"/{values.data.get('database')}",
        )
        assert (
            field_value_.path and len(field_value_.path) > 1
        ), "database must be provided"
        return field_value_.unicode_string()


# class model config
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
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

    # Settings for the FastAPI application CORS
    cors_allow_origins: str = "*"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"

    # Settings for the FastAPI application logging
    log_level: str = "info"
    log_format: str = "%(asctime)s %(levelname)s %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    # settings of the pyslc postgres database connection with schema
    db: DatabaseSettings = DatabaseSettings(schema="public")

    # settings of the pyslc openai api
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo-1106"
    zep_url: str = "http://localhost:8000"

    # settings of the pyslc llm storage
    llm_storage_dir: str = "./llm_storage"
    trusted_hosts: list[str] = ["localhost"]


# create an instance of the Settings class
if os.environ.get("PYSLC_ENV") == "production":
    settings = Settings(_env_file=".env")  # type: ignore
else:
    settings = Settings(_env_file="dev.env")  # type: ignore
