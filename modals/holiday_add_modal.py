import discord
from core.json_store import load_json, save_json
from core.constants import HOLIDAYS_JSON
from core.date_utils import validate_date, normalize_date


class HolidayAddModal(discord.ui.Modal, title="Thêm ngày lễ"):
    """Modal để thêm một hoặc nhiều ngày lễ."""
    
    holidays_input = discord.ui.TextInput(
        label="Ngày lễ (DD-MM-Tên, cách nhau bởi dấu ,)",
        placeholder="VD: 01-01-Tết Nguyên Đán, 25-12-Giáng Sinh",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=2000
    )
    
    type_input = discord.ui.TextInput(
        label="Loại lịch (Solar/Lunar)",
        placeholder="Solar hoặc Lunar",
        required=True,
        max_length=5,
        default="Solar"
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        holidays_text = self.holidays_input.value.strip()
        h_type = self.type_input.value.strip()
        
        # Validate type
        if h_type not in ["Solar", "Lunar"]:
            await interaction.response.send_message(
                "❌ Loại lịch phải là 'Solar' hoặc 'Lunar'.",
                ephemeral=True
            )
            return
        
        # Parse holidays - split by comma
        entries = [e.strip() for e in holidays_text.split(",") if e.strip()]
        
        if not entries:
            await interaction.response.send_message(
                "❌ Vui lòng nhập ít nhất một ngày lễ.",
                ephemeral=True
            )
            return
        
        existing_holidays = load_json(HOLIDAYS_JSON)
        new_holidays = []
        errors = []
        added_count = 0
        
        for entry in entries:
            # Parse format: date-name hoặc date:name
            # Ưu tiên dấu :, nếu không có thì dùng dấu - (parse từ phải sang trái)
            date_str = ""
            name = ""
            
            if ":" in entry:
                # Format: date:name
                parts = entry.split(":", 1)  # Split only on first colon
                date_str = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else ""
            elif "-" in entry:
                # Format: date-name (parse từ phải sang trái)
                # Lấy 2 phần cuối là date (DD-MM), phần còn lại là name
                parts = entry.split("-")
                if len(parts) >= 3:
                    # Lấy 2 phần cuối làm date (DD-MM)
                    date_str = f"{parts[-2]}-{parts[-1]}"
                    # Phần còn lại là name
                    name = "-".join(parts[:-2]).strip()
                    # Nếu name rỗng sau khi strip, có thể format sai
                    if not name:
                        errors.append(f"❌ '{entry}': Format không hợp lệ. Dùng date-name (VD: 12-12-Tết) hoặc date:name")
                        continue
                else:
                    errors.append(f"❌ '{entry}': Format không hợp lệ. Dùng date-name (VD: 12-12-Tết) hoặc date:name")
                    continue
            else:
                errors.append(f"❌ '{entry}': Thiếu dấu phân cách. Format: date-name (VD: 12-12-Tết) hoặc date:name")
                continue
            
            if not date_str:
                errors.append(f"❌ '{entry}': Thiếu ngày")
                continue
            
            if not name:
                errors.append(f"❌ '{entry}': Thiếu tên ngày lễ")
                continue
            
            # Validate date format
            if not validate_date(date_str, h_type):
                errors.append(f"❌ '{entry}': Định dạng ngày không hợp lệ. Dùng DD-MM (VD: 01-01)")
                continue
            
            date = normalize_date(date_str)
            
            # Check duplicate
            is_duplicate = False
            for h in existing_holidays:
                if h['date'] == date and h['type'] == h_type:
                    errors.append(f"⚠️ '{entry}': Ngày lễ {date} ({h_type}) đã tồn tại với tên '{h['name']}'")
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                new_holidays.append({
                    "date": date,
                    "name": name,
                    "type": h_type
                })
                added_count += 1
        
        # Build response message
        response_parts = []
        
        if added_count > 0:
            # Add new holidays
            existing_holidays.extend(new_holidays)
            save_json(HOLIDAYS_JSON, existing_holidays)
            
            response_parts.append(f"✅ Đã thêm {added_count} ngày lễ:")
            for h in new_holidays:
                response_parts.append(f"  • {h['name']} ({h['date']} - {h['type']})")
        
        if errors:
            response_parts.append("\n⚠️ Các lỗi:")
            response_parts.extend(errors[:10])  # Limit to 10 errors
            if len(errors) > 10:
                response_parts.append(f"... và {len(errors) - 10} lỗi khác")
        
        response_message = "\n".join(response_parts)
        
        # Discord message limit is 2000 characters
        if len(response_message) > 2000:
            response_message = response_message[:1900] + "\n...(tin nhắn quá dài)"
        
        await interaction.response.send_message(
            response_message,
            ephemeral=True
        )

