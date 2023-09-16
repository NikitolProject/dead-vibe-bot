import os

import discord

from src.instance import (
    bot, logger, cache
)
from src.database import TicketStatus
from src.ui.create_ticket import CreateTicketView 


async def create_ticket(sender: discord.User | discord.Member, text: str) -> None:
    guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))
    channel = await guild.fetch_channel(int(os.environ["ADMIN_CHANNEL"]))
    view = CreateTicketView()

    logger.info(f"New ticket by {sender.name}#{sender.discriminator}")

    message = discord.Embed(
        title="Новый заказ!",
        description=text,
        colour=discord.Colour.gold()
    )

    if sender.avatar:
        message.set_author(
            name=f"{sender.name}#{sender.discriminator}",
            icon_url=sender.avatar.url
        )

    message.set_footer(text=f"Заказчик: {sender.name}#{sender.discriminator}")
    
    await channel.send(embed=message, view=view)


class Ticket(discord.ui.Modal, title='Форма для отправки заказа'):
    name = discord.ui.TextInput(
        label='Никнейм',
        placeholder='Ваш никнейм в СП...',
        max_length=300
    )

    task = discord.ui.TextInput(
        label='Подробное ТЗ',
        style=discord.TextStyle.long,
        placeholder='Как вы хотите видеть свой скин?',
    )

    references = discord.ui.TextInput(
        label='Референсы для скина',
        style=discord.TextStyle.long,
        placeholder='Если у вас есть референсы к скину, напишите сюда URL-ы...',
        required=False
    )

    deadline = discord.ui.TextInput(
        label='Дедлайн',
        placeholder='Какие дедлайны по скину? (обязательно адекватные, за минуту/час не сделаем)',
        max_length=300
    )

    executor = discord.ui.TextInput(
        label='Предпочтительный художник',
        placeholder='Есть ли у вас предпочтительный художник для скина?',
        max_length=300,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await create_ticket(interaction.user, f"1. {self.name.value}\n2. {self.task.value}\n3. {self.references.value}\n4. {self.deadline.value}\n5. {self.executor.value}")        
        await cache.write_info_about_user(interaction.user, TicketStatus.WRITTEN)
        await interaction.response.send_message(f'{self.name.value}, ваше ТЗ переданно к художникам, ожидайте ответа.', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, _: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

