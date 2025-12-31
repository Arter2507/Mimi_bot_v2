import discord
from discord.ext import commands
from discord import app_commands
import json
import os

from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG
from modals.config_setup import ConfigSetupModal
from modals.countdown_config import CountdownConfigModal


class ConfigCog(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    config_group = app_commands.Group(name="config", description="Quản lý cấu hình bot")

    @config_group.command(name="setup", description="Thiết lập cấu hình ban đầu")
    async def setup(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ConfigSetupModal())

    @config_group.command(name="view", description="Xem cấu hình hiện tại")
    async def view(self, interaction: discord.Interaction):
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
        if not config:
            await interaction.response.send_message(
                "Server chưa được cấu hình. Vui lòng dùng `/config setup`.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title="Cấu hình hiện tại", color=discord.Color.green())
        embed.add_field(name="Channel ID", value=config.get('channel_id'), inline=False)
        embed.add_field(name="Role ID", value=config.get('role_id') or "None", inline=False)
        embed.add_field(name="Wish Type", value=config.get('wish_type'), inline=False)
        embed.add_field(name="Template", value=config.get('content_template'), inline=False)

        # Show countdown config if exists
        cd = config.get('countdown', {})
        if cd:
            embed.add_field(name="Countdown Frequency", value=cd.get('frequency', 'N/A'), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @config_group.command(name="delete", description="Xóa toàn bộ cấu hình")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete(self, interaction: discord.Interaction):
        data = load_json(JSON_CONFIG)
        if str(interaction.guild_id) in data:
            del data[str(interaction.guild_id)]
            save_json(JSON_CONFIG, data)
            await interaction.response.send_message("Đã xóa cấu hình server.", ephemeral=True)
        else:
            await interaction.response.send_message("Không tìm thấy cấu hình để xóa.", ephemeral=True)

    @config_group.command(name="export", description="Xuất cấu hình ra file JSON")
    async def export(self, interaction: discord.Interaction):
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
        if not config:
            await interaction.response.send_message("Không có cấu hình để xuất.", ephemeral=True)
            return

        # Create temp file
        backup_path = 'backup_config.json'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        await interaction.response.send_message(
            "File backup cấu hình:",
            file=discord.File(backup_path),
            ephemeral=True
        )
        os.remove(backup_path)

    @config_group.command(name="import", description="Nhập cấu hình từ file JSON")
    @app_commands.describe(file="File JSON chứa cấu hình")
    async def import_config(self, interaction: discord.Interaction, file: discord.Attachment):
        if not file.filename.endswith('.json'):
            await interaction.response.send_message("Vui lòng tải lên file .json", ephemeral=True)
            return

        try:
            data = await file.read()
            config_data = json.loads(data.decode('utf-8'))

            # Validate keys
            required_keys = ["channel_id", "wish_type", "content_template"]
            if not all(k in config_data for k in required_keys):
                await interaction.response.send_message(
                    "File JSON không hợp lệ (thiếu key).",
                    ephemeral=True
                )
                return

            all_configs = load_json(JSON_CONFIG)
            all_configs[str(interaction.guild_id)] = config_data
            save_json(JSON_CONFIG, all_configs)
            await interaction.response.send_message("Đã khôi phục cấu hình thành công!", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Lỗi khi nhập file: {e}", ephemeral=True)

    @config_group.command(name="countdown", description="Cấu hình thông báo đếm ngược")
    async def countdown(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CountdownConfigModal())


async def setup(bot):
    await bot.add_cog(ConfigCog(bot))
