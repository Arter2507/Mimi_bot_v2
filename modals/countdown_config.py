import discord
from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG

class CountdownConfigModal(discord.ui.Modal, title="Cấu hình Countdown"):
    frequency = discord.ui.TextInput(
        label="Tần suất (Weekly / Monthly)",
        default="Monthly",
        required=True
    )
    template_bd = discord.ui.TextInput(
        label="Template Birthday Countdown",
        style=discord.TextStyle.paragraph,
        default="{everyone} {role_mention} Còn {days} ngày nữa tới sinh nhật {user}, tròn {age} tuổi!",
        required=True
    )
    template_tet = discord.ui.TextInput(
        label="Template Tết Countdown",
        style=discord.TextStyle.paragraph,
        default="{everyone} {role_mention} Còn {days} ngày nữa là đến {date_name}!",
        required=True
    )

    days_before = discord.ui.TextInput(
        label="Số ngày báo trước (VD: 5, 7, 10)",
        default="5",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Validate days
        days_str = self.days_before.value
        try:
            # Chấp nhận format "5, 7, 10"
            days = [int(d.strip()) for d in days_str.split(",") if d.strip()]
            if not days:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                "❌ Số ngày không hợp lệ. Vui lòng nhập số nguyên (VD: 5) hoặc danh sách (VD: 5, 7)",
                ephemeral=True
            )
            return

        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)

        if gid not in data:
            data[gid] = {}

        data[gid]["countdown"] = {
            "frequency": self.frequency.value,
            "template_birthday": self.template_bd.value,
            "template_tet": self.template_tet.value,
            "days_before": days
        }

        save_json(JSON_CONFIG, data)
        await interaction.response.send_message(
            f"✅ Đã lưu cấu hình countdown (Báo trước: {', '.join(map(str, days))} ngày).", ephemeral=True
        )
