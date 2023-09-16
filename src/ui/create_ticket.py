import os

import discord

from src.instance import bot, cache
from src.ui.confirm_ticket import ConfirmTicketView
from src.ui.decline_modal import Decline
from src.database.models import TicketStatus

class CreateTicketView(discord.ui.View):

    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green)
    async def accept_ticket(self, interaction: discord.Interaction, _: discord.ui.Button) -> None: 
        if interaction.message is None:
            return None

        embed = interaction.message.embeds[0]

        embed.title = "Заказ принят!"
        embed.set_footer(
            text=f"{embed.footer.text}. Исполнитель: {interaction.user.name}#{interaction.user.discriminator}"
        )
        embed.colour = discord.Colour.blue()

        view = ConfirmTicketView()

        await interaction.message.edit(embed=embed, view=view)

        customer = await self.__get_customer(embed.author.name)               
        
        if customer is None:
            return await interaction.response.send_message(
                content="К сожалению, заказчика больше нет на сервере. Вы можете попробовать связаться с ним через личные сообщения.",
                ephemeral=True
            )

        await customer.send(content="Поздравляем! За ваш заказ принялся художник. В скором времени он напишет вам в личные сообщения.")
        await cache.write_info_about_user(customer, TicketStatus.ACCEPTED)

        await interaction.response.send_message(
            content=f"Вы успешно взялись за заказ! Свяжитесь с {customer.mention} для его дальнейшего обсуждения.",
            ephemeral=True
        )

    @discord.ui.button(label="Отколнить", style=discord.ButtonStyle.red)
    async def decline_ticket(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(Decline())

    async def __get_customer(self, nickname: str) -> discord.Member | None:
        guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))

        async for user in guild.fetch_members():
            if f"{user.name}#{user.discriminator}" == nickname:
                return user

