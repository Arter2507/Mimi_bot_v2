import discord
from core.json_store import load_json, save_json
from core.constants import HOLIDAYS_JSON
from core.date_utils import validate_date, normalize_date


class HolidayUpdateModal(discord.ui.Modal, title="Cập nhật ngày lễ"):
    """Modal để cập nhật tên và ngày của holiday."""
    
    def __init__(self, old_name: str, old_date: str, old_type: str):
        super().__init__()
        self.old_name = old_name
        self.old_date = old_date
        self.old_type = old_type
        
        # Tạo TextInput với giá trị mặc định
        self.new_name_input = discord.ui.TextInput(
            label="Tên ngày lễ mới",
            placeholder="Nhập tên ngày lễ mới...",
            required=True,
            max_length=100,
            default=old_name
        )
        self.add_item(self.new_name_input)
        
        self.new_date_input = discord.ui.TextInput(
            label="Ngày mới (DD-MM)",
            placeholder="Nhập ngày mới (VD: 01-01)...",
            required=True,
            max_length=5,
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
                "❌ Định dạng ngày không hợp lệ hoặc ngày không tồn tại. Dùng DD-MM (VD: 01-01)",
                ephemeral=True
            )
            return
        
        new_date = normalize_date(new_date)
        
        holidays = load_json(HOLIDAYS_JSON)
        
        # Tìm holiday cần cập nhật
        found = False
        for h in holidays:
            if h['name'] == self.old_name and h['date'] == self.old_date and h['type'] == self.old_type:
                # Kiểm tra xem có trùng với holiday khác không (nếu thay đổi date hoặc type)
                if new_date != self.old_date or new_type != self.old_type:
                    for other in holidays:
                        if other['date'] == new_date and other['type'] == new_type:
                            if not (other['name'] == self.old_name and other['date'] == self.old_date and other['type'] == self.old_type):
                                await interaction.response.send_message(
                                    f"❌ Ngày lễ với ngày {new_date} ({new_type}) đã tồn tại!",
                                    ephemeral=True
                                )
                                return
                
                # Cập nhật
                h['name'] = new_name
                h['date'] = new_date
                h['type'] = new_type
                found = True
                break
        
        if not found:
            await interaction.response.send_message(
                "❌ Không tìm thấy ngày lễ để cập nhật.",
                ephemeral=True
            )
            return
        
        save_json(HOLIDAYS_JSON, holidays)
        await interaction.response.send_message(
            f"✅ Đã cập nhật ngày lễ:\n"
            f"**Tên cũ:** {self.old_name} → **Tên mới:** {new_name}\n"
            f"**Ngày cũ:** {self.old_date} ({self.old_type}) → **Ngày mới:** {new_date} ({new_type})",
            ephemeral=True
        )


