import os

import discord

from src.instance import bot, cache
from src.ui.send_feedback import CreateFeedbackView
from src.database.models import TicketStatus

class ConfirmTicketView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Завершить заказ", style=discord.ButtonStyle.primary)
    async def confirm_ticket(self, interaction: discord.Interaction, _: discord.ui.Button) -> None: 
        if interaction.message is None:
            return None

        embed = interaction.message.embeds[0]

        embed.title = "Заказ завершён!"
        embed.colour = discord.Colour.dark_green()

        await interaction.message.edit(embed=embed, view=None)

        customer = await self.__get_customer(embed.author.name)               
        
        if customer is None:
            return None
        
        embed = discord.Embed(
            title="Поздравляем! Ваш заказ был завершён",
            description="Пожалуйста, заполните форму для оставления отзыва о заказе по кнопке ниже\n",
            colour=discord.Colour.gold()
        )
        view = CreateFeedbackView()

        await customer.send(embed=embed, view=view)
        await cache.write_info_about_user(customer, TicketStatus.SEND_FEEDBACK)

        await interaction.response.send_message(
            content=f"Вы успешно завершили заказ для {customer.mention}! Ожидайте отзыв о вашей проделанной работе от него",
            ephemeral=True
        )

    async def __get_customer(self, nickname: str) -> discord.Member | None:
        guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))

        async for user in guild.fetch_members():
            if f"{user.name}#{user.discriminator}" == nickname:
                return user

