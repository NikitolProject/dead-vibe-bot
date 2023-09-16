import discord

from src.instance import bot, cache
from src.ui.feedback_modal import Feedback
from src.database.models import TicketStatus


class CreateFeedbackView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Оставить отзыв", style=discord.ButtonStyle.primary)
    async def create_feedback(self, interaction: discord.Interaction, _: discord.ui.Button) -> None: 
        await interaction.response.send_modal(Feedback())

