from typing import Any
from datetime import date


def validate_float(value: Any) -> float:
    try:
        return float(value)
    except:
        raise TypeError("the Type of data should be Float")


def validate_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    else:
        raise TypeError("Worked Date should be a date")

# validate_in_list 