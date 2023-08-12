from utils.menu import Option
from models.employee import Employee
from sqlalchemy.orm import Session, Query
from settings import KIND_OPTS, DB_ENGINE
from utils.input_manager import InputManager
from utils.signal import Succeeded, Cancelled, Failed, Signal


class ShowAllEmployeesOpt(Option):
    name = "Show all"
    info = "Employees List"

    @property
    def task(self) -> str:
        return " Showing all Employees"

    def excute(self) -> Signal:
        with Session(DB_ENGINE) as session:
            results = session.query(Employee).all()
            for obj in results:
                print(obj)


class CreateNewEmployeesOpt(Option):
    name = "Create New"
    info = f"Avaliable Kinds: {KIND_OPTS}"
    input_list = [
        InputManager("name", str, str, "Name: "),
        InputManager("job_title", str, str, "Title: "),
        InputManager("gender", str, str, "Gender (m , f): "),
        InputManager("kind", str, str, "Kind: "),
    ]

    @property
    def task(self) -> str:
        return f" Creating {self.data_dict} Employee"

    def excute(self) -> Signal:
        with Session(DB_ENGINE) as session:
            session.add(Employee(**self.data_dict))
            session.commit()


class UpdateEmployeesOpt(Option):
    name = "Update"
    info = f"Avaliable Kinds: {KIND_OPTS}"
    input_list = [
        InputManager("em_id", int, int, "Employee Id you want to Update: "),
        InputManager("name", str, str, "Name: "),
        InputManager("job_title", str, str, "Title: "),
        InputManager("gender", str, str, "Gender (m , f): "),
        InputManager("kind", str, str, "Kind: "),
    ]

    @property
    def task(self) -> str:
        return f" Updating ({self.get_query().first()}) -> {self.data_dict} Employee"

    def get_query(self) -> Query:
        with Session(DB_ENGINE) as session:
            em_id = self.data_dict.get("em_id")
            q = session.query(Employee).filter(Employee.id == em_id)
            self.q = q
            return q

    def excute(self) -> Signal:
        with Session(DB_ENGINE) as session:
            q = self.get_query()
            q.update(**self.data_dict)
            session.commit()


class DeleteEmployeesOpt(Option):
    name = "Delete"

    input_list = [
        InputManager("em_id", int, int, "Employee Id you want to Delete: "),
    ]

    @property
    def task(self) -> str:
        return f"Deleting: {self.get_query().first()}"

    def get_query(self) -> Query:
        with Session(DB_ENGINE) as session:
            em_id = self.data_dict.get("em_id")
            q = session.query(Employee).filter(Employee.id == em_id)
            self.q = q
            return q

    def excute(self) -> Signal:
        with Session(DB_ENGINE) as session:
            q = self.get_query()
            q.delete()
            session.commit()
