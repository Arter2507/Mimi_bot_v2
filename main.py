import os
from bot import HolidayBot
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN missing")
    HolidayBot().run(token)
