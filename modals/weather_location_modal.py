import discord
from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG


class WeatherLocationModal(discord.ui.Modal, title="Thêm vị trí thời tiết"):
    """Modal để thêm vị trí thời tiết."""
    
    location = discord.ui.TextInput(
        label="Vị trí thời tiết",
        placeholder="Ví dụ: Hanoi, Ho Chi Minh City, Da Nang...",
        required=True,
        max_length=100
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Xử lý khi submit modal."""
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
        
        # Khởi tạo locations nếu chưa có
        if "locations" not in data[gid]["weather"]:
            data[gid]["weather"]["locations"] = []
        
        # Kiểm tra trùng lặp
        locations = data[gid]["weather"]["locations"]
        if self.location.value in locations:
            await interaction.response.send_message(
                f"❌ Vị trí '{self.location.value}' đã tồn tại trong danh sách.",
                ephemeral=True
            )
            return
        
        # Thêm vị trí mới
        locations.append(self.location.value)
        data[gid]["weather"]["locations"] = locations
        
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            f"✅ Đã thêm vị trí: **{self.location.value}**\n"
            f"📋 Tổng số vị trí: {len(locations)}",
            ephemeral=True
        )


class WeatherUpdateModal(discord.ui.Modal, title="Cập nhật vị trí thời tiết"):
    """Modal để cập nhật vị trí thời tiết."""
    
    def __init__(self, old_location: str):
        super().__init__()
        self.old_location = old_location
        # Set default value cho TextInput
        self.new_location = discord.ui.TextInput(
            label="Vị trí thời tiết mới",
            placeholder="Ví dụ: Hanoi, Ho Chi Minh City, Da Nang...",
            required=True,
            max_length=100,
            default=old_location
        )
        self.add_item(self.new_location)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Xử lý khi submit modal."""
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)
        
        if gid not in data or "weather" not in data[gid]:
            await interaction.response.send_message(
                "❌ Chưa cấu hình thông báo thời tiết.",
                ephemeral=True
            )
            return
        
        locations = data[gid]["weather"].get("locations", [])
        
        if self.old_location not in locations:
            await interaction.response.send_message(
                f"❌ Không tìm thấy vị trí '{self.old_location}' trong danh sách.",
                ephemeral=True
            )
            return
        
        # Kiểm tra trùng lặp (nếu tên mới khác tên cũ)
        if self.new_location.value != self.old_location and self.new_location.value in locations:
            await interaction.response.send_message(
                f"❌ Vị trí '{self.new_location.value}' đã tồn tại trong danh sách.",
                ephemeral=True
            )
            return
        
        # Cập nhật vị trí
        index = locations.index(self.old_location)
        locations[index] = self.new_location.value
        data[gid]["weather"]["locations"] = locations
        
        save_json(JSON_CONFIG, data)
        
        await interaction.response.send_message(
            f"✅ Đã cập nhật vị trí:\n"
            f"📍 Cũ: {self.old_location}\n"
            f"📍 Mới: **{self.new_location.value}**",
            ephemeral=True
        )

