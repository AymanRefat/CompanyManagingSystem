import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, CHAR, Integer, Float, ForeignKey, Date, DateTime
from sqlalchemy.orm import Session, validates
from datetime import date

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

    def __repr__(self):
        return f"{self.id} - {self.name}"


class WorkedHours(Base):
    __tablename__ = "worked_hours"
    id = Column("id", Integer, autoincrement=True, nullable=False, primary_key=True)
    employee_id = Column("employee_id", ForeignKey("employees.id"))
    hours = Column("hours", Float, nullable=False)
    current_hour_rate = Column("current_hour_rate", Float, nullable=False)
    worked_date = Column("worked_time", Date, nullable=False)

    def __repr__(self):
        with Session(bind=engine) as session:
            return f"ID:{self.id} - {session.query(Employee).filter(Employee.id == self.employee_id).first().name} - {self.hours} - {self.current_hour_rate}$ - {self.worked_date}"

    @validates("worked_date")
    def validate_worked_date(self, key, value) -> date:
        if isinstance(value, date):
            return value
        else:
            raise TypeError("Worked Date should be a date")

    @validates("hours", "current_hour_rate")
    def validate_float(self, key, value) -> float:
        try:
            return float(value)
        except:
            raise TypeError("the Type of data should be Float")


Base.metadata.create_all(bind=engine)
