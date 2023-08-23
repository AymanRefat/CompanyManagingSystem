from views.employee import *
from views.worked_hours import *
from utils.menu import Menu
from views.rewards import *


hours_menu = Menu(
    "Hours",
    ShowWorkedHours,
    ShowTotalHoursForAll,
    addWorkedHoursForAll,
    addWorkedHoursForEmployee,
    DeleteWorkedHoursForEmployee,
)

employees_menu = Menu(
    "Employees",
    ShowAllEmployeesOpt,
    CreateNewEmployeesOpt,
    DeleteEmployeesOpt,
    UpdateEmployeesOpt,
)

rewards_menu = Menu("Rewards", ShowAllRewards, CreateReward, DeleteReward)

home_menu = Menu("Home Menu", employees_menu, hours_menu, rewards_menu)
