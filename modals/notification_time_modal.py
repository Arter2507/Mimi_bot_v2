import discord
from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG


class NotificationTimeModal(discord.ui.Modal, title="Cấu hình thời gian thông báo"):
    """Modal để cấu hình thời gian gửi thông báo hằng ngày."""
    
    time_input = discord.ui.TextInput(
        label="Thời gian (HH:MM, 24h format)",
        placeholder="VD: 06:00, 07:30, 08:00",
        default="06:00",
        required=True,
        max_length=5,
        min_length=5
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        time_str = self.time_input.value.strip()
        
        # Validate format HH:MM
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            hour = int(parts[0])
            minute = int(parts[1])
            
            if hour < 0 or hour > 23:
                await interaction.response.send_message(
                    "❌ Giờ phải từ 00 đến 23.",
                    ephemeral=True
                )
                return
            
            if minute < 0 or minute > 59:
                await interaction.response.send_message(
                    "❌ Phút phải từ 00 đến 59.",
                    ephemeral=True
                )
                return
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Định dạng không hợp lệ. Vui lòng nhập theo format HH:MM (VD: 06:00).",
                ephemeral=True
            )
            return
        
        # Save to config
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        if gid not in data:
            data[gid] = {}
        
        data[gid]["notification_time"] = {
            "hour": hour,
            "minute": minute
        }
        
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            f"✅ Đã cấu hình thời gian thông báo: **{hour:02d}:{minute:02d}**\n"
            f"Bot sẽ gửi thông báo (lời chúc, thời tiết) vào lúc này mỗi ngày.",
            ephemeral=True
        )
