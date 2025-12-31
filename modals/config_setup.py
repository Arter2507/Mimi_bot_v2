import discord
from core.json_store import load_json, save_json
from core.constants import JSON_CONFIG

class ConfigSetupModal(discord.ui.Modal, title="Cài đặt ban đầu"):
    role_id = discord.ui.TextInput(
        label="Role ID (Optional)",
        placeholder="Nhập Role ID để tag...",
        required=False
    )
    channel_id = discord.ui.TextInput(
        label="Channel ID",
        placeholder="Nhập Channel ID để gửi tin...",
        required=True
    )
    wish_type = discord.ui.TextInput(
        label="Loại lời chúc (Static/AI)",
        default="Static",
        required=True
    )
    template = discord.ui.TextInput(
        label="Template tin nhắn",
        style=discord.TextStyle.paragraph,
        default="Chúc mừng {date_name}! {role_mention}",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        data = load_json(JSON_CONFIG)
        gid = str(interaction.guild_id)

        data[gid] = {
            "role_id": self.role_id.value or None,
            "channel_id": self.channel_id.value,
            "wish_type": self.wish_type.value,
            "content_template": self.template.value
        }

        save_json(JSON_CONFIG, data)
        await interaction.response.send_message(
            "Đã lưu cấu hình server.", ephemeral=True
        )
