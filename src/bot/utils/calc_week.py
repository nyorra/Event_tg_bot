import math
from datetime import date


def calculate_current_week() -> int:
    start_date = date(2025, 10, 1)
    today = date.today()
    delta_days = (today - start_date).days

    if delta_days < 0:
        return 0

    current_week = math.floor(delta_days / 7) + 1
    return current_week
