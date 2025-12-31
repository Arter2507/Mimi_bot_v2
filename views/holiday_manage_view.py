import discord
from core.json_store import load_json, save_json
from core.constants import HOLIDAYS_JSON
from core.date_utils import validate_date, normalize_date


class HolidayRemoveSelect(discord.ui.Select):
    """Select menu để chọn holiday cần xóa theo tên."""
    
    def __init__(self):
        holidays = load_json(HOLIDAYS_JSON)
        
        options = []
        for h in holidays:
            name = h.get('name', 'Unknown')
            date = h.get('date', 'N/A')
            h_type = h.get('type', 'Solar')
            # Tạo unique identifier: name|date|type
            value = f"{name}|{date}|{h_type}"
            label = f"{name} ({date} - {h_type})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    description=f"Xóa {name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có ngày lễ nào",
                    value="none",
                    description="Danh sách trống"
                )
            )
        
        super().__init__(
            placeholder="Chọn ngày lễ cần xóa...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message(
                "Không có ngày lễ nào để xóa.",
                ephemeral=True
            )
            return
        
        # Parse value: name|date|type
        parts = self.values[0].split("|")
        if len(parts) != 3:
            await interaction.response.send_message(
                "Lỗi: Không thể xác định ngày lễ.",
                ephemeral=True
            )
            return
        
        name, date, h_type = parts
        
        holidays = load_json(HOLIDAYS_JSON)
        new_holidays = [
            h for h in holidays 
            if not (h['name'] == name and h['date'] == date and h['type'] == h_type)
        ]
        
        if len(holidays) == len(new_holidays):
            await interaction.response.send_message(
                "Không tìm thấy ngày lễ để xóa.",
                ephemeral=True
            )
        else:
            save_json(HOLIDAYS_JSON, new_holidays)
            await interaction.response.send_message(
                f"✅ Đã xóa ngày lễ: **{name}** ({date} - {h_type})",
                ephemeral=True
            )


class HolidayRemoveView(discord.ui.View):
    """View với select menu để xóa holiday."""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(HolidayRemoveSelect())
    
    async def on_timeout(self):
        """Xử lý khi timeout."""
        pass


class HolidayUpdateSelect(discord.ui.Select):
    """Select menu để chọn holiday cần cập nhật theo tên."""
    
    def __init__(self):
        holidays = load_json(HOLIDAYS_JSON)
        
        options = []
        for h in holidays:
            name = h.get('name', 'Unknown')
            date = h.get('date', 'N/A')
            h_type = h.get('type', 'Solar')
            # Tạo unique identifier: name|date|type
            value = f"{name}|{date}|{h_type}"
            label = f"{name} ({date} - {h_type})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    description=f"Cập nhật {name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có ngày lễ nào",
                    value="none",
                    description="Danh sách trống"
                )
            )
        
        super().__init__(
            placeholder="Chọn ngày lễ cần cập nhật...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message(
                "Không có ngày lễ nào để cập nhật.",
                ephemeral=True
            )
            return
        
        # Parse value: name|date|type
        parts = self.values[0].split("|")
        if len(parts) != 3:
            await interaction.response.send_message(
                "Lỗi: Không thể xác định ngày lễ.",
                ephemeral=True
            )
            return
        
        name, date, h_type = parts
        
        # Import modal here to avoid circular import
        from modals.holiday_update_modal import HolidayUpdateModal
        
        modal = HolidayUpdateModal(name, date, h_type)
        await interaction.response.send_modal(modal)


class HolidayUpdateView(discord.ui.View):
    """View với select menu để cập nhật holiday."""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(HolidayUpdateSelect())
    
    async def on_timeout(self):
        """Xử lý khi timeout."""
        pass


