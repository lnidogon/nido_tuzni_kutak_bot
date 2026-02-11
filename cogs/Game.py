from discord.ext import commands
from StatsManager import StatsManager
from discord.ext import commands
from utils import *
import random

class Game(commands.Cog):
    def __init__(self, bot, stats_manager: StatsManager):
        self.bot = bot
        self.stats_manager = stats_manager

    @commands.command()
    @player_only
    async def kopaj(self, ctx):
        amount = random.gauss(1, 1.5)
        amount = round(amount)
        amount = max(1, min(amount, 5))
        self.stats_manager.give_credit(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention} je kopao kopao i iskopao {amount} goriot kredita!")


    @commands.command()
    @player_only
    async def kockaj(self, ctx, amount: float = 10.0):
        if amount < 10 or amount > 100:
            await ctx.send(f"Kuća neće prihvatiti tako smiješan ulog...")
            return
        if self.stats_manager.get_stats()[ctx.author.id].get_data()["goriot_credit"] < amount:
            await ctx.send(f"Nedovoljan iznos na računu...")
            return
        self.stats_manager.give_credit(ctx.author.id, -amount)
        options = [
            [22, 0, f"Podsjetnik zašto je klađenje loše, {ctx.author.mention} je izgubio sve uloženo. (-{amount}gk)"],
            [11, 0.2, f"Aj bar neš, {ctx.author.mention} je izgubio {0.8 * amount} goriot kredita. (-{0.8 * amount}gk)"],
            [12, 0.5, f"Pola kredita ošlo ća - sad ti je ža, sad ti je ža, {ctx.author.mention} je izgubio {0.5 * amount} goriot kredita. (-{0.5 * amount}gk)"],
            [20, 1, f"Ni da ni ne -  {ctx.author.mention} nije niti dobio, niti izgubio goriot kredit."],
            [14,  1.5, f"Idemooo - {ctx.author.mention} je osvojio {0.5} goriot kredita. (+{0.5 * amount}gk)"],
            [20, 2, f"Mi smo toliko nazad - {ctx.author.mention} je osvojio {amount} goriot kredita. (+{amount}gk)"],
            [1, 10, f"DRAGI KAMEN UPOZORENJE - {ctx.author} je osvojio glavnu nagradu i osvojio {10 * amount} goriot kredita!!! (+{10 * amount}gk)"]
        ]
        chosen = random.choices(options, weights=[w[0] for w in options], k=1)[0]
        self.stats_manager.give_credit(ctx.author.id, amount * chosen[1])
        await ctx.send(chosen[2])
        
async def setup(bot):
    from main import stats_manager
    await bot.add_cog(Game(bot, stats_manager))