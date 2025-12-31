import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from typing import List
import pytz

from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG
from core.weather_service import get_weather
from views.weather_channel_view import WeatherChannelView
from modals.weather_location_modal import WeatherLocationModal, WeatherUpdateModal


class WeatherCog(commands.Cog, name="Weather"):
    """Cog quản lý thông báo thời tiết hằng ngày."""
    
    def __init__(self, bot):
        self.bot = bot
    
    weather_group = app_commands.Group(name="weather", description="Quản lý thông báo thời tiết")
    
    @weather_group.command(name="setup", description="Cấu hình channel nhận thông báo thời tiết")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """Hiển thị view để chọn channel."""
        view = WeatherChannelView()
        await interaction.response.send_message(
            "📋 **Cấu hình channel thông báo thời tiết**\n"
            "Vui lòng chọn channel nhận thông báo thời tiết:",
            view=view,
            ephemeral=True
        )
    
    @weather_group.command(name="add", description="Thêm vị trí thời tiết")
    @app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction):
        """Thêm vị trí thời tiết mới."""
        await interaction.response.send_modal(WeatherLocationModal())
    
    @weather_group.command(name="list", description="Xem danh sách vị trí thời tiết")
    async def list(self, interaction: discord.Interaction):
        """Xem danh sách vị trí thời tiết."""
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
        weather_config = config.get("weather")
        
        if not weather_config:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết. Vui lòng dùng `/weather setup`.",
                ephemeral=True
            )
            return
        
        locations = weather_config.get("locations", [])
        channel_id = weather_config.get("channel_id")
        enabled = weather_config.get("enabled", True)
        
        embed = discord.Embed(
            title="🌤️ Danh sách vị trí thời tiết",
            color=discord.Color.blue()
        )
        
        if not locations:
            embed.description = "📭 Chưa có vị trí nào được thêm.\n💡 Sử dụng `/weather add` để thêm vị trí."
        else:
            locations_text = "\n".join([f"{i+1}. 📍 {loc}" for i, loc in enumerate(locations)])
            embed.description = locations_text
            embed.add_field(name="📊 Tổng số", value=f"{len(locations)} vị trí", inline=True)
        
        if channel_id:
            channel = interaction.guild.get_channel(channel_id)
            channel_name = channel.mention if channel else f"Channel ID: {channel_id}"
            embed.add_field(name="📺 Channel", value=channel_name, inline=True)
        else:
            embed.add_field(name="📺 Channel", value="Chưa cấu hình", inline=True)
        
        embed.add_field(name="✅ Trạng thái", value="Bật" if enabled else "Tắt", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @weather_group.command(name="update", description="Cập nhật vị trí thời tiết")
    @app_commands.describe(location="Vị trí cần cập nhật (chọn từ danh sách)")
    @app_commands.checks.has_permissions(administrator=True)
    async def update(
        self,
        interaction: discord.Interaction,
        location: str
    ):
        """Cập nhật vị trí thời tiết."""
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
        weather_config = config.get("weather")
        
        if not weather_config:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết.",
                ephemeral=True
            )
            return
        
        locations = weather_config.get("locations", [])
        
        if location not in locations:
            await interaction.response.send_message(
                f"❌ Không tìm thấy vị trí '{location}' trong danh sách.\n"
                f"💡 Sử dụng `/weather list` để xem danh sách vị trí.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_modal(WeatherUpdateModal(location))
    
    @update.autocomplete('location')
    async def update_location_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete cho lệnh update."""
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
        weather_config = config.get("weather", {})
        locations = weather_config.get("locations", [])
        
        choices = [
            app_commands.Choice(name=loc, value=loc)
            for loc in locations
            if current.lower() in loc.lower()
        ][:25]  # Giới hạn 25 choices
        
        return choices
    
    @weather_group.command(name="delete", description="Xóa vị trí thời tiết")
    @app_commands.describe(location="Vị trí cần xóa (chọn từ danh sách)")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete(
        self,
        interaction: discord.Interaction,
        location: str
    ):
        """Xóa vị trí thời tiết."""
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        if gid not in data or "weather" not in data[gid]:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết.",
                ephemeral=True
            )
            return
        
        locations = data[gid]["weather"].get("locations", [])
        
        if location not in locations:
            await interaction.response.send_message(
                f"❌ Không tìm thấy vị trí '{location}' trong danh sách.\n"
                f"💡 Sử dụng `/weather list` để xem danh sách vị trí.",
                ephemeral=True
            )
            return
        
        # Xóa vị trí
        locations.remove(location)
        data[gid]["weather"]["locations"] = locations
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            f"✅ Đã xóa vị trí: **{location}**\n"
            f"📋 Còn lại: {len(locations)} vị trí",
            ephemeral=True
        )
    
    @delete.autocomplete('location')
    async def delete_location_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete cho lệnh delete."""
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
        weather_config = config.get("weather", {})
        locations = weather_config.get("locations", [])
        
        choices = [
            app_commands.Choice(name=loc, value=loc)
            for loc in locations
            if current.lower() in loc.lower()
        ][:25]  # Giới hạn 25 choices
        
        return choices
    
    @weather_group.command(name="view", description="Xem cấu hình thời tiết hiện tại")
    async def view(self, interaction: discord.Interaction):
        """Xem cấu hình thời tiết hiện tại."""
        config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
        weather_config = config.get("weather")
        
        if not weather_config:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết. Vui lòng dùng `/weather setup`.",
                ephemeral=True
            )
            return
        
        locations = weather_config.get("locations", [])
        channel_id = weather_config.get("channel_id")
        enabled = weather_config.get("enabled", True)
        
        embed = discord.Embed(
            title="🌤️ Cấu hình thời tiết",
            color=discord.Color.blue()
        )
        
        if locations:
            locations_text = "\n".join([f"📍 {loc}" for loc in locations])
            embed.add_field(name="Vị trí", value=locations_text or "Chưa có", inline=False)
        else:
            embed.add_field(name="Vị trí", value="Chưa có vị trí nào", inline=False)
        
        if channel_id:
            channel = interaction.guild.get_channel(channel_id)
            channel_name = channel.mention if channel else f"Channel ID: {channel_id}"
            embed.add_field(name="📺 Channel", value=channel_name, inline=False)
        else:
            embed.add_field(name="📺 Channel", value="Chưa cấu hình", inline=False)
        
        embed.add_field(name="✅ Trạng thái", value="Bật" if enabled else "Tắt", inline=False)
        embed.add_field(name="📊 Tổng số vị trí", value=str(len(locations)), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    

    
    @weather_group.command(name="disable", description="Tắt thông báo thời tiết")
    @app_commands.checks.has_permissions(administrator=True)
    async def disable(self, interaction: discord.Interaction):
        """Tắt thông báo thời tiết."""
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        if gid not in data or "weather" not in data[gid]:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết.",
                ephemeral=True
            )
            return
        
        data[gid]["weather"]["enabled"] = False
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            "✅ Đã tắt thông báo thời tiết.",
            ephemeral=True
        )
    
    @weather_group.command(name="enable", description="Bật thông báo thời tiết")
    @app_commands.checks.has_permissions(administrator=True)
    async def enable(self, interaction: discord.Interaction):
        """Bật thông báo thời tiết."""
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        if gid not in data or "weather" not in data[gid]:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết. Vui lòng dùng `/weather setup`.",
                ephemeral=True
            )
            return
        
        data[gid]["weather"]["enabled"] = True
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            "✅ Đã bật thông báo thời tiết.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
