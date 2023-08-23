from sqlalchemy import Engine
from models.employee import Base


def create_tabels(engine: Engine) -> None:
    Base.metadata.create_all(engine)
