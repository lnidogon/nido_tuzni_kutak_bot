from discord.ext import commands
from StatsManager import StatsManager
from utils import *

class Fun(commands.Cog):
    def __init__(self, bot, stats_manager: StatsManager):
        self.bot = bot
        self.stats_manager =    stats_manager
    @commands.command()
    async def dajmiznanje(self, ctx):
        await ctx.send("D637C289NNT")

    @commands.command()
    async def obojime(self, ctx, hexcode: str):
        await color(ctx, ctx.author, hexcode)
        await ctx.send(f"Green na midu")

    @commands.command()
    async def lakunoc(self, ctx):
        await ctx.send(f"Laku noć i tebi {ctx.author.mention}")

    @commands.command()
    async def obojiga(self, ctx, member: discord.Member, hexcode: str):
        await color(ctx, member, hexcode)
        await ctx.send(f"Green nam idu")

async def setup(bot):
    from main import stats_manager 
    await bot.add_cog(Fun(bot, stats_manager))