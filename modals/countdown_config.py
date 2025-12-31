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

    async def on_submit(self, interaction: discord.Interaction):
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)

        if gid not in data:
            data[gid] = {}

        data[gid]["countdown"] = {
            "frequency": self.frequency.value,
            "template_birthday": self.template_bd.value,
            "template_tet": self.template_tet.value
        }

        save_json(JSON_CONFIG, data)
        await interaction.response.send_message(
            "Đã lưu cấu hình countdown.", ephemeral=True
        )
