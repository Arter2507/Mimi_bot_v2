import discord
from discord.ext import commands
from discord import app_commands


class InfoCog(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot

    info_group = app_commands.Group(name="info", description="Thông tin server")

    @info_group.command(name="view", description="Xem thông tin server cơ bản")
    async def view(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Thông tin Server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="about", description="Thông tin về bot")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Holiday Bot",
            description="Bot gửi lời chúc tự động vào ngày lễ và sinh nhật.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Language", value="Python 3.8+ (discord.py)", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Hướng dẫn sử dụng bot")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Hướng dẫn sử dụng Holiday Bot",
            color=discord.Color.green()
        )

        embed.add_field(name="⚙️ Cấu hình (/config)", value=(
            "- `/config setup`: Cài đặt ban đầu.\n"
            "- `/config countdown`: Cấu hình đếm ngược.\n"
            "- `/config view` / `/config export` / `/config import`.\n"
            "**Placeholders**: `{date_name}`, `{date}`, `{time}`, `{role_mention}`, `{everyone}`, `{here}`, `{guild}`, `{user}`, `{days}`, `{age}`."
        ), inline=False)

        embed.add_field(name="📅 Ngày lễ & Sinh nhật", value=(
            "- `/holiday add [date] [name] [type]`\n"
            "- `/birthday add [date] [user] [type]`\n  (Date: DD-MM-YYYY, User/Type: Optional)\n"
            "- `/holiday list` / `/birthday list`\n"
            "- `/holiday remove` / `/birthday remove`"
        ), inline=False)

        embed.add_field(name="🛠️ Công cụ & Test", value=(
            "- `/test wish`: Test lời chúc.\n"
            "- `/test birthday`: Test sinh nhật (Popup chọn user).\n"
            "- `/test countdown_birthday`: Test đếm ngược sinh nhật.\n"
            "- `/test countdown_tet`: Test đếm ngược Tết.\n"
            "- `/announcement`: Tạo thông báo."
        ), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(InfoCog(bot))
