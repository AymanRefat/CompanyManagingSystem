from app.menu import Menu


class Interface:
    """a Class that managing the displaying of the menus"""

    def __init__(self, home_menu) -> None:
        self.home_menu = home_menu
        self.menu_history = []

    def start(self) -> None:
        self.print_welcome_message()
        self.start_menu(self.home_menu)

    # BUG
    def add_menu_to_history(self, menu: Menu) -> None:
        self.menu_history.append(menu)

    def back_Menu(self) -> Menu:
        if self.menu_history:
            return self.menu_history[-2]

    def start_menu(self, menu: Menu) -> None:
        self.add_menu_to_history(menu)
        menu.display()
        back_opt_num = None

        if len(self.menu_history) >= 2:
            back_opt_num = menu.range_opt_number[1] + 1
            print(f"{back_opt_num}. Back")

        user_input = self.get_int_or_quit("Enter the number: ")

        if user_input == back_opt_num:
            self.start_menu(self.back_Menu())
        else:
            opt = menu.get_opt(int(user_input))

            # if it was a new menu
            # show it
            # if it's a command do it

            if isinstance(opt, Menu):
                self.start_menu(opt)
            else:
                opt.run()
                self.start_menu(menu)

    def get_int_or_quit(self, promt: str) -> int:
        while True:
            user_input: str = input(promt)
            if user_input.lower() == "q":
                print("Bye :)")
                quit()
            if user_input.isdigit():
                return int(user_input)
            else:
                continue

    def print_welcome_message(self) -> None:
        print("""======================================""")
        print("""=========== Welcome There ============""")
        print("""======================================""")
        print("q: Quit")
        print("\n")
