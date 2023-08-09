def get_salary_by_hours(
    hours_worked: float,
    hour_price: float,
    award: float = 0,
) -> float:
    return hours_worked * hour_price + award
