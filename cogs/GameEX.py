from discord.ext import commands
from StatsManager import StatsManager
from ConfigManager import ConfigManager
from discord.ext import commands
from utils import *
from random import randint, gauss

class GameEX(commands.Cog):
    def __init__(self, bot):
        self.upregnuti: dict[int, set[int]] = {}
        self.bot = bot
        self.stats_manager: StatsManager = bot.stats_manager
        self.config_manager: ConfigManager = bot.config_manager
        self.cat_lock = asyncio.Lock()

    @commands.command()
    @player_only
    async def armagedon(self, ctx, member: discord.Member = None):
        if member == None or member == ctx.author:
            await ctx.send("Za armagedon je potrebno dvoje.")
            return
        if self.stats_manager.get_stat(ctx.author.id, "gambling") > -1000:
            await ctx.send("Ovakav pothvat mogu raditi samo pravi kockari.")
            return
        if self.stats_manager.get_credit(member.id) > self.stats_manager.get_credit(ctx.author.id):
            await ctx.send("Armagedon ne radi ako osoba ima više kredita.")
            return
        choice = randint(0, 1)
        amount1 = self.stats_manager.get_credit(member.id)
        amount2 = self.stats_manager.get_credit(ctx.author.id)
        await self.stats_manager.update_stat(ctx.author.id, "zloba", amount2)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -5)
        if choice == 0:
            await self.stats_manager.give_credit(member.id, amount2)
            await self.stats_manager.give_credit(ctx.author.id, -amount2)
            await self.stats_manager.update_stat(ctx.author.id, "gambling", amount2)
            await ctx.send(f"U armagedonu {ctx.author.mention} je izgubio {amount2} goriot kredita koji je {member.mention} uspješno oteo.")
        else:
            await self.stats_manager.give_credit(member.id, -amount1)
            await self.stats_manager.give_credit(ctx.author.id, amount1)
            await self.stats_manager.update_stat(ctx.author.id, "gambling", -amount1) 
            await ctx.send(f"U armagedonu {member.mention} je izgubio {amount1} goriot kredita koji je {ctx.author.mention} uspješno oteo.")
            

    @commands.command()
    @player_only
    async def upregni(self, ctx):
        if ctx.author.id not in self.upregnuti:
            self.upregnuti[ctx.author.id] = set(range(1, 11))
        if len(self.upregnuti[ctx.author.id]) == 0 or min(self.upregnuti[ctx.author.id]) > 10:
            await ctx.send(f"Sve pariške mačke koje te slušaju {ctx.author.mention} su već upregnute.")
            return
        if self.stats_manager.get_stat(ctx.author.id, "closetness") < 100:
            await ctx.send("Za upregavanje je potrebno više grindati (wink).")
            return
        async with self.cat_lock:
            await self.stats_manager.update_stat(ctx.author.id, "closetness", 1)
            idx = min(self.upregnuti[ctx.author.id])
            await ctx.send(f"Pariška mačka pod rednim brojem {idx} je upregnuta u ime {ctx.author.mention}.")
            self.upregnuti[ctx.author.id].remove(idx)
        await asyncio.sleep(5)
        for _ in range(randint(4, 6)):
            amount = round(gauss(5, 5))
            amount = min(3, max(1, amount))
            await self.stats_manager.give_credit(ctx.author.id, amount)
            await ctx.send(f"Pariška mačka pod rednim brojem {idx} je iskopala {amount} goriot kredita u ime {ctx.author.mention}.")
            await asyncio.sleep(randint(1, 2) * 300)
        async with self.cat_lock:
            await ctx.send(f"Pariška mačka pod rednim brojem {idx} se vratila u sobu {ctx.author.mention} nakon svoje borbe.")
            self.upregnuti[ctx.author.id].add(idx)
    @commands.command()
    @player_only
    async def djecjisan(self, ctx, member: discord.Member = None):
        pass
        
async def setup(bot):
    await bot.add_cog(GameEX(bot))