import discord
from discord.ext import commands
from discord import app_commands

from core.json_store import load_json, save_json
from core.constants import BIRTHDAYS_JSON


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
        try:
            day, month, year = map(int, date.split('-'))
            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError
        except:
            await interaction.response.send_message(
                "Định dạng ngày không hợp lệ. Dùng DD-MM-YYYY (VD: 01-01-1999).",
                ephemeral=True
            )
            return

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

    @birthday_group.command(name="remove", description="Xóa sinh nhật theo ngày")
    @app_commands.describe(date="Ngày sinh cần xóa (DD-MM-YYYY)")
    async def remove(self, interaction: discord.Interaction, date: str):
        birthdays = load_json(BIRTHDAYS_JSON)
        new_bd = [b for b in birthdays if b['date'] != date]

        if len(birthdays) == len(new_bd):
            await interaction.response.send_message(
                "Không tìm thấy sinh nhật nào ngày này.",
                ephemeral=True
            )
        else:
            save_json(BIRTHDAYS_JSON, new_bd)
            await interaction.response.send_message(
                f"Đã xóa các sinh nhật ngày {date}.",
                ephemeral=True
            )

    @birthday_group.command(name="update", description="Cập nhật user name cho sinh nhật")
    @app_commands.describe(
        date="Ngày sinh cần cập nhật (DD-MM-YYYY)",
        new_name="Tên mới"
    )
    async def update(self, interaction: discord.Interaction, date: str, new_name: str):
        birthdays = load_json(BIRTHDAYS_JSON)
        found = False

        for b in birthdays:
            if b['date'] == date:
                b['user_name'] = new_name
                found = True

        if found:
            save_json(BIRTHDAYS_JSON, birthdays)
            await interaction.response.send_message(
                f"Đã cập nhật sinh nhật ngày {date}.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Không tìm thấy.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
