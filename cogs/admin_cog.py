import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Union
import os
import sys
import subprocess
import asyncio
import json
from datetime import datetime

from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG
from modals.announcement_modal import AnnouncementModal

# File để lưu thông tin restart
RESTART_INFO_FILE = "restart_info.json"


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Kiểm tra latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms")

    @app_commands.command(name="restart", description="Khởi động lại bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def restart(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔄 Đang khởi động lại...")
        os.execv(sys.executable, ['python'] + sys.argv)

    @app_commands.command(name="stop", description="Tắt bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("⏹️ Đang tắt bot...")
        await self.bot.close()

    @app_commands.command(name="sync", description="Sync slash commands")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync()
        await interaction.followup.send(f"✅ Đã sync {len(synced)} commands!")

    @app_commands.command(name="clear_cache", description="Xóa cache, reset commands và khởi động lại")
    @app_commands.describe(channel="Kênh để gửi log quá trình (tùy chọn)")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear_cache(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel] = None
    ):
        # Use provided channel or get from config
        log_channel = channel
        if not log_channel:
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
            if config and config.get('channel_id'):
                log_channel = self.bot.get_channel(int(config['channel_id']))

        await interaction.response.send_message(
            "🔄 Bắt đầu xóa cache và reset commands...",
            ephemeral=True
        )

        # Send initial message to log channel
        if log_channel:
            await log_channel.send("🔄 **Bắt đầu xóa cache...**")

        # Run reset_commands.py
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reset_script = os.path.join(base_dir, "reset_commands.py")

            if log_channel:
                await log_channel.send("📤 Đang chạy `reset_commands.py`...")

            # Run subprocess and capture output
            process = await asyncio.create_subprocess_exec(
                sys.executable, reset_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=base_dir
            )

            stdout, _ = await process.communicate()
            output = stdout.decode('utf-8', errors='replace')

            if log_channel:
                # Send output in code block
                if len(output) > 1900:
                    output = output[:1900] + "..."
                await log_channel.send(f"```\n{output}\n```")
                await log_channel.send("✅ **Reset commands hoàn tất!**")
                await log_channel.send("🔄 **Đang khởi động lại bot...**")
                
                # Lưu thông tin restart để kiểm tra sau khi bot khởi động lại
                restart_info = {
                    "guild_id": str(interaction.guild_id),
                    "channel_id": log_channel.id,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": interaction.user.id,
                    "user_name": str(interaction.user)
                }
                try:
                    with open(RESTART_INFO_FILE, 'w', encoding='utf-8') as f:
                        json.dump(restart_info, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"Lỗi khi lưu restart info: {e}")

        except Exception as e:
            if log_channel:
                await log_channel.send(f"❌ Lỗi: {e}")

        # Restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)

    @app_commands.command(name="announcement", description="Tạo thông báo")
    @app_commands.describe(
        channel="Chọn kênh để gửi (Mặc định: Kênh cấu hình)",
        mention="Chọn User/Role để mention trong nội dung"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def announcement(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel] = None,
        mention: Optional[Union[discord.Role, discord.User, discord.Member]] = None
    ):
        target_channel = channel
        if not target_channel:
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
            if config and config.get('channel_id'):
                target_channel = self.bot.get_channel(int(config['channel_id']))

        if target_channel:
            await interaction.response.send_modal(AnnouncementModal(target_channel, mention))
        else:
            await interaction.response.send_message(
                "Không tìm thấy channel cấu hình và không có channel được chọn.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
