
import os
from urllib.parse import quote_plus


class Config:
    # Use a strong random SECRET_KEY in Render
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "dev-only-change-me"
    )

    # Local defaults are for development only.
    # Render will use the Aiven values from its environment variables.
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
    MYSQL_DB = os.environ.get("MYSQL_DB", "smart_agro_ai1")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{quote_plus(MYSQL_USER)}:"
        f"{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOST}:"
        f"{MYSQL_PORT}/{MYSQL_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure certificate verification for Aiven when supplied.
    MYSQL_SSL_CA = os.environ.get("MYSQL_SSL_CA")

    if MYSQL_SSL_CA:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "ssl": {
                    "ca": MYSQL_SSL_CA
                }
            }
        }
