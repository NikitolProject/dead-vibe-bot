import discord

from src.instance import bot, cache
from src.ui.ticket_modal import Ticket
from src.database.models import TicketStatus


class SendTicketView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Оформить заказ", style=discord.ButtonStyle.primary)
    async def create_ticket(self, interaction: discord.Interaction, _: discord.ui.Button) -> None: 
        await interaction.response.send_modal(Ticket())

