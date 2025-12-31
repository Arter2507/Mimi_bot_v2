import discord
from discord.ext import commands
from discord import app_commands

from core.json_store import load_json, save_json
from core.constants import BIRTHDAYS_JSON
from core.date_utils import validate_date, normalize_date
from views.birthday_manage_view import BirthdayRemoveView, BirthdayUpdateView


class BirthdayCog(commands.Cog, name="Birthday"):
    def __init__(self, bot):
        self.bot = bot

    birthday_group = app_commands.Group(name="birthday", description="Quản lý sinh nhật")

    @birthday_group.command(name="add", description="Thêm sinh nhật mới (DD-MM-YYYY)")
    @app_commands.describe(
        date="Ngày sinh (DD-MM-YYYY)",
        user="User (Mặc định: Bạn)",
        type="Loại lịch (Mặc định: Solar)"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="Solar", value="Solar"),
        app_commands.Choice(name="Lunar", value="Lunar")
    ])
    async def add(
        self,
        interaction: discord.Interaction,
        date: str,
        user: discord.User = None,
        type: app_commands.Choice[str] = None
    ):
        target_user = user or interaction.user
        date_type = type.value if type else "Solar"

        # Validate date format DD-MM-YYYY
        if not validate_date(date, date_type):
            await interaction.response.send_message(
                "Định dạng ngày không hợp lệ hoặc ngày không tồn tại. Dùng DD-MM-YYYY (VD: 01-01-1999).",
                ephemeral=True
            )
            return

        date = normalize_date(date)

        birthdays = load_json(BIRTHDAYS_JSON)
        birthdays.append({
            "user_id": target_user.id,
            "user_name": target_user.name,
            "date": date,
            "type": date_type
        })
        save_json(BIRTHDAYS_JSON, birthdays)
        await interaction.response.send_message(
            f"Đã thêm sinh nhật cho {target_user.name} ({date} - {date_type})",
            ephemeral=True
        )

    @birthday_group.command(name="list", description="Xem danh sách sinh nhật")
    async def list_bd(self, interaction: discord.Interaction):
        birthdays = load_json(BIRTHDAYS_JSON)

        if not birthdays:
            await interaction.response.send_message("Danh sách trống.", ephemeral=True)
            return

        desc = ""
        for b in birthdays:
            desc += f"- <@{b['user_id']}>: {b['date']} ({b['type']})\n"

        embed = discord.Embed(
            title="Danh sách Sinh nhật",
            description=desc,
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @birthday_group.command(name="remove", description="Xóa sinh nhật")
    async def remove(self, interaction: discord.Interaction):
        view = BirthdayRemoveView()
        await interaction.response.send_message(
            "Chọn sinh nhật cần xóa:",
            view=view,
            ephemeral=True
        )

    @birthday_group.command(name="update", description="Cập nhật sinh nhật (tên người và ngày)")
    async def update(self, interaction: discord.Interaction):
        view = BirthdayUpdateView()
        await interaction.response.send_message(
            "Chọn sinh nhật cần cập nhật:",
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
