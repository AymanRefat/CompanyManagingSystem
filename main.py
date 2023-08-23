from views.interface import Interface
from models.funcs import create_tabels
from dotenv import load_dotenv
from views import menus
from settings import SESSION_MAKER, DB_ENGINE

if __name__ == "__main__":
    load_dotenv()
    create_tabels(DB_ENGINE)
    inter = Interface(menus.home_menu, SESSION_MAKER)
    inter.start()
