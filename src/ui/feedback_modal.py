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


class Feedback(discord.ui.Modal, title='Форма для отправки отзыва'):
    name = discord.ui.TextInput(
        label='Никнейм',
        placeholder='Ваш никнейм в СП...',
        max_length=300
    )

    executor = discord.ui.TextInput(
        label='Никнейм художника',
        placeholder='Никнейм художника, нарисовавшего вам скин...',
        max_length=300
    )

    feedback = discord.ui.TextInput(
        label='Ваш отзыв',
        style=discord.TextStyle.long,
        placeholder='Как вам нарисованный скин?',
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await create_feedback(interaction.user, f"1. {self.name.value}\n2. {self.executor.value}\n3. {self.feedback.value}")        
        await cache.write_info_about_user(interaction.user, TicketStatus.NOT_CREATED)
        await interaction.response.send_message(f'Спасибо за оставленный отзыв, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, _: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

