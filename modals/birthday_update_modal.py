import discord
from core.json_store import load_json, save_json
from core.constants import BIRTHDAYS_JSON
from core.date_utils import validate_date, normalize_date


class BirthdayUpdateModal(discord.ui.Modal, title="Cập nhật sinh nhật"):
    """Modal để cập nhật tên người và ngày của birthday."""
    
    def __init__(self, old_user_id: str, old_user_name: str, old_date: str, old_type: str):
        super().__init__()
        self.old_user_id = old_user_id
        self.old_user_name = old_user_name
        self.old_date = old_date
        self.old_type = old_type
        
        # Tạo TextInput với giá trị mặc định
        self.new_name_input = discord.ui.TextInput(
            label="Tên người mới",
            placeholder="Nhập tên người mới...",
            required=True,
            max_length=100,
            default=old_user_name
        )
        self.add_item(self.new_name_input)
        
        self.new_date_input = discord.ui.TextInput(
            label="Ngày sinh mới (DD-MM-YYYY)",
            placeholder="Nhập ngày sinh mới (VD: 01-01-1999)...",
            required=True,
            max_length=10,
            default=old_date
        )
        self.add_item(self.new_date_input)
        
        self.new_type_input = discord.ui.TextInput(
            label="Loại lịch (Solar/Lunar)",
            placeholder="Solar hoặc Lunar",
            required=True,
            max_length=5,
            default=old_type
        )
        self.add_item(self.new_type_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        new_name = self.new_name_input.value.strip()
        new_date = self.new_date_input.value.strip()
        new_type = self.new_type_input.value.strip()
        
        # Validate type
        if new_type not in ["Solar", "Lunar"]:
            await interaction.response.send_message(
                "❌ Loại lịch phải là 'Solar' hoặc 'Lunar'.",
                ephemeral=True
            )
            return
        
        # Validate date format
        if not validate_date(new_date, new_type):
            await interaction.response.send_message(
                "❌ Định dạng ngày không hợp lệ hoặc ngày không tồn tại. Dùng DD-MM-YYYY (VD: 01-01-1999)",
                ephemeral=True
            )
            return
        
        new_date = normalize_date(new_date)
        
        birthdays = load_json(BIRTHDAYS_JSON)
        
        # Tìm birthday cần cập nhật
        found = False
        for b in birthdays:
            if str(b.get('user_id', '')) == self.old_user_id and b['date'] == self.old_date and b['type'] == self.old_type:
                # Kiểm tra xem có trùng với birthday khác không (nếu thay đổi date hoặc type)
                if new_date != self.old_date or new_type != self.old_type:
                    for other in birthdays:
                        if other['date'] == new_date and other['type'] == new_type:
                            if not (str(other.get('user_id', '')) == self.old_user_id and other['date'] == self.old_date and other['type'] == self.old_type):
                                await interaction.response.send_message(
                                    f"❌ Sinh nhật với ngày {new_date} ({new_type}) đã tồn tại!",
                                    ephemeral=True
                                )
                                return
                
                # Cập nhật
                b['user_name'] = new_name
                b['date'] = new_date
                b['type'] = new_type
                found = True
                break
        
        if not found:
            await interaction.response.send_message(
                "❌ Không tìm thấy sinh nhật để cập nhật.",
                ephemeral=True
            )
            return
        
        save_json(BIRTHDAYS_JSON, birthdays)
        await interaction.response.send_message(
            f"✅ Đã cập nhật sinh nhật:\n"
            f"**Tên cũ:** {self.old_user_name} → **Tên mới:** {new_name}\n"
            f"**Ngày cũ:** {self.old_date} ({self.old_type}) → **Ngày mới:** {new_date} ({new_type})",
            ephemeral=True
        )


