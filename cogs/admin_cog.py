import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Union
from datetime import datetime, timedelta
import asyncio

from core.json_store import load_json
from core.constants import JSON_CONFIG, BIRTHDAYS_JSON
from modals.announcement_modal import AnnouncementModal


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Kiểm tra latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms")

    clear_group = app_commands.Group(name="clear", description="Xóa tin nhắn")

    async def birthday_user_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete cho user từ danh sách birthday."""
        birthdays = load_json(BIRTHDAYS_JSON)
        choices = []
        for b in birthdays:
            user_name = b.get('user_name', 'Unknown')
            user_id = b.get('user_id', '')
            if current.lower() in user_name.lower() or current in str(user_id):
                choices.append(app_commands.Choice(name=user_name, value=str(user_id)))
            if len(choices) >= 25:
                break
        return choices

    @clear_group.command(name="message", description="Xóa tin nhắn của người dùng")
    @app_commands.describe(
        amount="Số lượng tin nhắn cần xóa (mặc định: 10)",
        time="Thời gian (VD: 7d, 24h, 30m) - chỉ xóa tin nhắn trong khoảng thời gian này",
        channel="Kênh cần xóa tin nhắn (mặc định: kênh hiện tại)",
        user="Người dùng cần xóa tin nhắn (mặc định: bạn, chỉ admin mới chọn được user khác)"
    )
    @app_commands.autocomplete(user=birthday_user_autocomplete)
    async def clear_message(
        self,
        interaction: discord.Interaction,
        amount: Optional[int] = 10,
        time: Optional[str] = None,
        channel: Optional[discord.TextChannel] = None,
        user: Optional[str] = None
    ):
        """Xóa tin nhắn của người dùng."""
        await interaction.response.defer(ephemeral=True)
        
        # Kiểm tra quyền manage_messages
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.followup.send("❌ Bạn không có quyền xóa tin nhắn.", ephemeral=True)
            return
        
        # Xác định channel
        target_channel = channel or interaction.channel
        if not isinstance(target_channel, discord.TextChannel):
            await interaction.followup.send("❌ Chỉ có thể xóa tin nhắn trong text channel.", ephemeral=True)
            return
        
        # Kiểm tra quyền bot
        if not target_channel.permissions_for(interaction.guild.me).manage_messages:
            await interaction.followup.send("❌ Bot không có quyền xóa tin nhắn trong channel này.", ephemeral=True)
            return
        
        # Xác định user - chỉ admin mới được chọn user khác
        target_user_id = None
        is_admin = interaction.user.guild_permissions.administrator
        
        if user:
            if not is_admin:
                await interaction.followup.send("❌ Chỉ admin mới được chọn user khác để xóa tin nhắn.", ephemeral=True)
                return
            try:
                target_user_id = int(user)
            except ValueError:
                await interaction.followup.send("❌ User ID không hợp lệ.", ephemeral=True)
                return
        else:
            target_user_id = interaction.user.id
        
        # Parse thời gian
        time_limit = None
        if time:
            try:
                # Parse format: 7d, 24h, 30m, 1w
                time_lower = time.lower()
                if time_lower.endswith('d'):
                    days = int(time_lower[:-1])
                    time_limit = datetime.utcnow() - timedelta(days=days)
                elif time_lower.endswith('h'):
                    hours = int(time_lower[:-1])
                    time_limit = datetime.utcnow() - timedelta(hours=hours)
                elif time_lower.endswith('m'):
                    minutes = int(time_lower[:-1])
                    time_limit = datetime.utcnow() - timedelta(minutes=minutes)
                elif time_lower.endswith('w'):
                    weeks = int(time_lower[:-1])
                    time_limit = datetime.utcnow() - timedelta(weeks=weeks)
                else:
                    await interaction.followup.send("❌ Format thời gian không hợp lệ. Dùng: 7d, 24h, 30m, 1w", ephemeral=True)
                    return
            except ValueError:
                await interaction.followup.send("❌ Format thời gian không hợp lệ.", ephemeral=True)
                return
        
        # Giới hạn amount
        if amount < 1:
            amount = 1
        if amount > 100:
            amount = 100
        
        # Lấy và xóa tin nhắn
        deleted_count = 0
        try:
            # Lấy user object
            target_user = self.bot.get_user(target_user_id)
            if not target_user:
                # Thử lấy từ guild
                target_user = interaction.guild.get_member(target_user_id)
            
            user_name = target_user.name if target_user else f"User {target_user_id}"
            
            # Lấy tin nhắn
            async for message in target_channel.history(limit=200):
                # Kiểm tra user
                if message.author.id != target_user_id:
                    continue
                
                # Kiểm tra thời gian
                if time_limit and message.created_at < time_limit:
                    break
                
                # Xóa tin nhắn
                try:
                    await message.delete()
                    deleted_count += 1
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    pass
                
                # Đủ số lượng
                if deleted_count >= amount:
                    break
                
                # Delay nhỏ để tránh rate limit
                if deleted_count % 5 == 0:
                    await asyncio.sleep(0.5)
            
            # Gửi thông báo kết quả
            if deleted_count > 0:
                await interaction.followup.send(
                    f"✅ Đã xóa {deleted_count} tin nhắn của {user_name} trong {target_channel.mention}.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"ℹ️ Không tìm thấy tin nhắn nào của {user_name} để xóa trong {target_channel.mention}.",
                    ephemeral=True
                )
                
        except Exception as e:
            await interaction.followup.send(
                f"❌ Lỗi khi xóa tin nhắn: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(name="announcement", description="Tạo thông báo")
    @app_commands.describe(
        channel="Chọn kênh để gửi (Mặc định: Kênh cấu hình)",
        mention="Chọn User/Role để mention trong nội dung"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def announcement(
        self,
        interaction: discord.Interaction,
        channel: Optional[discord.TextChannel] = None,
        mention: Optional[Union[discord.Role, discord.User, discord.Member]] = None
    ):
        target_channel = channel
        if not target_channel:
            config = load_json(JSON_CONFIG).get(str(interaction.guild_id))
            if config and config.get('channel_id'):
                target_channel = self.bot.get_channel(int(config['channel_id']))

        if target_channel:
            await interaction.response.send_modal(AnnouncementModal(target_channel, mention))
        else:
            await interaction.response.send_message(
                "Không tìm thấy channel cấu hình và không có channel được chọn.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
