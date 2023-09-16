import os

from dotenv import load_dotenv

from src import bot

load_dotenv(".env")

bot.run(os.environ["BOT_TOKEN"])

