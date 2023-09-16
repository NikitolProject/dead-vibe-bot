import json

import discord

import redis.asyncio as redis

from src.database.json_encoder import EnhancedJSONEncoder
from src.database.models import User, TicketStatus


class CacheControl:

    def __init__(self) -> None:
        self.connection = redis.from_url("redis://redis:7777")

    async def get_info_about_user(self, user: discord.User | discord.Member) -> User | None:
        user_data = await self.connection.get(f"discord_user:{user.id}")

        if user_data is None:
            return None

        user_data = json.loads(user_data)
        
        print(user_data)

        return User(**user_data)

    async def write_info_about_user(
        self, user: discord.User | discord.Member, status: TicketStatus
    ) -> None:
        await self.connection.set(
            f"discord_user:{user.id}", 
            json.dumps({"ticket_status": status}, cls=EnhancedJSONEncoder)
        )

