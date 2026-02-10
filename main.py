import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
 
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
    if "battle cats" in message.content.lower():
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

async def color(ctx, member: discord.Member, hexcode: str):
    COLOR_MAP = {
        "red": "#ff0000",
        "darkred": "#8b0000",
        "orange": "#ffa500",
        "gold": "#ffd700",
        "yellow": "#ffff00",
        "green": "#00ff00",
        "darkgreen": "#006400",
        "lime": "#32cd32",
        "cyan": "#00ffff",
        "teal": "#008080",
        "blue": "#0000ff",
        "navy": "#000080",
        "skyblue": "#87ceeb",
        "purple": "#800080",
        "violet": "#ee82ee",
        "magenta": "#ff00ff",
        "pink": "#ffc0cb",
        "hotpink": "#ff69b4",
        "brown": "#8b4513",
        "chocolate": "#d2691e",
        "white": "#ffffff",
        "lightgray": "#d3d3d3",
        "gray": "#808080",
        "darkgray": "#404040",
        "black": "#000000",
        "benja":  "#cb21b2"
    }
    if hexcode.lower() in COLOR_MAP:
        hexcode = COLOR_MAP[hexcode.lower()]
    hexcode = hexcode.lstrip("#")
    guild = ctx.guild
    try:
        color_value = int(hexcode, 16)
    except:
        await ctx.send("Ovo nije boja u koju te mogu obojati")
        return
    color = discord.Color(color_value)
    role_name = f"Goriot-blagoslov-{member.id}"
    role = discord.utils.get(guild.roles, name=role_name)
    target_position = guild.me.top_role.position - 1
    if role is None:
        role = await guild.create_role(
            name=role_name,
            color=color
        )
        await asyncio.sleep(5)
    await role.edit(color=color, position=target_position)
    await member.add_roles(role)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)