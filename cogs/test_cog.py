import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

from core.json_store import load_json
from core.constants import BIRTHDAYS_JSON, HOLIDAYS_JSON, JSON_CONFIG
from core.date_utils import get_days_until_solar, get_days_until_lunar, get_age
from views.test_views import (
    TestWishView,
    TestBirthdayView,
    TestCountdownBirthdayView,
    TestWeatherView
)


class TestCog(commands.Cog, name="Test"):
    """Cog quản lý các lệnh test."""
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test", description="Test các chức năng của bot")
    @app_commands.describe(
        function="Chọn chức năng cần test",
        channel="Channel để gửi test (tùy chọn, mặc định dùng channel cấu hình)"
    )
    @app_commands.choices(function=[
        app_commands.Choice(name="Wish - Test gửi lời chúc", value="wish"),
        app_commands.Choice(name="Birthday - Test chúc mừng sinh nhật", value="birthday"),
        app_commands.Choice(name="Countdown Birthday - Test đếm ngược sinh nhật", value="countdown_birthday"),
        app_commands.Choice(name="Countdown Tet - Test đếm ngược Tết", value="countdown_tet"),
        app_commands.Choice(name="Weather - Test thông báo thời tiết", value="weather")
    ])
    async def test(
        self,
        interaction: discord.Interaction,
        function: app_commands.Choice[str],
        channel: Optional[discord.TextChannel] = None
    ):
        """Lệnh test chính với menu chọn function."""
        function_value = function.value
        
        # Lấy channel (ưu tiên channel được chọn, sau đó dùng channel cấu hình)
        target_channel = channel
        if not target_channel:
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id), {})
            channel_id = config.get('channel_id')
            if channel_id:
                target_channel = interaction.guild.get_channel(channel_id)
        
        if not target_channel:
            await interaction.response.send_message(
                "❌ Không tìm thấy channel. Vui lòng chọn channel hoặc cấu hình channel trong `/config setup`.",
                ephemeral=True
            )
            return
        
        # Xử lý theo từng function
        if function_value == "wish":
            view = TestWishView(self.bot, interaction.guild, target_channel)
            await interaction.response.send_message(
                "📋 **Test Wish**\nVui lòng chọn ngày lễ hoặc dùng ngày hiện tại:",
                view=view,
                ephemeral=True
            )
        
        elif function_value == "birthday":
            view = TestBirthdayView(self.bot, interaction.guild, target_channel)
            await interaction.response.send_message(
                "📋 **Test Birthday**\nVui lòng chọn user để test:",
                view=view,
                ephemeral=True
            )
        
        elif function_value == "countdown_birthday":
            view = TestCountdownBirthdayView(self.bot, interaction.guild, target_channel)
            await interaction.response.send_message(
                "📋 **Test Countdown Birthday**\nVui lòng chọn user để test:",
                view=view,
                ephemeral=True
            )
        
        elif function_value == "countdown_tet":
            await interaction.response.send_message(
                "🔄 Đang gửi test countdown Tết...",
                ephemeral=True
            )
            await self.bot.send_tet_countdown_report(interaction.guild)
            await interaction.followup.send(
                "✅ Đã gửi test countdown Tết!",
                ephemeral=True
            )
        
        elif function_value == "weather":
            view = TestWeatherView(self.bot, interaction.guild, target_channel)
            await interaction.response.send_message(
                "📋 **Test Weather**\nĐang kiểm tra cấu hình thời tiết...",
                view=view,
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(TestCog(bot))
