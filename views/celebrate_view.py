import discord

class CelebrateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view, no timeout
        self.celebrated = {}

    @discord.ui.button(label="🎉 Ăn mừng ngay!", style=discord.ButtonStyle.green, custom_id="celebrate_button")
    async def celebrate(self, interaction: discord.Interaction, _):
        mid = interaction.message.id
        uid = interaction.user.id
        self.celebrated.setdefault(mid, set())
        if uid in self.celebrated[mid]:
            await interaction.response.send_message("Bạn đã ăn mừng rồi!", ephemeral=True)
            return
        self.celebrated[mid].add(uid)
        await interaction.response.send_message(
            f"{interaction.user.mention} đã tham gia ăn mừng!", ephemeral=False
        )

    async def on_timeout(self):
        # Cleanup when view times out
        self.celebrated.clear()
