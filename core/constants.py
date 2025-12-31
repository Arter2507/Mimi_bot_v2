import os
from datetime import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, "json_config")
os.makedirs(JSON_DIR, exist_ok=True)

HOLIDAYS_JSON = os.path.join(JSON_DIR, "holidays.json")
BIRTHDAYS_JSON = os.path.join(JSON_DIR, "birthdays.json")
JSON_CONFIG = os.path.join(JSON_DIR, "server_config.json")

DEFAULT_WISH_TIME = time(hour=6, minute=0, second=0)
