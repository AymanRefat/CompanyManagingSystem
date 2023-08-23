from utils.option import Option, ShowAllOption
from models.employee import Employee, WorkedHours
from sqlalchemy.orm import Query
from datetime import datetime, date
from utils.input_manager import InputManager


class ShowWorkedHours(ShowAllOption):
    name = "Show All"
    info = "Worked Hours List"
    objects = "worked hours"
    model = WorkedHours


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
        InputManager("hours", float, float, "Enter Hours Worked: "),
    ]

    @property
    def task(self) -> str:
        return f"Adding {self.data_dict.get('hours')} with Hour Rate {self.data_dict.get('hour_rate')}$ For All Employees "

    def excute(self) -> None:
        with self.SessionMaker as session:
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
        with self.SessionMaker as session:
            employee_id = self.data_dict.pop("employee_id")
            q = session.query(Employee).filter(Employee.id == employee_id)
            self.q = q
            return q

    def excute(self) -> None:
        with self.SessionMaker as session:
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


class ShowTotalHoursForAll(Option):
    name = "Show Total Hours for All"

    @property
    def task(self) -> str:
        return f"Getting Total hours for All"

    def excute(self) -> None:
        with self.SessionMaker as session:
            ems = session.query(Employee).all()

            for em in ems:
                print(
                    f"Employee:({em.name}) , Total Hours:{em.get_total_hours(self.SessionMaker)}"
                )


class DeleteWorkedHoursForEmployee(Option):
    name = "Delete Worked Hours for Employee"

    input_list = [
        InputManager("record_id", int, int, "Worked Hours Id you want to delete: ")
    ]

    @property
    def task(self) -> str:
        return f"Deleting {self.get_query().first()} "

    def get_query(self) -> Query:
        with self.SessionMaker as session:
            record_id = self.data_dict.pop("record_id")
            q = session.query(WorkedHours).filter(WorkedHours.id == record_id)
            self.q = q
            return q

    def excute(self) -> None:
        with self.SessionMaker as session:
            q = self.q
            session.delete(q.first())
            session.commit()
