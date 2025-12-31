# reset_commands.py
import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # có thể None

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


async def clear_and_sync_guild(bot, guild_id: int):
    log(f"Xóa slash command GUILD (ID={guild_id})")
    guild_obj = discord.Object(id=guild_id)
    bot.tree.clear_commands(guild=guild_obj)
    synced = await bot.tree.sync(guild=guild_obj)
    log(f"GUILD sync xong, còn {len(synced)} command")


async def clear_and_sync_global(bot):
    log("Xóa slash command GLOBAL")
    bot.tree.clear_commands(guild=None)
    synced = await bot.tree.sync()
    log(f"GLOBAL sync xong, còn {len(synced)} command")


@bot.event
async def on_ready():
    log(f"Bot đăng nhập: {bot.user} (ID={bot.user.id})")
    log(f"Ping: {round(bot.latency * 1000)} ms")

    try:
        if GUILD_ID:
            await clear_and_sync_guild(bot, int(GUILD_ID))
        else:
            log("Không có GUILD_ID, bỏ qua reset guild")

        await clear_and_sync_global(bot)

        log("Reset slash command hoàn tất")
    except Exception as e:
        log(f"LỖI: {e}")
    finally:
        log("Đóng bot reset... Vui lòng chạy 'py main.py' để khởi động lại bot.")
        await bot.close()


if __name__ == "__main__":
    log("Khởi động reset slash command")
    asyncio.run(bot.start(DISCORD_TOKEN))
