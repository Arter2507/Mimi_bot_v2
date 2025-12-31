import discord
from discord.ext import commands
from discord import app_commands

from core.json_store import load_json, save_json
from core.constants import HOLIDAYS_JSON
from core.date_utils import validate_date, normalize_date
from views.holiday_manage_view import HolidayRemoveView, HolidayUpdateView
from modals.holiday_add_modal import HolidayAddModal


class HolidayCog(commands.Cog, name="Holiday"):
    def __init__(self, bot):
        self.bot = bot

    holiday_group = app_commands.Group(name="holiday", description="Quản lý ngày lễ")

    @holiday_group.command(name="add", description="Thêm ngày lễ mới (có thể thêm nhiều ngày)")
    async def add(self, interaction: discord.Interaction):
        modal = HolidayAddModal()
        await interaction.response.send_modal(modal)

    @holiday_group.command(name="remove", description="Xóa ngày lễ")
    async def remove(self, interaction: discord.Interaction):
        view = HolidayRemoveView()
        await interaction.response.send_message(
            "Chọn ngày lễ cần xóa:",
            view=view,
            ephemeral=True
        )

    @holiday_group.command(name="list", description="Xem danh sách ngày lễ")
    async def list_holidays(self, interaction: discord.Interaction):
        holidays = load_json(HOLIDAYS_JSON)

        if not holidays:
            await interaction.response.send_message("Danh sách trống.", ephemeral=True)
            return

        desc = ""
        for h in holidays:
            desc += f"- **{h['date']}** ({h['type']}): {h['name']}\n"

        embed = discord.Embed(
            title="Danh sách Ngày lễ",
            description=desc,
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @holiday_group.command(name="update", description="Cập nhật ngày lễ (tên và ngày)")
    async def update(self, interaction: discord.Interaction):
        view = HolidayUpdateView()
        await interaction.response.send_message(
            "Chọn ngày lễ cần cập nhật:",
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(HolidayCog(bot))
