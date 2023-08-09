from app.menu import Menu, Option
from app.models import Employee, engine, Session, KIND_OPTS


class ShowAllEmployeesOpt(Option):
    name = "Show all"

    @classmethod
    def run(cls) -> None:
        print("\nEmployees Table")
        print("===============")
        with Session(engine) as session:
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
        kind = input("Full , Part , Freelance: ")
        hour_rate = input("Hour Rate: ")

        with Session(engine) as session:
            session.add(
                Employee(
                    name=name,
                    job_title=title,
                    gender=gender,
                    kind=kind,
                    hour_rate=hour_rate,
                )
            )
            session.commit()
            print("=== Done ===")


class UpdateEmployeesOpt(Option):
    name = "Update"

    @classmethod
    def run(self) -> None:
        with Session(engine) as session:
            em_id = int(input("Employee Id you want to Update: "))
            q = session.query(Employee).filter(Employee.id == em_id)
            sure = input(f"Do you really want to Update ({q.first()}) (y , n): ")
            if sure.lower() == "y":
                print(f"Avaliable Kinds: {KIND_OPTS}")
                name = input("Name: ")
                title = input("Title: ")
                gender = input("Gender (m , f): ")
                kind = input("Full , Part , Freelance: ")
                hour_rate = input("Hour Rate: ")
                q.update(
                    {
                        "name": name,
                        "job_title": title,
                        "gender": gender,
                        "kind": kind,
                        "hour_rate": hour_rate,
                    }
                )
                session.commit()
            else:
                print("=== Canceled ===")


class DeleteEmployeesOpt(Option):
    name = "Delete"

    @classmethod
    def run(self) -> None:
        with Session(engine) as session:
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


employees_menu = Menu(
    "Employees",
    ShowAllEmployeesOpt,
    CreateNewEmployeesOpt,
    DeleteEmployeesOpt,
    UpdateEmployeesOpt,
)

home_menu = Menu("Home Menu", employees_menu)
