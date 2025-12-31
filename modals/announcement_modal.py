import discord
from views.announcement_view import AnnouncementConfirmView

class AnnouncementModal(discord.ui.Modal, title="Tạo thông báo"):
    title_input = discord.ui.TextInput(
        label="Tiêu đề",
        required=True
    )
    description_input = discord.ui.TextInput(
        label="Nội dung",
        style=discord.TextStyle.paragraph,
        required=True
    )
    icon_url = discord.ui.TextInput(
        label="Icon URL (Optional)",
        required=False
    )
    image_url = discord.ui.TextInput(
        label="Image URL (Optional)",
        required=False
    )
    footer_text = discord.ui.TextInput(
        label="Footer (Optional)",
        required=False
    )

    def __init__(self, channel, mention_default=None):
        super().__init__()
        self.channel = channel
        if mention_default:
            self.description_input.default = f"{mention_default.mention} "

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=discord.Color.blue()
        )

        if self.icon_url.value:
            embed.set_thumbnail(url=self.icon_url.value)
        if self.image_url.value:
            embed.set_image(url=self.image_url.value)
        if self.footer_text.value:
            embed.set_footer(text=self.footer_text.value)

        view = AnnouncementConfirmView(self.channel, embed)

        await interaction.response.send_message(
            f"Xem trước thông báo sẽ gửi vào {self.channel.mention}:",
            embed=embed,
            view=view,
            ephemeral=True
        )
