import discord

class AnnouncementConfirmView(discord.ui.View):
    def __init__(self, channel, embed):
        super().__init__(timeout=60)
        self.channel = channel
        self.embed = embed

    @discord.ui.button(label="Gửi ngay", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, _):
        for c in self.children: c.disabled = True
        await self.channel.send(embed=self.embed)
        await interaction.response.edit_message(content="✅ Đã gửi.", view=self)

    @discord.ui.button(label="Hủy", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, _):
        for c in self.children: c.disabled = True
        await interaction.response.edit_message(content="❌ Đã hủy.", view=self)
