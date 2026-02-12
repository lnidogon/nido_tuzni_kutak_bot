from discord.ext import commands
from StatsManager import StatsManager
from discord.ext import commands
from utils import *
import random
import math
from functools import partial

class Game(commands.Cog):
    def __init__(self, bot, stats_manager: StatsManager):
        self.active_polls = {}
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
            [1, 10, f"DRAGI KAMEN UPOZORENJE - {ctx.author.mention} je osvojio glavnu nagradu i osvojio {10 * amount} goriot kredita!!! (+{10 * amount}gk)"]
        ]
        chosen = random.choices(options, weights=[w[0] for w in options], k=1)[0]
        self.stats_manager.give_credit(ctx.author.id, amount * chosen[1])
        await ctx.send(chosen[2])
        

    @commands.command()
    @player_only
    async def kradi(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Koga?")
            return
        if self.stats_manager.get_credit(ctx.author.id) > self.stats_manager.get_credit(member.id):
            await ctx.send("Nije moguća krađa siromašnijih.")
            return
        if self.stats_manager.get_credit(member.id) < 25:
            await ctx.send("Osoba ima premalo goriot kredita za krađu.")
            return
        
        amount = round(random.uniform(10, 25), 2)
        amount_back = round(random.uniform(amount/2, amount), 2)
        self.stats_manager.update_stat(ctx.author.id, "steals", 1)
        self.stats_manager.give_credit(ctx.author.id, amount_back)
        self.stats_manager.give_credit(member.id, -amount)
        await ctx.send(f"Muahaha, {ctx.author.mention} je pokrao {amount} goriot kredita od {member.mention} i time se obogatio za {amount_back} goriot kredita.")


    @commands.command()
    @player_only
    async def hvala(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Kome?")
            return
        if ctx.author.id == member.id:
            await ctx.send("Nije moguća zahvala samome sebi.")
        if self.stats_manager.get_credit(ctx.author.id) < 2:
            await ctx.send("Nedovoljno goriot kredita za zahvalu.")
            return
        self.stats_manager.give_credit(ctx.author.id, -2)
        self.stats_manager.give_credit(member.id, 5)
        await ctx.send(f"Holsom, {ctx.author.mention} je donirao 5 goriot kredita  {member.mention} iz zahvale.")


    @commands.command()
    @player_only
    async def glasovaj(self, ctx, amount: float = 40,member: discord.Member = None):
        if member == None:
            member = ctx.author
        min_votes  = math.floor(amount / 20)
        if amount < 40:
            await ctx.send(f"Iznos mora biti veći ili jednak 40.")
            return
        message = await ctx.send(f"Zahtjev da {member.mention} dobije {amount} goriot kredita, potrebno je {min_votes} glasova. (👍)")
        await message.add_reaction("👍")

        async def on_vote(author_id: int, amount: float, min_votes: int, reaction: discord.Reaction):
            if str(reaction.emoji) != "👍":
                return
            users = set()
            async for u in reaction.users():
                if not u.bot:
                    users.add(u.id)
            users.discard(author_id)
            if len(users) >= min_votes:
                self.stats_manager.give_credit(author_id, amount)
                await message.channel.send(f"<@{author_id}> je zaradio {amount} goriot kredita!")
                await message.delete()
                del self.active_polls[message.id]

        self.active_polls[message.id] = partial(on_vote, member.id, amount, min_votes)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        message = reaction.message
        if message.id not in self.active_polls:
            return
        await self.active_polls[message.id](reaction)

    @commands.command()
    @player_only
    async def ruznopogledaj(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Koga?")
            return
        if self.stats_manager.get_stats()[ctx.author.id].get_data()['steals'] >= self.stats_manager.get_stats()[member.id].get_data()['steals']:
            await ctx.send(f"Nije moguće osuditi osobu koja manje krade.")
            return
        unjudged_steals = self.stats_manager.get_stat(member.id, 'steals') - self.stats_manager.get_stat(member.id, 'judged_steals')
        if unjudged_steals == 0:
            await ctx.send(f"Osoba nema krađa koje nisu bile ružno pogledane.")
            return
        self.stats_manager.give_credit(ctx.author.id, 10 * unjudged_steals)
        self.stats_manager.update_stat(member.id, 'judged_steals', unjudged_steals)
        await ctx.send(f"{ctx.author.mention} je ružno pogledao {unjudged_steals} krađa koje je počinio {member.mention}, i time zaradio {10 * unjudged_steals} goriot kredita.")

async def setup(bot):
    from main import stats_manager
    await bot.add_cog(Game(bot, stats_manager))