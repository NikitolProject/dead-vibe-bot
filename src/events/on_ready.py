import os

import discord

from src.instance import bot, logger
from src.ui import CreateTaskView


@bot.event
async def on_ready():
    guild = await bot.fetch_guild(int(os.environ["GUILD_ID"]))
    channel = await guild.fetch_channel(int(os.environ["START_CHANNEL"]))
    view = CreateTaskView()
    
    await channel.send(content="Что бы создать заказ нажмите на кнопку ниже.", view=view)

    logger.info("Bot has been started successfully")

