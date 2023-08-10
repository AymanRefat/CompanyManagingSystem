from views.menu import Menu, Option
from models.employee import Employee, WorkedHours
from sqlalchemy.orm import Session
from datetime import datetime
from settings import KIND_OPTS, DB_ENGINE


class ShowAllEmployeesOpt(Option):
    name = "Show all"

    @classmethod
    def run(cls) -> None:
        print("\nEmployees Table")
        print("===============")
        with Session(DB_ENGINE) as session:
            results = session.query(Employee).all()
            for obj in results:
                print(obj)
            print("=== Done ===")


class CreateNewEmployeesOpt(Option):
    name = "Create New"

    @classmethod
    def run(cls) -> None:
        print(f"Avaliable Kinds: {KIND_OPTS}")
        name = input("Name: ")
        title = input("Title: ")
        gender = input("Gender (m , f): ")
        kind = input("Job Kind: ")

        with Session(DB_ENGINE) as session:
            session.add(
                Employee(
                    name=name,
                    job_title=title,
                    gender=gender,
                    kind=kind,
                )
            )
            session.commit()
            print("=== Done ===")


class UpdateEmployeesOpt(Option):
    name = "Update"

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            em_id = int(input("Employee Id you want to Update: "))
            q = session.query(Employee).filter(Employee.id == em_id)
            sure = input(f"Do you really want to Update ({q.first()}) (y , n): ")
            if sure.lower() == "y":
                print(f"Avaliable Kinds: {KIND_OPTS}")
                name = input("Name: ")
                title = input("Title: ")
                gender = input("Gender (m , f): ")
                kind = input("Full , Part , Freelance: ")
                q.update(
                    {
                        "name": name,
                        "job_title": title,
                        "gender": gender,
                        "kind": kind,
                    }
                )
                session.commit()
            else:
                print("=== Canceled ===")


class DeleteEmployeesOpt(Option):
    name = "Delete"

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            em_id = int(input("Employee Id you want to delete: "))
            q = session.query(Employee).filter(Employee.id == em_id)
            print(q)
            sure = input(f"Do you really want to Delete ({q.first()}) (y , n): ")
            if sure.lower() == "y":
                q.delete()
                session.commit()
                print("=== Done ===")
            else:
                print("=== Canceled ===")


class ShowWorkedHours(Option):
    name = "Show All"

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            q = session.query(WorkedHours).all()

            for item in q:
                print(item)


class addWorkedHoursForAll(Option):
    name = "Add Worked Hours for All "

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            user_input_date = input("Enter a date in the format YYYY-MM-DD: ")
            d = datetime.strptime(user_input_date, "%Y-%m-%d").date()
            hour_rate = input("Enter Hour Rate Price: ")
            hours = input("Enter Hours: ")

            employees = session.query(Employee).all()
            for employee in employees:
                data = {
                    "employee_id": employee.id,
                    "worked_date": d,
                    "current_hour_rate": hour_rate,
                    "hours": hours,
                }
                obj = WorkedHours(**data)
                session.add(obj)
            session.commit()


class addWorkedHoursForEmployee(Option):
    name = "Add Worked Hours for Employee"

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            user_input_date = input("Enter a date in the format YYYY-MM-DD: ")
            d = datetime.strptime(user_input_date, "%Y-%m-%d").date()

            employee_id = int(input("Enter Employee id: "))
            hour_rate = input("Enter Hour Rate Price: ")
            hours = input("Enter Hours: ")

            employee = (
                session.query(Employee).filter(Employee.id == employee_id).first()
            )
            data = {
                "employee_id": employee.id,
                "worked_date": d,
                "current_hour_rate": hour_rate,
                "hours": hours,
            }

            obj = WorkedHours(**data)
            session.add(obj)
            session.commit()
        print("=== Done ===")


class DeleteWorkedHoursForEmployee(Option):
    name = "Delete Worked Hours for Employee"

    @classmethod
    def run(self) -> None:
        with Session(DB_ENGINE) as session:
            wh_id = int(input("Worked Hours Id you want to delete: "))
            q = session.query(WorkedHours).filter(WorkedHours.id == wh_id)
            sure = input(f"Do you really want to Delete ({q.first()}) (y , n): ")
            if sure.lower() == "y":
                q.delete()
                session.commit()
                print("=== Done ===")
            else:
                print("=== Canceled ===")


hours_menu = Menu(
    "Hours",
    ShowWorkedHours,
    addWorkedHoursForAll,
    addWorkedHoursForEmployee,
    DeleteWorkedHoursForEmployee,
)

employees_menu = Menu(
    "Employees",
    ShowAllEmployeesOpt,
    CreateNewEmployeesOpt,
    DeleteEmployeesOpt,
    UpdateEmployeesOpt,
)

home_menu = Menu("Home Menu", employees_menu, hours_menu)
