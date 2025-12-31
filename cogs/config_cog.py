import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import json
import os

from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG
from modals.config_setup import ConfigSetupModal
from modals.countdown_config import CountdownConfigModal
from modals.notification_time_modal import NotificationTimeModal


class ConfigCog(commands.Cog, name="Configuration"):
    """Cog quản lý cấu hình bot."""
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Quản lý cấu hình bot")
    @app_commands.describe(
        function="Chọn chức năng cấu hình",
        channel="Channel (cho log_channel)",
        file="File JSON (cho import)"
    )
    @app_commands.choices(function=[
        app_commands.Choice(name="Setup - Thiết lập cấu hình ban đầu", value="setup"),
        app_commands.Choice(name="View - Xem cấu hình hiện tại", value="view"),
        app_commands.Choice(name="Delete - Xóa toàn bộ cấu hình", value="delete"),
        app_commands.Choice(name="Export - Xuất cấu hình ra file JSON", value="export"),
        app_commands.Choice(name="Import - Nhập cấu hình từ file JSON", value="import"),
        app_commands.Choice(name="Countdown - Cấu hình đếm ngược", value="countdown"),
        app_commands.Choice(name="Log Channel - Cấu hình channel log", value="log_channel"),
        app_commands.Choice(name="Notification Time - Thời gian gửi thông báo", value="notification_time"),
        app_commands.Choice(name="Language - Ngôn ngữ (Vietnamese/English)", value="language"),
    ])
    async def config(
        self,
        interaction: discord.Interaction,
        function: app_commands.Choice[str],
        channel: Optional[discord.TextChannel] = None,
        file: Optional[discord.Attachment] = None
    ):
        """Lệnh config tổng hợp với menu chọn function."""
        func = function.value
        
        # === SETUP ===
        if func == "setup":
            await interaction.response.send_modal(ConfigSetupModal())
        
        # === VIEW ===
        elif func == "view":
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
            if not config:
                await interaction.response.send_message(
                    "❌ Server chưa được cấu hình. Vui lòng dùng `/config Setup`.",
                    ephemeral=True
                )
                return

            embed = discord.Embed(title="⚙️ Cấu hình hiện tại", color=discord.Color.green())
            
            # Channel
            ch_id = config.get('channel_id')
            if ch_id:
                ch = interaction.guild.get_channel(int(ch_id))
                embed.add_field(name="📺 Channel", value=ch.mention if ch else f"ID: {ch_id}", inline=True)
            
            # Role
            role_id = config.get('role_id')
            embed.add_field(name="👥 Role ID", value=role_id or "None", inline=True)
            
            # Wish Type
            embed.add_field(name="🎉 Wish Type", value=config.get('wish_type', 'N/A'), inline=True)
            
            # Template
            embed.add_field(name="📝 Template", value=f"```{config.get('content_template', 'N/A')[:100]}```", inline=False)
            
            # Notification Time
            notif_time = config.get('notification_time', {})
            hour = notif_time.get('hour', 6)
            minute = notif_time.get('minute', 0)
            embed.add_field(name="⏰ Thời gian thông báo", value=f"{hour:02d}:{minute:02d}", inline=True)
            
            # Log channel
            log_channel_id = config.get('log_channel_id')
            if log_channel_id:
                log_ch = interaction.guild.get_channel(int(log_channel_id))
                embed.add_field(name="📋 Log Channel", value=log_ch.mention if log_ch else f"ID: {log_channel_id}", inline=True)

            # Countdown
            cd = config.get('countdown', {})
            if cd:
                embed.add_field(name="📆 Countdown Frequency", value=cd.get('frequency', 'N/A'), inline=True)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # === DELETE ===
        elif func == "delete":
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Chỉ admin mới có thể xóa cấu hình.", ephemeral=True)
                return
            
            data = load_json(JSON_CONFIG)
            if str(interaction.guild_id) in data:
                del data[str(interaction.guild_id)]
                save_json(JSON_CONFIG, data)
                await interaction.response.send_message("✅ Đã xóa cấu hình server.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Không tìm thấy cấu hình để xóa.", ephemeral=True)
        
        # === EXPORT ===
        elif func == "export":
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
            if not config:
                await interaction.response.send_message("❌ Không có cấu hình để xuất.", ephemeral=True)
                return

            backup_path = 'backup_config.json'
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            await interaction.response.send_message(
                "📁 File backup cấu hình:",
                file=discord.File(backup_path),
                ephemeral=True
            )
            os.remove(backup_path)
        
        # === IMPORT ===
        elif func == "import":
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Chỉ admin mới có thể import cấu hình.", ephemeral=True)
                return
            
            if not file:
                await interaction.response.send_message(
                    "❌ Vui lòng đính kèm file JSON.\n"
                    "💡 Sử dụng: `/config Import file:your_file.json`",
                    ephemeral=True
                )
                return
            
            if not file.filename.endswith('.json'):
                await interaction.response.send_message("❌ Vui lòng tải lên file .json", ephemeral=True)
                return

            try:
                data = await file.read()
                config_data = json.loads(data.decode('utf-8'))

                required_keys = ["channel_id", "wish_type", "content_template"]
                if not all(k in config_data for k in required_keys):
                    await interaction.response.send_message(
                        "❌ File JSON không hợp lệ (thiếu key).",
                        ephemeral=True
                    )
                    return

                all_configs = load_json(JSON_CONFIG)
                all_configs[str(interaction.guild_id)] = config_data
                save_json(JSON_CONFIG, all_configs)
                await interaction.response.send_message("✅ Đã khôi phục cấu hình thành công!", ephemeral=True)

            except Exception as e:
                await interaction.response.send_message(f"❌ Lỗi khi nhập file: {e}", ephemeral=True)
        
        # === COUNTDOWN ===
        elif func == "countdown":
            await interaction.response.send_modal(CountdownConfigModal())
        
        # === LOG CHANNEL ===
        elif func == "log_channel":
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Chỉ admin mới có thể cấu hình log channel.", ephemeral=True)
                return
            
            if not channel:
                await interaction.response.send_message(
                    "❌ Vui lòng chọn channel.\n"
                    "💡 Sử dụng: `/config Log Channel channel:#your-channel`",
                    ephemeral=True
                )
                return
            
            data = load_json(JSON_CONFIG)
            gid = str(interaction.guild_id)

            if gid not in data:
                data[gid] = {}

            data[gid]["log_channel_id"] = channel.id
            save_json(JSON_CONFIG, data)

            await interaction.response.send_message(
                f"✅ Đã cấu hình log channel: {channel.mention}\n"
                f"📋 Các thông báo về khởi động, tắt, restart và clear cache sẽ được gửi vào đây.",
                ephemeral=True
            )
        
        # === NOTIFICATION TIME ===
        elif func == "notification_time":
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Chỉ admin mới có thể cấu hình thời gian thông báo.", ephemeral=True)
                return
            
            await interaction.response.send_modal(NotificationTimeModal())
        
        # === LANGUAGE ===
        elif func == "language":
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Chỉ admin mới có thể cấu hình ngôn ngữ.", ephemeral=True)
                return
            
            # Simple View with Buttons for Language Selection
            from discord.ui import View, Button
            
            async def set_lang(interaction: discord.Interaction, lang_code: str):
                data = load_json(JSON_CONFIG)
                gid = str(interaction.guild_id)
                if gid not in data:
                    data[gid] = {}
                data[gid]["language"] = lang_code
                save_json(JSON_CONFIG, data)
                
                # Dynamic response based on selected language
                msg = "✅ Đã chuyển sang ngôn ngữ: Tiếng Việt 🇻🇳" if lang_code == "vi" else "✅ Language switched to: English 🇺🇸"
                await interaction.response.send_message(msg, ephemeral=True)

            view = View()
            btn_vi = Button(label="Tiếng Việt 🇻🇳", style=discord.ButtonStyle.primary)
            btn_en = Button(label="English 🇺🇸", style=discord.ButtonStyle.primary)
            
            btn_vi.callback = lambda i: set_lang(i, "vi")
            btn_en.callback = lambda i: set_lang(i, "en")
            
            view.add_item(btn_vi)
            view.add_item(btn_en)
            
            await interaction.response.send_message("Chọn ngôn ngữ / Select Language:", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(ConfigCog(bot))
