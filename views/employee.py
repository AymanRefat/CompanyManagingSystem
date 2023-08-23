from utils.option import Option, ShowAllOption
from models.employee import Employee
from sqlalchemy.orm import Query
from settings import KIND_OPTS
from utils.input_manager import InputManager
from utils.signal import Signal


class ShowAllEmployeesOpt(ShowAllOption):
    name = "Show all"
    info = "Employees List"
    objects = "employees"
    model = Employee


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
        with self.SessionMaker as session:
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
        with self.SessionMaker as session:
            em_id = self.data_dict.pop("em_id")
            q = session.query(Employee).filter(Employee.id == em_id)
            self.q = q
            return q

    def excute(self) -> Signal:
        with self.SessionMaker as session:
            q = self.get_query()
            q.update(self.data_dict)
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
        with self.SessionMaker as session:
            em_id = self.data_dict.get("em_id")
            q = session.query(Employee).filter(Employee.id == em_id)
            self.q = q
            return q

    def excute(self) -> Signal:
        with self.SessionMaker as session:
            q = self.get_query()
            session.delete(q.first())
            session.commit()
