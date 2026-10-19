from urllib.parse import quote_plus

class Config:

    SECRET_KEY = "smart_agro_secret_key"

    MYSQL_USER = "root"
    MYSQL_PASSWORD = quote_plus("pinky@741153")
    MYSQL_HOST = "localhost"
    MYSQL_DB = "smart_agro_ai1"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}/{MYSQL_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False