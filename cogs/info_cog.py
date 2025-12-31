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
            title="Mimi Bot",
            description="Bot gửi lời chúc tự động vào ngày lễ và sinh nhật.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Language", value="Python 3.8+ (discord.py)", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Hướng dẫn sử dụng bot")
    async def help_cmd(self, interaction: discord.Interaction):
        is_admin = interaction.user.guild_permissions.administrator
        
        # === EMBED 1: TỔNG QUAN ===
        embed_overview = discord.Embed(
            title="📖 Hướng dẫn sử dụng Mimi Bot",
            description=(
                "Mimi Bot giúp gửi lời chúc tự động cho ngày lễ, sinh nhật và thông báo thời tiết.\n\n"
                "**💡 Placeholders có thể dùng trong template:**\n"
                "```\n"
                "{user}         - Mention user\n"
                "{user_name}    - Tên user\n"
                "{date_name}    - Tên ngày lễ/sinh nhật\n"
                "{date}         - Ngày (DD-MM)\n"
                "{time}         - Giờ hiện tại\n"
                "{role_mention} - Mention role cấu hình\n"
                "{everyone}     - @everyone\n"
                "{here}         - @here\n"
                "{guild}        - Tên server\n"
                "{days}         - Số ngày còn lại (countdown)\n"
                "{age}          - Tuổi (sinh nhật)\n"
                "```"
            ),
            color=discord.Color.green()
        )
        
        # === EMBED 2: LỆNH ADMIN ===
        embed_admin = discord.Embed(
            title="🔐 Lệnh dành cho Admin",
            color=discord.Color.red()
        )
        
        embed_admin.add_field(
            name="⚙️ Cấu hình Bot (`/config [function]`)",
            value=(
                "`/config Setup` - Thiết lập (hỗ trợ `Wish Type` = AI)\n"
                "`/config View` - Xem cấu hình hiện tại\n"
                "`/config Delete` - Xóa toàn bộ cấu hình\n"
                "`/config Export` / `Import` - Backup/restore\n"
                "`/config Countdown` - Cấu hình đếm ngược (flexible days)\n"
                "`/config Log Channel` - Channel log\n"
                "`/config Notification Time` - Giờ gửi thông báo\n"
                "`/config Language` - Đổi ngôn ngữ (Vietnamese/English) 🆕"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="📅 Quản lý Ngày lễ (`/holiday`)",
            value=(
                "`/holiday add` - Thêm ngày lễ mới (modal)\n"
                "`/holiday list` - Xem danh sách ngày lễ\n"
                "`/holiday update` - Cập nhật ngày lễ\n"
                "`/holiday remove` - Xóa ngày lễ"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="🎂 Quản lý Sinh nhật (`/birthday`)",
            value=(
                "`/birthday add [date] [user] [type]` - Thêm sinh nhật\n"
                "  → `date`: Ngày sinh (DD-MM-YYYY)\n"
                "  → `user`: User (mặc định: bạn)\n"
                "  → `type`: Solar/Lunar (mặc định: Solar)\n"
                "`/birthday list` - Xem danh sách sinh nhật\n"
                "`/birthday update` - Cập nhật sinh nhật\n"
                "`/birthday remove` - Xóa sinh nhật"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="🌤️ Thời tiết (`/weather`)",
            value=(
                "`/weather setup` - Chọn channel gửi thông báo\n"
                "`/weather add` - Thêm vị trí thời tiết\n"
                "`/weather list` - Xem danh sách vị trí\n"
                "`/weather update [location]` - Cập nhật vị trí\n"
                "`/weather delete [location]` - Xóa vị trí\n"
                "`/weather view` - Xem cấu hình thời tiết\n"
                "`/weather test` - Test thông báo thời tiết\n"
                "`/weather enable` / `disable` - Bật/tắt thông báo"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="🧹 Xóa tin nhắn (`/clear`)",
            value=(
                "`/clear message [amount] [time] [channel] [user]`\n"
                "  → `amount`: Số tin nhắn (1-100, mặc định: 10)\n"
                "  → `time`: Khoảng thời gian (VD: 7d, 24h, 30m)\n"
                "  → `channel`: Kênh xóa (mặc định: kênh hiện tại)\n"
                "  → `user`: User cần xóa (chỉ admin)"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="📢 Thông báo",
            value=(
                "`/announcement [channel] [mention]` - Tạo thông báo\n"
                "  → `channel`: Channel gửi (mặc định: channel cấu hình)\n"
                "  → `mention`: User/Role để mention"
            ),
            inline=False
        )
        
        embed_admin.add_field(
            name="🧪 Test các chức năng (`/test`)",
            value=(
                "`/test [function] [channel]` - Test chức năng bot\n"
                "  → `function`: wish, birthday, countdown_birthday,\n"
                "     countdown_tet, weather\n"
                "  → `channel`: Channel gửi test (tùy chọn)"
            ),
            inline=False
        )
        
        # === EMBED 3: LỆNH USER ===
        embed_user = discord.Embed(
            title="👤 Lệnh dành cho User",
            color=discord.Color.blue()
        )
        
        embed_user.add_field(
            name="📊 Thông tin (`/info`)",
            value=(
                "`/info view` - Xem thông tin server\n"
                "`/about` - Thông tin về bot\n"
                "`/help` - Xem hướng dẫn này"
            ),
            inline=False
        )
        
        embed_user.add_field(
            name="🏓 Tiện ích",
            value="`/ping` - Kiểm tra độ trễ của bot",
            inline=False
        )
        
        embed_user.add_field(
            name="📅 Xem danh sách",
            value=(
                "`/holiday list` - Xem danh sách ngày lễ\n"
                "`/birthday list` - Xem danh sách sinh nhật\n"
                "`/weather list` - Xem danh sách vị trí thời tiết"
            ),
            inline=False
        )
        
        embed_user.add_field(
            name="🎂 Thêm sinh nhật cá nhân",
            value="`/birthday add [date]` - Thêm sinh nhật của bạn",
            inline=False
        )
        
        # Send all embeds
        if is_admin:
            await interaction.response.send_message(
                embeds=[embed_overview, embed_admin, embed_user],
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embeds=[embed_overview, embed_user],
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(InfoCog(bot))
