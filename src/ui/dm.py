import discord

from src.instance import bot


class DMView(discord.ui.View):

    def __init__(self, dm_channel: discord.DMChannel) -> None:
        super().__init__()
        
        button = discord.ui.Button(
            label="Перейти в лс бота",
            style=discord.ButtonStyle.url,
            url=dm_channel.jump_url
        )

        self.add_item(button)

