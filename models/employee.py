from __future__ import annotations
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, String, CHAR, ForeignKey
from sqlalchemy.orm import validates
from datetime import date
from settings import KIND_OPTS
from models.validators import validate_float, validate_date


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    name: Mapped[str] = mapped_column("name", nullable=False)
    job_title: Mapped[str] = mapped_column("job_title", nullable=False)
    gender: Mapped[CHAR] = mapped_column("gender", CHAR, nullable=False)  # m , f
    kind: Mapped[str] = mapped_column(
        "kind", String(20), nullable=False
    )  # full , part , free
    worked_hours: Mapped[List[WorkedHours]] = relationship(
        back_populates="employee",
        cascade="all, delete",
    )
    rewards: Mapped[List[Reward]] = relationship(
        back_populates="employee",
        cascade="all, delete",
    )

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

    def get_total_hours(self) -> float:
        with self.session as session:
            q = session.query(WorkedHours).filter(WorkedHours.employee_id == self.id)
            return sum(x[0] for x in q.values(Column("hours")))

    def __str__(self):
        return f"{self.id} - {self.name}"


class WorkedHours(Base):
    __tablename__ = "worked_hours"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        "employee_id", ForeignKey("employees.id"), nullable=False
    )
    employee: Mapped[Employee] = relationship(back_populates="worked_hours")
    hours: Mapped[float] = mapped_column("hours", nullable=False)
    hour_rate: Mapped[float] = mapped_column("current_hour_rate", nullable=False)
    worked_date: Mapped[date] = mapped_column("worked_time", nullable=False)

    def __str__(self):
        return f"ID:{self.id} - {self.employee.name} - {self.hours} H - {self.hour_rate}$/H - {self.worked_date}"

    @validates("worked_date")
    def validate_worked_date(self, key, value) -> date:
        return validate_date(value)

    @validates("hours", "hour_rate")
    def validate_float(self, key, value) -> float:
        return validate_float(value)


class Reward(Base):
    __tablename__ = "rewards"
    id: Mapped[int] = mapped_column(
        autoincrement=True, nullable=False, primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        "employee_id", ForeignKey("employees.id"), nullable=False
    )
    employee: Mapped[Employee] = relationship(back_populates="rewards")

    value: Mapped[float] = mapped_column("value")
    reward_date: Mapped[date] = mapped_column("date")

    @validates("date")
    def validate_worked_date(self, key, value) -> date:
        return validate_date(value)

    @validates("value")
    def validate_float(self, key, value) -> float:
        return validate_float(value)

    def __str__(self):
        return f"{self.id} - {self.employee.name} - {self.value}"
