import os

import discord

from src.instance import bot, logger


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

