import discord
from core.json_store import load_json, save_json
from core.constants import BIRTHDAYS_JSON


class BirthdayRemoveSelect(discord.ui.Select):
    """Select menu để chọn birthday cần xóa theo tên người."""
    
    def __init__(self):
        birthdays = load_json(BIRTHDAYS_JSON)
        
        options = []
        for b in birthdays:
            user_name = b.get('user_name', 'Unknown')
            user_id = b.get('user_id', '')
            date = b.get('date', 'N/A')
            b_type = b.get('type', 'Solar')
            # Tạo unique identifier: user_id|date|type
            value = f"{user_id}|{date}|{b_type}"
            label = f"{user_name} ({date} - {b_type})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    description=f"Xóa sinh nhật của {user_name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có sinh nhật nào",
                    value="none",
                    description="Danh sách trống"
                )
            )
        
        super().__init__(
            placeholder="Chọn sinh nhật cần xóa...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message(
                "Không có sinh nhật nào để xóa.",
                ephemeral=True
            )
            return
        
        # Parse value: user_id|date|type
        parts = self.values[0].split("|")
        if len(parts) != 3:
            await interaction.response.send_message(
                "Lỗi: Không thể xác định sinh nhật.",
                ephemeral=True
            )
            return
        
        user_id, date, b_type = parts
        
        birthdays = load_json(BIRTHDAYS_JSON)
        new_birthdays = [
            b for b in birthdays 
            if not (str(b.get('user_id', '')) == user_id and b['date'] == date and b['type'] == b_type)
        ]
        
        if len(birthdays) == len(new_birthdays):
            await interaction.response.send_message(
                "Không tìm thấy sinh nhật để xóa.",
                ephemeral=True
            )
        else:
            # Tìm tên người để hiển thị
            user_name = "Unknown"
            for b in birthdays:
                if str(b.get('user_id', '')) == user_id and b['date'] == date and b['type'] == b_type:
                    user_name = b.get('user_name', 'Unknown')
                    break
            
            save_json(BIRTHDAYS_JSON, new_birthdays)
            await interaction.response.send_message(
                f"✅ Đã xóa sinh nhật của **{user_name}** ({date} - {b_type})",
                ephemeral=True
            )


class BirthdayRemoveView(discord.ui.View):
    """View với select menu để xóa birthday."""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(BirthdayRemoveSelect())
    
    async def on_timeout(self):
        """Xử lý khi timeout."""
        pass


class BirthdayUpdateSelect(discord.ui.Select):
    """Select menu để chọn birthday cần cập nhật theo tên người."""
    
    def __init__(self):
        birthdays = load_json(BIRTHDAYS_JSON)
        
        options = []
        for b in birthdays:
            user_name = b.get('user_name', 'Unknown')
            user_id = b.get('user_id', '')
            date = b.get('date', 'N/A')
            b_type = b.get('type', 'Solar')
            # Tạo unique identifier: user_id|date|type
            value = f"{user_id}|{date}|{b_type}"
            label = f"{user_name} ({date} - {b_type})"
            # Giới hạn label length
            if len(label) > 100:
                label = label[:97] + "..."
            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    description=f"Cập nhật sinh nhật của {user_name}"
                )
            )
        
        if not options:
            options.append(
                discord.SelectOption(
                    label="Không có sinh nhật nào",
                    value="none",
                    description="Danh sách trống"
                )
            )
        
        super().__init__(
            placeholder="Chọn sinh nhật cần cập nhật...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message(
                "Không có sinh nhật nào để cập nhật.",
                ephemeral=True
            )
            return
        
        # Parse value: user_id|date|type
        parts = self.values[0].split("|")
        if len(parts) != 3:
            await interaction.response.send_message(
                "Lỗi: Không thể xác định sinh nhật.",
                ephemeral=True
            )
            return
        
        user_id, date, b_type = parts
        
        # Tìm user_name để truyền vào modal
        birthdays = load_json(BIRTHDAYS_JSON)
        user_name = "Unknown"
        for b in birthdays:
            if str(b.get('user_id', '')) == user_id and b['date'] == date and b['type'] == b_type:
                user_name = b.get('user_name', 'Unknown')
                break
        
        # Import modal here to avoid circular import
        from modals.birthday_update_modal import BirthdayUpdateModal
        
        modal = BirthdayUpdateModal(user_id, user_name, date, b_type)
        await interaction.response.send_modal(modal)


class BirthdayUpdateView(discord.ui.View):
    """View với select menu để cập nhật birthday."""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(BirthdayUpdateSelect())
    
    async def on_timeout(self):
        """Xử lý khi timeout."""
        pass


