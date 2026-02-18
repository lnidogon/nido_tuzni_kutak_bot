from functools import wraps
import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import asyncio

from ConfigManager import ConfigManager
from StatsManager import StatsManager

def player_only(func):
    @wraps(func)
    async def wrapper(self, ctx, *args, **kwargs):
        from main import stats_manager
        if not stats_manager.is_playing_the_game(ctx.author.id):
            await ctx.send("Molimo prijavite se kako biste koristili ovu naredbu!")
            return
        for arg in args:
            if isinstance(arg, discord.Member):
                if arg.id not in stats_manager.get_stats():
                    await ctx.send("Spominje se osoba koja nije prijavljena!")
                    return
        return await func(self, ctx, *args, **kwargs)
    return wrapper


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
    target_position = guild.me.top_role.position - 2
    if role is None:
        role = await guild.create_role(
            name=role_name,
            color=color
        )
        await asyncio.sleep(5)
    await role.edit(color=color, position=target_position)
    await member.add_roles(role)

def regify(s: str):
    rets = '.*?'.join(s)
    return rets

async def onezivi(ctx, member: discord.Member, stats_manager: StatsManager, config_manager: ConfigManager):
    if "ulogasmrti" not in config_manager.get_all_config():
        await ctx.send("Uloga smrti nije postavljena")
        return
    if stats_manager.get_stat(member.id, "dead") == 1:
        await ctx.send(f"{ctx.mention} je već mrtav.")
        return
    uloga_id = int(config_manager.get_config("ulogasmrti").strip("<@&>"))
    uloga = ctx.guild.get_role(uloga_id)
    await stats_manager.set_stat(member.id, "dead", 1)
    await member.add_roles(uloga)
    current_nick = member.nick if member.nick else member.name
    new_nick = f"{current_nick[:30]} 🪦"
    await member.edit(nick=new_nick)
    await ctx.send(f"Umro je drug {member.mention}.")