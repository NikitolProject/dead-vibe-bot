import logging

import discord

from discord.ext import commands

from src.database import CacheControl

bot = commands.Bot(
    command_prefix='!', intents=discord.Intents.all()
)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

cache = CacheControl()

