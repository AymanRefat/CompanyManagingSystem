from app.interface import Interface
from dotenv import load_dotenv
from app import menus_struct

if __name__ == "__main__":
    load_dotenv()
    inter = Interface(menus_struct.home_menu)
    inter.start()
