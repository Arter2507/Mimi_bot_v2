from datetime import datetime, date as dt_date
from lunardate import LunarDate

def get_solar_date():
    return datetime.now().strftime("%d-%m")

def get_lunar_date():
    d = datetime.now()
    l = LunarDate.fromSolarDate(d.year, d.month, d.day)
    return f"{l.day:02d}-{l.month:02d}"

def get_days_until_solar(date_str):
    d, m = map(int, date_str.split("-")[:2])
    today = datetime.now().date()
    target = dt_date(today.year, m, d)
    if target < today:
        target = dt_date(today.year + 1, m, d)
    return (target - today).days

def get_days_until_lunar(date_str):
    d, m = map(int, date_str.split("-")[:2])
    today = datetime.now().date()
    today_l = LunarDate.fromSolarDate(today.year, today.month, today.day)
    target_l = LunarDate(today_l.year, m, d)
    target_s = target_l.toSolarDate()
    if target_s < today:
        target_s = LunarDate(today_l.year + 1, m, d).toSolarDate()
    return (target_s - today).days

def get_age(date_str, kind):
    parts = list(map(int, date_str.split("-")))
    if len(parts) < 3:
        return "?"
    _, _, year = parts
    if kind == "Solar":
        return datetime.now().year - year
    l = LunarDate.fromSolarDate(datetime.now().year, datetime.now().month, datetime.now().day)
    return l.year - year


def is_today(date_str, date_type):
    """Check if the given date matches today."""
    if date_type == "Solar":
        return date_str == get_solar_date() or date_str.startswith(get_solar_date())
    else:
        return date_str == get_lunar_date() or date_str.startswith(get_lunar_date())


def days_until(date_str, date_type):
    """Get days until the given date."""
    if date_type == "Solar":
        return get_days_until_solar(date_str)
    else:
        return get_days_until_lunar(date_str)

