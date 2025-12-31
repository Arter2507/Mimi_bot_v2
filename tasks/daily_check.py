import discord
from discord.ext import tasks
from datetime import datetime, date

from core.json_store import load_json
from core.constants import (
    HOLIDAYS_JSON,
    BIRTHDAYS_JSON,
    JSON_CONFIG
)
from core.date_utils import (
    is_today,
    days_until
)

class DailyCheckTask:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.daily_check.start()

    def cog_unload(self):
        self.daily_check.cancel()

    @tasks.loop(hours=24)
    async def daily_check(self):
        today
