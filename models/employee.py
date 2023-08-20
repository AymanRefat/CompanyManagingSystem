from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, CHAR, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import Session, validates
from datetime import date
from settings import KIND_OPTS, DB_ENGINE


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column("id", Integer, autoincrement=True, nullable=False, primary_key=True)
    name = Column("name", String(255), nullable=False)
    job_title = Column("job_title", String(255), nullable=False)
    gender = Column("gender", CHAR, nullable=False)  # m , f
    kind = Column("kind", String(20), nullable=False)  # full , part , free

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

    def get_total_hours(self, SessionMaker: Session) -> float:
        with SessionMaker as session:
            q = session.query(WorkedHours).filter(WorkedHours.employee_id == self.id)
            return sum(x[0] for x in q.values(Column("hours")))

    def __str__(self):
        return f"{self.id} - {self.name}"


class WorkedHours(Base):
    __tablename__ = "worked_hours"
    id = Column("id", Integer, autoincrement=True, nullable=False, primary_key=True)
    employee_id = Column(
        "employee_id", ForeignKey("employees.id", ondelete="CASCADE"), nullable=False
    )
    hours = Column("hours", Float, nullable=False)
    hour_rate = Column("current_hour_rate", Float, nullable=False)
    worked_date = Column("worked_time", Date, nullable=False)

    def __str__(self):
        with Session(bind=DB_ENGINE) as session:
            q = session.query(Employee).get({"id": self.employee_id})
            return f"ID:{self.id} - {q.name} - {self.hours} H - {self.hour_rate}$/H - {self.worked_date}"

    @validates("worked_date")
    def validate_worked_date(self, key, value) -> date:
        if isinstance(value, date):
            return value
        else:
            raise TypeError("Worked Date should be a date")

    @validates("hours", "hour_rate")
    def validate_float(self, key, value) -> float:
        try:
            return float(value)
        except:
            raise TypeError("the Type of data should be Float")


Base.metadata.create_all(bind=DB_ENGINE)
