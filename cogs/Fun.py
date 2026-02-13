from discord.ext import commands
from StatsManager import StatsManager
from utils import *

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_manager = bot.stats_manager
    @commands.command()
    async def dajmiznanje(self, ctx):
        """Saznaj kod za znanje."""
        await ctx.send("D637C289NNT")

    @commands.command()
    async def obojime(self, ctx, hexcode: str):
        """Promijeni svoju boju."""
        await color(ctx, ctx.author, hexcode)
        await ctx.send(f"Green na midu")

    @commands.command()
    async def lakunoc(self, ctx):
        """Poželi Gori-Botu laku noć."""
        await ctx.send(f"Laku noć i tebi {ctx.author.mention}")

    @commands.command()
    async def obojiga(self, ctx, member: discord.Member, hexcode: str):
        """Promijeni nečiju boju."""
        await color(ctx, member, hexcode)
        await ctx.send(f"Green nam idu")

async def setup(bot):
    await bot.add_cog(Fun(bot))