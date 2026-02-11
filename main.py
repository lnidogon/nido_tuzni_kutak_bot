import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import asyncio
from utils import *
import re
from StatsManager import StatsManager
from functools import wraps
from keywords import keywords

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

stats_manager = StatsManager()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def player_only(func):
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        member = args[0]
        if member == None:
            member = ctx.author
        if member.id not in stats_manager.get_stats():
            await ctx.send("Osoba nije prijavljena!")
            return
        return await func(ctx, *args, **kwargs)
    return wrapper
 
bot = commands.Bot(command_prefix=['?', 'jasamotacgoriot ', '`'], intents=intents)

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
                stats_manager.update_factor(message.author.id, {k : v * relevancy_factor for k, v in value.items()})
    
    banned_re = [
        r"^.*b.*a.*t.*t.*[l1].*[e3].*c.*a.*t.*$", 
        r"^.*c.*o.*u.*p.*c.*a.*t.*$"
    ]
    if any(re.match(reg, message.content.lower(), re.DOTALL) for reg in banned_re):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - oprezno s time...")
    if message.content[0] == '`':
        await message.delete()
    await bot.process_commands(message)
    
@bot.command()
async def dajmiznanje(ctx):
    await ctx.send("D637C289NNT")

@bot.command()
async def obojime(ctx, hexcode: str):
    await color(ctx, ctx.author, hexcode)
    await ctx.send(f"Green na midu")

@bot.command()
async def lakunoc(ctx):
    await ctx.send(f"Laku noć i tebi {ctx.author.mention}")

@bot.command()
async def obojiga(ctx, member: discord.Member, hexcode: str):
    await color(ctx, member, hexcode)
    await ctx.send(f"Green nam idu")

@bot.command()
async def zeliseigrati(ctx, member: discord.Member = None):
    if member == None:
        await ctx.send(f"Tko?")
        return
    await zelimseigrati(ctx, member, True)


#TODO: napraviti da samo bot moze postaviti bot_called na true
@bot.command() 
async def zelimseigrati(ctx, member: discord.Member = None, bot_called: bool = False):
    if member == None:
        member = ctx.author
    if stats_manager.init_person(member.id):
        if not bot_called:
            await ctx.send(f"{member.mention} se pridružio našoj maloj igri...") 
        else:
            await ctx.send(f"{ctx.author.mention} je uvukao {member.mention} u našu malu igru...")
    else:
        await ctx.send(f"Cijenim tvoju veliku želju za igranjem, ali jedna prijava je dovoljna!") 

@bot.command()
@player_only
async def kredit(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author 
    await ctx.send(f"{member.mention} ima {stats_manager.get_stats()[member.id].get_data().get('goriot_credit', 0)} goriot kredita")

@bot.command()
async def ljestvica(ctx):
    table = []
    for member_id, stats in stats_manager.get_stats().items():
        member = ctx.guild.get_member(member_id)
        if member:
            name = member.display_name
        else:
            continue
        table.append([name, stats.get_data().get("goriot_credit", 0)])
    name_width = max(len(str(row[0])) for row in table)
    credit_width = max(len(str(row[1])) for row in table)
    lines = []
    lines.append(f"{'Ime'.ljust(name_width)} | {'Goriot kredit'.rjust(credit_width)}")
    lines.append(f"{'-' * name_width}-+-{'-' * credit_width}")
    for name, credit in table:
        lines.append(
            f"{str(name).ljust(name_width)} | {str(credit).rjust(credit_width)}"
        )
        
    output_string = "```" + "\n".join(lines) + "```"
    await ctx.send(output_string)



bot.run(token, log_handler=handler, log_level=logging.DEBUG)