from views.interface import Interface
from dotenv import load_dotenv
from views import options

if __name__ == "__main__":
    load_dotenv()
    inter = Interface(options.home_menu)
    inter.start()
