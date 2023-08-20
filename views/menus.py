from views.employee import *
from views.worked_hours import *
from utils.menu import Menu

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

home_menu = Menu("Home Menu", employees_menu, hours_menu)
