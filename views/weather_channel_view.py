import discord
from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG


class ChannelSelect(discord.ui.ChannelSelect):
    """ChannelSelect để chọn channel nhận thông báo thời tiết."""
    
    def __init__(self):
        super().__init__(
            placeholder="Chọn channel nhận thông báo thời tiết...",
            channel_types=[discord.ChannelType.text]
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi người dùng chọn channel."""
        selected_channel = self.values[0] if self.values else None
        
        if not selected_channel:
            await interaction.response.send_message(
                "Vui lòng chọn một channel.", 
                ephemeral=True
            )
            return
        
        # Lưu channel vào config
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        # Khởi tạo config cho guild nếu chưa có
        if gid not in data:
            data[gid] = {}
        
        # Khởi tạo weather config nếu chưa có
        if "weather" not in data[gid]:
            data[gid]["weather"] = {
                "locations": [],
                "enabled": True
            }
        
        # Lưu channel_id
        data[gid]["weather"]["channel_id"] = selected_channel.id
        
        # Đảm bảo locations tồn tại
        if "locations" not in data[gid]["weather"]:
            data[gid]["weather"]["locations"] = []
        
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            f"✅ Đã cấu hình channel nhận thông báo thời tiết!\n"
            f"📺 Channel: {selected_channel.mention}\n"
            f"💡 Sử dụng `/weather add` để thêm vị trí thời tiết.",
            ephemeral=True
        )


class WeatherChannelView(discord.ui.View):
    """View với ChannelSelect để chọn channel nhận thông báo thời tiết."""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ChannelSelect())

