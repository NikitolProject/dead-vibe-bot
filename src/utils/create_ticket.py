import os

import discord

from src.instance import bot, logger

from src.ui import CreateTicketView 


async def create_ticket(sender: discord.User | discord.Member, text: str) -> None:
    guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))
    channel = await bot.fetch_channel(int(os.environ["ADMIN_CHANNEL"]))
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

