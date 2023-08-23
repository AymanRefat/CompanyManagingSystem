from utils.menu import Option
from utils.option import ShowAllOption
from models.employee import Reward, Employee
from utils.input_manager import InputManager
from utils.signal import Signal

from datetime import date, datetime
from sqlalchemy.orm import Query


class ShowAllRewards(ShowAllOption):
    name = "Show Rewards"
    info = "Rewards List"
    objects = "rewards"
    model = Reward


class CreateReward(Option):
    name = "Create Reward"
    input_list = [
        InputManager("employee_id", int, int, "Enter Employee id: "),
        InputManager("value", float, float, "Enter Reward Value: "),
        InputManager(
            "d",
            date,
            datetime.strptime,
            "Enter a date in the format YYYY-MM-DD: ",
            cast_func_args=["%Y-%m-%d"],
        ),
    ]

    def get_query(self) -> Query:
        with self.SessionMaker as session:
            employee_id = self.data_dict.pop("employee_id")
            q = session.query(Employee).filter(Employee.id == employee_id)
            self.q = q
            return q

    @property
    def task(self) -> str:
        return (
            f"Create {self.data_dict.get('value')}$ for {self.get_query().first().name}"
        )

    def excute(self) -> Signal:
        with self.SessionMaker as session:
            d = self.data_dict.pop("date").date()

            data = {**self.data_dict, "date": d}
            obj = Reward(self.SessionMaker, **data)
            session.add(obj)
            session.commit()


class DeleteReward(Option):
    name = "Delete Reward"
    input_list = [
        InputManager("id", int, int, "Enter Reward id: "),
    ]

    @property
    def task(self) -> str:
        return f"Deleting Reward: {self.get_query().first()}"

    def get_query(self) -> Query:
        with self.SessionMaker as session:
            return session.query(Reward).filter(Reward.id == self.data_dict.get("id"))

    def excute(self) -> None:
        with self.SessionMaker as session:
            q = self.get_query()
            self.obj = q.first()
            session.delete(self.obj)
            session.commit()
