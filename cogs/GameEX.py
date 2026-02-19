from discord.ext import commands
from StatsManager import StatsManager
from ConfigManager import ConfigManager
from discord.ext import commands
from utils import *
from random import randint, gauss, uniform

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
            await self.stats_manager.update_stat(ctx.author.id, "gambling", -amount2)
            await ctx.send(f"U armagedonu {ctx.author.mention} je izgubio {amount2} goriot kredita koji je {member.mention} uspješno oteo.")
        else:
            await self.stats_manager.give_credit(member.id, -amount1)
            await self.stats_manager.give_credit(ctx.author.id, amount1)
            await self.stats_manager.update_stat(ctx.author.id, "gambling", amount1) 
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
            amount = min(15, max(5, amount))
            await self.stats_manager.give_credit(ctx.author.id, amount)
            await ctx.send(f"Pariška mačka pod rednim brojem {idx} je iskopala {amount} goriot kredita u ime {ctx.author.mention}.")
            await asyncio.sleep(randint(1, 2) * 300)
        async with self.cat_lock:
            await ctx.send(f"Pariška mačka pod rednim brojem {idx} se vratila u sobu {ctx.author.mention} nakon svoje borbe.")
            self.upregnuti[ctx.author.id].add(idx)
    @commands.command()
    @player_only
    async def rucnokradi(self, ctx, member: discord.Member = None):
        if member == None or member == ctx.author:
            await ctx.send("Za ručnu krađu je potrebno dvoje.")
            return
        if self.stats_manager.get_stat(ctx.author.id, "zloba") < 100:
            await ctx.send("Ovakvu vrstu krađe mogu raditi samo oni s dovoljno tmine u duši.")
            return 
        choice = randint(0, 2)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -40)
        amount = round(uniform(10, 25), 2)
        amount = min(amount, self.stats_manager.get_credit(member.id))
        amount_back = round(uniform(amount/2, amount), 2)
        await self.stats_manager.update_stat(ctx.author.id, "zloba", amount * 2)
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", -amount)
        await self.stats_manager.update_stat(ctx.author.id, "pravicnost", -2)
        await self.stats_manager.update_stat(ctx.author.id, "steals", 1)
        await self.stats_manager.give_credit(ctx.author.id, amount_back)
        await self.stats_manager.give_credit(member.id, -amount)
        await ctx.send(f"Pod prijetnjom franuckse bajunete, {ctx.author.mention} je ukrao {amount} goriot kredita {member.mention} i time se obogatio za {amount_back} goriot kredita.")
        if choice == 0:
            await asyncio.sleep(5)
            await ctx.send(f"Zapravo nije bila prijetnja - bila je najava, 'đenja")
            await asyncio.sleep(1)
            await onezivi(ctx, member, self.stats_manager, self.config_manager)
    @commands.command()
    @player_only
    async def pomoliseza(self, ctx, member: discord.Member = None):
        if member == None or member == ctx.author:
            await ctx.send("Za koga?")
            return
        if self.stats_manager.get_stat(ctx.author.id, "zahvalnost") < 1000:
            await ctx.send("Moliti se mogu samo oni koji su zahvalni za svoje prijatelje.")
            return 
        if self.stats_manager.get_credit(ctx.author.id) < 100:
            await ctx.send("Nedovoljno kredita za molitvu.")
            return
        choice = randint(0, 2)
        await self.stats_manager.give_credit(ctx.author.id, -100)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 50)
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", 200)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -40)
        await ctx.send(f"{ctx.author.mention} se pomolio za {member.mention}... (također platio 100 goriot kredita instituciji)")
        await asyncio.sleep(5)
        if self.stats_manager.get_stat(member.id, "dead") == 0:
            await ctx.send(f"Osoba {member.mention} nije mrtva, ali molitva se cijeni.")
            return
        if choice == 0:
            await ctx.send(f"Molitva je bila uspješna!!! Poruka sponzora: 没问题")
            await ozivi(ctx, member, self.stats_manager, self.config_manager)
        else:
            await ctx.send(f"Molitva nije postigla ništa, zanmljivo kako to radi.") 
async def setup(bot):
    await bot.add_cog(GameEX(bot))