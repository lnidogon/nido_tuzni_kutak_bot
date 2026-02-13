import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import asyncio
from utils import *
import re
from StatsManager import StatsManager
from ConfigManager import ConfigManager
from keywords import keywords

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

stats_manager = StatsManager()
config_manager = ConfigManager()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
intents.reactions = True
intents.presences = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=["?", "jasamotacgoriot ", "`"],
            intents=intents,
            log_handler=handler,
            log_level=logging.DEBUG
        )

    async def setup_hook(self):
        await self.load_extension("cogs.Fun")
        await self.load_extension("cogs.Meta")
        await self.load_extension("cogs.Game")

bot = MyBot()
bot.stats_manager = stats_manager
bot.config_manager = config_manager

@bot.event
async def on_ready():
    print(f"We are ready to go {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Stiti cu {member.name} zauvijek")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if stats_manager.is_playing_the_game(message.author.id):
        for name, value in keywords.items():
            matches = re.findall(regify(name), message.content.lower(), re.DOTALL)
            if len(matches) > 0:
                relevancy_factor = len(name) / len(message.content) * len(matches)
                await stats_manager.update_factor(message.author.id, {k : v * relevancy_factor for k, v in value.items()})
    
    banned_re = [
        r"^.*b.*a.*t.*t.*[l1].*[e3].*c.*a.*t.*$", 
        r"^.*c.*o.*u.*p.*c.*a.*t.*$"
    ]
    if any(re.match(reg, message.content.lower()) for reg in banned_re):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - oprezno s time...")

    # if message.content[0] == '`':
    #     await message.delete()

    await bot.process_commands(message)
    
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply() 

    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token))
    loop.run_forever()