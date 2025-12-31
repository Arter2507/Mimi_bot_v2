import discord
from discord.ext import commands
from discord import app_commands

from core.json_store import load_json, save_json
from core.constants import HOLIDAYS_JSON
from core.date_utils import validate_date, normalize_date

async def holiday_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    holidays = load_json(HOLIDAYS_JSON)
    choices = []
    for h in holidays:
        date = h.get('date', '')
        name = h.get('name', 'Unknown')
        label = f"{date} - {name}"
        if current.lower() in label.lower():
            choices.append(app_commands.Choice(name=label, value=date))
        if len(choices) >= 25:  # Discord limit
            break
    return choices


class HolidayCog(commands.Cog, name="Holiday"):
    def __init__(self, bot):
        self.bot = bot

    holiday_group = app_commands.Group(name="holiday", description="Quản lý ngày lễ")

    @holiday_group.command(name="add", description="Thêm ngày lễ mới")
    @app_commands.describe(
        date="Ngày lễ (DD-MM)",
        name="Tên ngày lễ",
        type="Loại lịch"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="Solar (Dương lịch)", value="Solar"),
        app_commands.Choice(name="Lunar (Âm lịch)", value="Lunar")
    ])
    async def add(
        self,
        interaction: discord.Interaction,
        date: str,
        name: str,
        type: app_commands.Choice[str]
    ):
        # Validate date format DD-MM
        if not validate_date(date, type.value):
            await interaction.response.send_message(
                "Định dạng ngày không hợp lệ hoặc ngày không tồn tại. Dùng DD-MM (VD: 01-01)",
                ephemeral=True
            )
            return

        date = normalize_date(date)

        holidays = load_json(HOLIDAYS_JSON)

        # Check duplicate
        for h in holidays:
            if h['date'] == date and h['type'] == type.value:
                await interaction.response.send_message(
                    "Ngày lễ này đã tồn tại!",
                    ephemeral=True
                )
                return

        holidays.append({"date": date, "name": name, "type": type.value})
        save_json(HOLIDAYS_JSON, holidays)
        await interaction.response.send_message(
            f"Đã thêm lễ: {name} ({date} - {type.value})",
            ephemeral=True
        )

    @holiday_group.command(name="remove", description="Xóa ngày lễ")
    @app_commands.describe(date="Ngày lễ cần xóa (DD-MM)")
    @app_commands.autocomplete(date=holiday_autocomplete)
    async def remove(self, interaction: discord.Interaction, date: str):
        holidays = load_json(HOLIDAYS_JSON)
        new_holidays = [h for h in holidays if h['date'] != date]

        if len(holidays) == len(new_holidays):
            await interaction.response.send_message(
                "Không tìm thấy ngày lễ nào trùng khớp để xóa.",
                ephemeral=True
            )
        else:
            save_json(HOLIDAYS_JSON, new_holidays)
            await interaction.response.send_message(
                f"Đã xóa ngày lễ {date}.",
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

    @holiday_group.command(name="update", description="Cập nhật tên ngày lễ")
    @app_commands.describe(
        date="Ngày lễ cần cập nhật (DD-MM)",
        new_name="Tên mới"
    )
    @app_commands.autocomplete(date=holiday_autocomplete)
    async def update(self, interaction: discord.Interaction, date: str, new_name: str):
        holidays = load_json(HOLIDAYS_JSON)
        found = False

        for h in holidays:
            if h['date'] == date:
                h['name'] = new_name
                found = True

        if found:
            save_json(HOLIDAYS_JSON, holidays)
            await interaction.response.send_message(
                f"Đã cập nhật tên ngày lễ {date} thành {new_name}.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Không tìm thấy ngày lễ {date}.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(HolidayCog(bot))
