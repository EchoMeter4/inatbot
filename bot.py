import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp


class iNatBot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents(
            guilds=True,
            members=True,
            emojis=True,
            messages=True,
            reactions=True,
        )
        super().__init__(command_prefix="|", allowed_mentions=allowed_mentions, intents=intents)

        self.endpoint = "https://api.inaturalist.org/v1"

        self.embed_color = 7646208

    async def on_ready(self):
        print(f"Successfully logged in as {self.user.display_name}.")
