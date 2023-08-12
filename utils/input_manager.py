from typing import Callable, Any


class InputManager:
    def __init__(
        self,
        key: str,
        t: type,
        cast_func: Callable,
        promt_msg: str,
        cast_func_args: tuple = (),
        cast_func_kwargs: dict = {},
    ) -> None:
        self.t = t
        self.cast_func: Callable = cast_func
        self.promt_msg: str = promt_msg
        self.key = key
        self.cast_func_args = cast_func_args
        self.cast_func_kwargs = cast_func_kwargs

    def try_till_get(self, exit_opt=False) -> dict:
        """start a while loop until getting the data , returns a dict with the key and gotten data"""

        while True:
            data = input(self.promt_msg)
            if exit_opt:
                if data == "q":
                    print("Bye :)")
                    exit()
            try:
                return {
                    self.key: self.cast_func(
                        data, *self.cast_func_args, **self.cast_func_kwargs
                    )
                }
            except Exception as e:
                print(e.__traceback__.__str__())
                print(e)
