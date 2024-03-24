"""All application settings."""

import os

from base.base_helper import LOG_LEVEL
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Base(BaseSettings):
    class Config:
        """Settings for reading environment variables from a file.

        env_file - The path to the environment, to run locally
        """

        env_nested_delimiter = "__"
        env_file = os.path.join(BASE_DIR, ".env_crawler")
        enf_file_encoding = "utf-8"
        extra = "ignore"


class UvicornSettings(Base):
    """Uvicorn settings class.

    Args:
        host (str): Hostname.
        port (int): Port number.
        workers (int): Number of worker processes.
        log_level (str): Log level.
        reload (bool): Reload on code changes.
    """

    host: str
    port: int
    workers: int
    log_level: LOG_LEVEL = "INFO"
    reload: bool = True

    @field_validator("log_level")
    def to_lower_case(cls, log_level: LOG_LEVEL) -> str:  # noqa:
        """Convert the log level to lower case.

        Args:
            log_level (str): The log level.

        Returns:
            str: The converted log level.
        """
        return log_level.lower()


class AppSettings(Base):
    """Application settings class.

    Args:
        title (str): The name of the application.
        description (str): The description of the application.
        version (str): The version of the application.
        docs_url (str): The URL for the application's documentation.
        redoc_url (str): The URL for the application's redoc.
        openapi_url (str): The URL for the application's openapi.json.
    """

    title: str = "File handler"
    description: str = "Files for processing are taken from the cloud drive."
    version: str = "0.0.1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"

    app_host: str = "0.0.0.0"
    app_port: int = 8010

    @property
    def base_url(self) -> str:
        """The base URL for the application.

        Returns:
            str: The base URL for the application.
        """
        return f"http://{self.app_host}:{self.app_port}"  # noqa:


class LogSettings(Base):
    """Setting logging.

    level (str, optional): The level of logging. Defaults to "INFO".
    guru (bool, optional): Whether to enable guru mode. Defaults to True.
    traceback (bool, optional): Whether to include tracebacks in logs. Defaults to True.
    """

    level: LOG_LEVEL
    guru: bool
    traceback: bool


class PostgresSettings(Base):
    """Settings for PostgresSQL database connections.

    Attributes:
        postgres_db: The name of the database.
        postgres_user: The username for the database.
        postgres_password: The password for the database.
        postgres_host: The hostname or IP address of the database server.
        postgres_port: The port number of the database server.
        postgres_schema: The name of the schema to use.

    Methods:
        dsn: Returns the connection URL as a string.
    """

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: str
    postgres_schema: str

    def dsn(self, show_secret: bool = False) -> str:
        """Returns the connection URL as a string.

        Args:
            show_secret (bool, optional): Whether to show the secret. Defaults to False.

        Returns:
            str: The connection URL.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=self.postgres_user,
            password=(
                self.postgres_password.get_secret_value()
                if show_secret
                else self.postgres_password
            ),
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
        )
