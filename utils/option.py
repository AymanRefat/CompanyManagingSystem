from abc import ABC, abstractmethod, abstractproperty
from utils.input_manager import InputManager
from utils.signal import *
from utils.funcs import combine_dicts
from sqlalchemy.orm import Session


class Option(ABC):
    """an option is a function every Option should have a functionality to do"""

    name: str = None
    info: str = None
    input_list: list[InputManager] = []

    def __init__(self, SessionMaker: Session, exit_opt: bool = False) -> None:
        self.exit_opt = exit_opt
        self.SessionMaker = SessionMaker
        self.data_dict = {}

    @abstractproperty
    def task(self) -> str:
        """return a string describing the task"""

    def __str__(self) -> str:
        return self.name

    def show_info(self) -> None:
        if self.info:
            print(self.info)

    def get_data(self) -> None:
        """Take the data from the Input Manager and set it in the Option Instance"""
        data = []
        for item in self.input_list:
            data.append(item.try_till_get(self.exit_opt))
        self.data_dict = combine_dicts(*data)

    @abstractmethod
    def excute(self) -> Signal:
        """a function excutes when the user choose the option and return a Signal"""

    def add_signal(self, signal: Signal) -> None:
        self.signal = signal(self.task)

    def start(self) -> None:
        self.show_info()
        # to ensure that the opt needs data
        if len(self.input_list) >= 1:
            self.get_data()
        try:
            self.excute()
            self.add_signal(Succeeded)
        except Exception as e:
            self.add_signal(Failed)
            print(e)
            print(e.__traceback__)

        self.signal.print()
