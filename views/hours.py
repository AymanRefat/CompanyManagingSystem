from utils.menu import Option
from models.employee import Employee, WorkedHours
from sqlalchemy.orm import Session, Query
from datetime import datetime, date
from settings import DB_ENGINE
from utils.input_manager import InputManager


class ShowWorkedHours(Option):
    name = "Show All"
    info = "Worked Hours List"

    @property
    def task(self) -> str:
        return " Showing all Worked Hours"

    def excute(self) -> None:
        with Session(DB_ENGINE) as session:
            q = session.query(WorkedHours).all()
            for item in q:
                print(item)


class addWorkedHoursForAll(Option):
    name = "Add Worked Hours for All "
    input_list = [
        InputManager(
            "date",
            date,
            datetime.strptime,
            "Enter a date in the format YYYY-MM-DD: ",
            cast_func_args=["%Y-%m-%d"],
        ),
        InputManager("hour_rate", float, float, "Enter Hour Rate Price: "),
        InputManager("hours", float, float, "Enter Hours Price: "),
    ]

    @property
    def task(self) -> str:
        return f"Adding {self.data_dict.get('hours')} with Hour Rate {self.data_dict.get('hour_rate')}$ For All Employees "

    def excute(self) -> None:
        with Session(DB_ENGINE) as session:
            d = self.data_dict.pop("date").date()
            employees = session.query(Employee).all()
            for employee in employees:
                data = {
                    **self.data_dict,
                    "employee_id": employee.id,
                    "worked_date": d,
                }
                obj = WorkedHours(**data)
                session.add(obj)
            session.commit()


class addWorkedHoursForEmployee(Option):
    name = "Add Worked Hours for Employee"

    input_list = [
        InputManager("employee_id", int, int, "Enter Employee id: "),
        InputManager(
            "date",
            date,
            datetime.strptime,
            "Enter a date in the format YYYY-MM-DD: ",
            cast_func_args=["%Y-%m-%d"],
        ),
        InputManager("hour_rate", float, float, "Enter Hour Rate Price: "),
        InputManager("hours", float, float, "Enter Hours Price: "),
    ]

    @property
    def task(self) -> str:
        return f"Adding {self.data_dict.get('hours')} with Hour Rate {self.data_dict.get('hour_rate')}$ For {self.get_query().first()} "

    def get_query(self) -> Query:
        with Session(DB_ENGINE) as session:
            employee_id = self.data_dict.pop("employee_id")
            q = session.query(Employee).filter(Employee.id == employee_id)
            self.q = q
            return q

    def excute(self) -> None:
        with Session(DB_ENGINE) as session:
            d = self.data_dict.pop("date").date()

            employee = self.q.first()
            data = {
                **self.data_dict,
                "employee_id": employee.id,
                "worked_date": d,
            }

            obj = WorkedHours(**data)
            session.add(obj)
            session.commit()


class DeleteWorkedHoursForEmployee(Option):
    name = "Delete Worked Hours for Employee"

    input_list = [
        InputManager("record_id", int, int, "Worked Hours Id you want to delete: ")
    ]

    @property
    def task(self) -> str:
        return f"Deleting {self.get_query().first()} "

    def get_query(self) -> Query:
        with Session(DB_ENGINE) as session:
            record_id = self.data_dict.pop("record_id")
            q = session.query(WorkedHours).filter(WorkedHours.id == record_id)
            self.q = q
            return q

    def excute(self) -> None:
        with Session(DB_ENGINE) as session:
            q = self.q
            q.delete()
            session.commit()
