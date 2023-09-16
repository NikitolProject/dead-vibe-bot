import os

import discord

from src.instance import (
    bot, logger, cache
)
from src.database import TicketStatus


async def create_feedback(sender: discord.User | discord.Member, text: str) -> None:
    guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))
    channel = await guild.fetch_channel(int(os.environ["FEEDBACK_CHANNEL"]))

    logger.info(f"New feedback by {sender.name}#{sender.discriminator}")

    message = discord.Embed(
        title="Новый отзыв!",
        description=text,
        colour=discord.Colour.gold()
    )

    if sender.avatar:
        message.set_author(
            name=f"{sender.name}#{sender.discriminator}",
            icon_url=sender.avatar.url
        )

    message.set_footer(text=f"Заказчик: {sender.name}#{sender.discriminator}")
    
    await channel.send(embed=message)


class Decline(discord.ui.Modal, title='Форма для отклонения заказа'):
    reason = discord.ui.TextInput(
        label='Причина отклонения заказа',
        placeholder='Почему вы решили отклонить заказ',
        max_length=300
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.message is None:
            return None

        embed = interaction.message.embeds[0]

        embed.title = "Заказ отклонён!"
        embed.description += f"\nПричина отказа от заказа: {self.reason.value}"
        embed.set_footer(
            text=f"{embed.footer.text}. Отклонитель: {interaction.user.name}#{interaction.user.discriminator}"
        )
        embed.colour = discord.Colour.dark_red()

        await interaction.message.edit(embed=embed, view=None)

        customer = await self.__get_customer(embed.author.name)
        
        if customer is not None:
            await customer.send(content=f"Ваш заказ был отклонён {interaction.user.mention}\nПричина отказа: {self.reason.value}")
            await cache.write_info_about_user(customer, TicketStatus.NOT_CREATED)

        await interaction.response.send_message(
            content=f"Заказ был отклонён.",
            ephemeral=True
        )

    async def on_error(self, interaction: discord.Interaction, _: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

    async def __get_customer(self, nickname: str) -> discord.Member | None:
        guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))

        async for user in guild.fetch_members():
            if f"{user.name}#{user.discriminator}" == nickname:
                return user


