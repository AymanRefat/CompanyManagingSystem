from views.interface import Interface
from dotenv import load_dotenv
from views import menus
from settings import SESSION_MAKER

if __name__ == "__main__":
    load_dotenv()
    inter = Interface(menus.home_menu, SESSION_MAKER)
    inter.start()
