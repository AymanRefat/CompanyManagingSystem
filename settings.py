import os
from sqlalchemy import create_engine, Engine


def mysql_engine(logging: bool) -> Engine:
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")
    connection_string = (
        f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}"
    )

    return create_engine(connection_string, echo=logging)


def sqlite_engine(logging: bool) -> Engine:
    return create_engine("sqlite:///database.sqlite")


LOGGING = False

DB_ENGINE = sqlite_engine(LOGGING)


KIND_OPTS = ["freelancer", "fulltime", "parttime"]
