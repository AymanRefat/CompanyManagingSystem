import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, CHAR, Integer, Float
from sqlalchemy.orm import Session, validates

load_dotenv()
Base = declarative_base()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")

KIND_OPTS = ["freelancer", "fulltime", "parttime"]

connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}"

engine = create_engine(connection_string, echo=False)


class Employee(Base):
    __tablename__ = "employees"
    id = Column("id", Integer, autoincrement=True, nullable=False, primary_key=True)
    name = Column("name", String(255))
    job_title = Column("job_title", String(255))
    gender = Column("gender", CHAR)  # m , f
    kind = Column("kind", String(20))  # full , part , free
    hour_rate = Column("hour_rate", Float, default=10)

    @validates("gender")
    def validate_gender(self, key, value: str) -> str:
        allowed = ["f", "m"]
        if value.strip().lower() not in allowed:
            raise ValueError(f"the Gender Should be in {allowed}")
        else:
            return value.lower()

    @validates("kind")
    def validate_kind(self, key, value: str) -> str:
        if value.strip().lower() not in KIND_OPTS:
            raise ValueError(f"the Kind Should be in {KIND_OPTS}")
        else:
            return value.strip().lower()

    @validates("hour_rate")
    def validate_hour_rate(self, key, value) -> float:
        try:
            return float(value)
        except:
            raise TypeError("Hour Rate should be Float")

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.hour_rate}$"


Base.metadata.create_all(bind=engine)
