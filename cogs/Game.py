from discord.ext import commands
from StatsManager import StatsManager
from ConfigManager import ConfigManager
from cogs.PollManager import PollManager
from discord.ext import commands
from utils import *
import random
import math
from functools import partial

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_manager: PollManager = bot.get_cog("PollManager")
        self.stats_manager: StatsManager = bot.stats_manager
        self.config_manager: ConfigManager = bot.config_manager

    @commands.command()
    @player_only
    async def kopaj(self, ctx):
        """
        Iskopaj 1 - 5 goriot kredita.
        """
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", 5)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 1)
        await self.stats_manager.update_stat(ctx.author.id, 'closetness', 1)
        amount = random.gauss(1, 1.5)
        amount = round(amount)
        amount = max(1, min(amount, 5))
        await self.stats_manager.give_credit(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention} je kopao kopao i iskopao {amount} goriot kredita!")


    @commands.command()
    @player_only
    async def kockaj(self, ctx, amount: float = 10.0):
        """Uloži 10 - 1000 goriot kredita, i osvoji nagrade do čak 10 puta iznosa!!!"""
        if amount < 10 or amount > 1000:
            await ctx.send(f"Kuća neće prihvatiti tako smiješan ulog...")
            return
        if self.stats_manager.get_stats()[ctx.author.id].get_data()["goriot_credit"] < amount:
            await ctx.send(f"Nedovoljan iznos na računu...")
            return
        
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 10)
        await self.stats_manager.give_credit(ctx.author.id, -amount)
        options = [
            [22, 0, f"Podsjetnik zašto je klađenje loše, {ctx.author.mention} je izgubio sve uloženo. (-{amount}gk)"],
            [11, 0.2, f"Aj bar neš, {ctx.author.mention} je izgubio {0.8 * amount} goriot kredita. (-{0.8 * amount}gk)"],
            [12, 0.5, f"Pola kredita ošlo ća - sad ti je ža, sad ti je ža, {ctx.author.mention} je izgubio {0.5 * amount} goriot kredita. (-{0.5 * amount}gk)"],
            [20, 1, f"Ni da ni ne -  {ctx.author.mention} nije niti dobio, niti izgubio goriot kredit."],
            [14,  1.5, f"Idemooo - {ctx.author.mention} je osvojio {0.5 * amount} goriot kredita. (+{0.5 * amount}gk)"],
            [20, 2, f"Mi smo toliko nazad - {ctx.author.mention} je osvojio {amount} goriot kredita. (+{amount}gk)"],
            [1, 10, f"DRAGI KAMEN UPOZORENJE - {ctx.author.mention} je osvojio glavnu nagradu i osvojio {10 * amount} goriot kredita!!! (+{10 * amount}gk)"]
        ]
        chosen = random.choices(options, weights=[w[0] for w in options], k=1)[0]
        diff = amount * chosen[1] - amount
        await self.stats_manager.update_stat(ctx.author.id, 'gambling', diff)
        await self.stats_manager.give_credit(ctx.author.id, amount * chosen[1])
        await ctx.send(chosen[2])
        

    @commands.command()
    @player_only
    async def kradi(self, ctx, member: discord.Member = None):
        """Pokradi osobi koja ima više kredita od tebe 25 kredita, ti dobivaš samo udio!"""
        if member == None:
            await ctx.send("Koga?")
            return
        
        if self.stats_manager.get_credit(ctx.author.id) > self.stats_manager.get_credit(member.id):
            await ctx.send("Nije moguća krađa siromašnijih.")
            return
        if self.stats_manager.get_credit(member.id) < 25:
            await ctx.send("Osoba ima premalo goriot kredita za krađu.")
            return
        
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -20)
        amount = round(random.uniform(10, 25), 2)
        amount_back = round(random.uniform(amount/2, amount), 2)
        await self.stats_manager.update_stat(ctx.author.id, "zloba", amount)
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", -amount)
        await self.stats_manager.update_stat(ctx.author.id, "pravicnost", -1)
        await self.stats_manager.update_stat(ctx.author.id, "steals", 1)
        await self.stats_manager.give_credit(ctx.author.id, amount_back)
        await self.stats_manager.give_credit(member.id, -amount)
        await ctx.send(f"Muahaha, {ctx.author.mention} je pokrao {amount} goriot kredita od {member.mention} i time se obogatio za {amount_back} goriot kredita.")


    @commands.command()
    @player_only
    async def hvala(self, ctx, member: discord.Member = None):
        """Potroši 2 kredita kako bi se zahvalio osobi i njoj poklonio 5."""
        if member == None:
            await ctx.send("Kome?")
            return
        if ctx.author.id == member.id:
            await ctx.send("Nije moguća zahvala samome sebi.")
        if self.stats_manager.get_credit(ctx.author.id) < 2:
            await ctx.send("Nedovoljno goriot kredita za zahvalu.")
            return
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 5)
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", 100)
        await self.stats_manager.give_credit(ctx.author.id, -2)
        await self.stats_manager.give_credit(member.id, 5)
        await ctx.send(f"Holsom, {ctx.author.mention} je donirao 5 goriot kredita  {member.mention} iz zahvale.")


    @commands.command()
    @player_only
    async def glasaj(self, ctx, amount: float = 40, member: discord.Member = None):
        """Zatraži glasanje od {količina} goriot kredita, {količina}//20 osoba mora glasovati za."""
        if self.config_manager.get_config("pollkanal") == "":
            await ctx.send(f"Molimo odaberite kanal za pollove.")
            return
        pollchannel_id =int(self.config_manager.get_config("pollkanal").strip("<#!>")) 
        channel = self.bot.get_channel(pollchannel_id)
        if member == None:
            member = ctx.author
        min_votes  = math.floor(amount / 20)
        if amount < 40:
            await ctx.send(f"Iznos mora biti veći ili jednak 40.")
            return
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -5)
        message = await channel.send(f"Zahtjev da {member.mention} dobije {amount} goriot kredita, potrebno je {min_votes} glasova. (👍)")
        await message.add_reaction("👍")

        async def on_vote(ctx, message, author_id: int, amount: float, min_votes: int, reaction: discord.Reaction):
            if str(reaction.emoji) != "👍":
                return
            users = set()
            async for u in reaction.users():
                if not u.bot and u.id in self.stats_manager.get_stats().keys():
                    users.add(u.id)
            users.discard(author_id)
            if len(users) >= min_votes:
                async for u in reaction.users():
                    if not u.bot and u.id in self.stats_manager.get_stats().keys():
                        await self.stats_manager.update_stat(u.id, "zahvalnost", 50)
                        await self.stats_manager.update_stat(u.id, "zloba", -20)
                await self.stats_manager.update_stat(author_id, "pravicnost", min_votes)
                await self.stats_manager.give_credit(author_id, amount)
                await ctx.send(f"<@{author_id}> je zaradio {amount} goriot kredita!")
                await message.delete()
                del self.poll_manager.active_polls[message.id]

        self.poll_manager.active_polls[message.id] = partial(on_vote, ctx, message, member.id, amount, min_votes)

    @commands.command()
    @player_only
    async def ruznopogledaj(self, ctx, member: discord.Member = None):
        """Ružno pogledaj osobu koja krade više od tebe. Osoba gubi 15 kredita, a ti dobivaš 10 puta broj krađa koje nisu ružno pogledane. Ružno gledanje osoba koje kradu manje od tebe se kažnjava gubitkom od 10 goriot kredita."""
        if member == None:
            await ctx.send(f"Koga?")
            return
        
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 10)

        if self.stats_manager.get_stats()[ctx.author.id].get_data()['steals'] >= self.stats_manager.get_stats()[member.id].get_data()['steals']:
            amount_taken = min(self.stats_manager.get_credit(ctx.author.id), 10)
            await self.stats_manager.give_credit(ctx.author.id, -amount_taken)
            await ctx.send(f"Nije moguće osuditi osobu koja manje krade. Oduzeto je {amount_taken} goriot kredita.")
            return
        unjudged_steals = self.stats_manager.get_stat(member.id, 'steals') - self.stats_manager.get_stat(member.id, 'judged_steals')
        if unjudged_steals == 0:
            await ctx.send(f"Osoba nema krađa koje nisu bile ružno pogledane.")
            return
        amount_stolen_back = min(self.stats_manager.get_credit(member.id), 15)

        await self.stats_manager.update_stat(ctx.author.id, "zloba", amount_stolen_back)
        await self.stats_manager.update_stat(ctx.author.id, "zahvalnost", -amount_stolen_back)
        await self.stats_manager.update_stat(ctx.author.id, "pravicnost", 1)
        await self.stats_manager.set_stat(ctx.author.id, 'judge', 1)
        await self.stats_manager.give_credit(ctx.author.id, 10 * unjudged_steals)
        await self.stats_manager.update_stat(member.id, 'judged_steals', unjudged_steals)
        await self.stats_manager.give_credit(member.id, -amount_stolen_back)
        await ctx.send(f"{ctx.author.mention} je ružno pogledao {unjudged_steals} krađa koje je počinio {member.mention}, i time zaradio {10 * unjudged_steals} goriot kredita.\n\
                       {member.mention} je kao kaznu za svoje grijehe izgubio {amount_stolen_back} goriot kredita.")


    @commands.command()
    @player_only
    async def poljubi(self, ctx, member: discord.Member = None):
        """Poljubi osobu koja je nekoga prije ružno pogledala kako bi dobio 30 goriot kredita, a ona izgubila 10. Ljubljenje već poljubljene osobe se kažnjava gubitkom 30 goriot kredita."""
        if member == None:
            await ctx.send(f"Koga?")
            return
        if member == ctx.author:
            await ctx.send(f"Ne možeš poljubiti samoga sebe.")
            return
        await self.stats_manager.update_stat(ctx.author.id, "sus", 5)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", 20)
        if int(self.stats_manager.get_stats()[member.id].get_data()['judge']) == 0:
            if int(member.id) == int(self.stats_manager.get_stat(ctx.author.id, "partner")):
                await ctx.send(f"Iako osoba nije tužibaba, ljubav unutar bračne zajednice je dopuštena, awek.\n{ctx.author.mention} i {member.mention} oboje dobivaju 10 goriot kredita.")
                await self.stats_manager.give_credit(member.id, 10)
                await self.stats_manager.give_credit(ctx.author.id, 10)
                return
            amount_taken = min(self.stats_manager.get_credit(ctx.author.id), 30)
            await self.stats_manager.give_credit(ctx.author.id, -amount_taken)
            await ctx.send(f"Osoba nije tužibaba. Policija je zgroženo oduzela {amount_taken} goriot kredita.")
            return
        amount_returned = min(self.stats_manager.get_credit(member.id), 10)

        await self.stats_manager.update_stat(ctx.author.id, "zloba", -amount_returned)
        await self.stats_manager.update_stat(member.id, "sus", 1)

        await self.stats_manager.set_stat(member.id, 'judge', 0)
        await self.stats_manager.give_credit(ctx.author.id, 30)
        await self.stats_manager.give_credit(member.id, -amount_returned)
        await ctx.send(f"{ctx.author.mention} je nježno poljubio {member.mention} u čelo u nadi da će prestati biti takva tužibaba.\n\
                       Centralna banka je ovakav čin ljubavi nagradila iznosom od 30 goriot kredita.\n\
                       {member.mention} je kao pokoru donirao {amount_returned} goriot kredita u dobrotvorne svrhe.")

    @commands.command()
    @player_only
    async def postujvelikogvodu(self, ctx):
        """Dok je veliki vođa online ova naredba donosi 4-8 goriot kredita poput kopanja."""
        voda_id = int(self.config_manager.get_config("velikivoda").strip("<@!>"))
        voda = ctx.guild.get_member(voda_id)
        await self.stats_manager.update_stat(ctx.author.id, "benjavicnost", -1)
        await self.stats_manager.update_stat(ctx.author.id, "rossini odanost", 1)
        if voda and voda.status == discord.Status.offline:
            amount_taken_back = min(self.stats_manager.get_credit(ctx.author.id), 20)
            await self.stats_manager.give_credit(ctx.author.id, -amount_taken_back)
            await self.stats_manager.update_stat(ctx.author.id, "zloba", amount_taken_back)
            await ctx.send(f"{ctx.author.mention} je pokušao zaraditi velikom vođi {voda.mention} iza leđa, time mu je oduzeto {amount_taken_back} goriot kredita za kaznu.")
            return
        if voda and voda.status != discord.Status.online:
            await ctx.send(f"{ctx.author.mention} poštuje velikog vođu, ali vođa trenutno nešto drugo radi pa ga ne može opiti svojom snagom.")
            return 
        amount = random.gauss(4, 1.5)
        amount = round(amount)
        amount = max(4, min(amount, 9))
        await self.stats_manager.give_credit(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention} je opijen snagom velikog vođe pronašao {amount} goriot kredita u svome srcu!")
async def setup(bot):
    await bot.add_cog(Game(bot))