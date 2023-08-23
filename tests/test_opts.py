from models.employee import Employee, WorkedHours
from views.employee import (
    ShowAllEmployeesOpt,
    CreateNewEmployeesOpt,
    UpdateEmployeesOpt,
    DeleteEmployeesOpt,
)
from views.worked_hours import (
    ShowWorkedHours,
    addWorkedHoursForAll,
    addWorkedHoursForEmployee,
)
from views.rewards import ShowAllOption, CreateReward, DeleteReward
from sqlalchemy.orm import Session
from tests.conftest import create_employee


class TestEmployeeOptions:
    def test_showall_opt(self, SessionMaker: Session):
        opt = ShowAllEmployeesOpt(SessionMaker)
        opt.excute()

    def test_create_opt(self, employee_dict1: dict, SessionMaker: Session):
        opt = CreateNewEmployeesOpt(SessionMaker)
        opt.data_dict = employee_dict1
        opt.excute()

        with SessionMaker as s:
            q = s.query(Employee).filter(Employee.name == employee_dict1.get("name"))
            assert q.count() != 0

    def test_update_opt(
        self, employee_dict1: dict, employee_dict2: dict, SessionMaker: Session
    ):
        with SessionMaker as s:
            #  Getting id from the created employee
            obj = create_employee(SessionMaker, employee_dict1)
            opt = UpdateEmployeesOpt(SessionMaker)
            opt.data_dict = {**employee_dict2}
            #  add the new data and the id
            opt.data_dict["em_id"] = obj.id
            opt.excute()
            # assert that the name in the db is the new name
            q2 = s.query(Employee).filter(Employee.id == obj.id)
            assert q2.first().name == employee_dict2.get("name")

    def test_delete_opt(self, employee_dict1: dict, SessionMaker: Session):
        opt = DeleteEmployeesOpt(SessionMaker)
        obj = create_employee(SessionMaker, employee_dict1)
        with SessionMaker as s:
            opt.data_dict["em_id"] = obj.id
            opt.excute()

            assert s.query(Employee).get({"id" == obj.id}) == None


class TestWorkedHoursOptions:
    def test_show_all(self, SessionMaker: Session):
        # Create before show
        opt = ShowWorkedHours(SessionMaker)
        opt.excute()


class TestRewardsOptions:
    pass
