from discord.ext import commands
from StatsManager import StatsManager
from ConfigManager import ConfigManager
import discord
from discord.ext import commands
from utils import *


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_manager: StatsManager = bot.stats_manager
        self.config_manager: ConfigManager = bot.config_manager
    @commands.command()
    async def zeliseigrati(self, ctx, member: discord.Member = None):
        """Pridruži nekoga igri."""
        if member == None:
            await ctx.send(f"Tko?")
            return
        if member.mention == self.config_manager.get_config("velikivoda"):
            await ctx.send("Veliki voda se ne tretira na ovaj nacin!")
            return
        await self.zelimseigrati(ctx, member, True)


    #TODO: napraviti da samo bot moze postaviti bot_called na true
    @commands.command() 
    async def zelimseigrati(self, ctx, member: discord.Member = None, bot_called: bool = False):
        """Pridruži se igri."""
        if member == None:
            member = ctx.author
        if await self.stats_manager.init_person(member.id):
            if not bot_called:
                await ctx.send(f"{member.mention} se pridružio našoj maloj igri...") 
            else:
                await ctx.send(f"{ctx.author.mention} je uvukao {member.mention} u našu malu igru...")
        else:
            await ctx.send(f"Cijenim tvoju veliku želju za igranjem, ali jedna prijava je dovoljna!") 

    @commands.command()
    async def sigurnarijec(self, ctx, member: discord.Member):
        if await self.stats_manager.remove_person(member.id):
            await ctx.send(f"{member.mention} je nažalost odlucila izaci iz igre.")
        else:
            await ctx.send(f"Osoba nije clan igre.")
    @commands.command()
    @player_only
    async def kredit(self, ctx, member: discord.Member = None):
        """Saznaj kredit neke osobe ili sebe."""
        if member == None:
            member = ctx.author 
        await ctx.send(f"{member.mention} ima {self.stats_manager.get_stats()[member.id].get_data().get('goriot_credit', 0)} goriot kredita")

    @commands.command()
    async def ljestvica(self, ctx):
        """Saznaj kredit svih osoba."""
        table = []
        for member_id, stats in self.stats_manager.get_stats().items():
            member = ctx.guild.get_member(member_id)
            if member:
                name = member.display_name
            else:
                continue
            table.append([name, round(stats.get_data().get("goriot_credit", 0), 3)])
        name_width = max(len(str(row[0])) for row in table)
        credit_width = max(len(str(row[1])) for row in table)
        lines = []
        lines.append(f"{'Ime'.ljust(name_width)} | {'Goriot kredit'.rjust(credit_width)}")
        lines.append(f"{'-' * name_width}-+-{'-' * credit_width}")
        table.sort(key=lambda x: -x[1])
        for name, credit in table:
            lines.append(
                f"{str(name).ljust(name_width)} | {str(credit).rjust(credit_width)}"
            )
        
        output_string = "```" + "\n".join(lines) + "```"
        await ctx.send(output_string)

    @commands.command()
    async def config(self, ctx, name, value):
        if name not in self.config_manager.get_all_config().keys():
            await ctx.send(f"{name} nije postavka.")
            return
        await self.config_manager.set_config(name, value)
        await ctx.send(f"Postavka {name} je uspješno promijenjena.")

    @commands.command()
    async def tkoje(self, ctx, name: str):
        if name not in self.config_manager.get_all_config().keys():
            await ctx.send(f"{name} nije postavka.")
            return
        if self.config_manager.get_config(name) == "":
            await ctx.send(f"Nitko nije {name}.")
            return
        await ctx.send(f"{self.config_manager.get_config(name)} je {name}.")

async def setup(bot):
    await bot.add_cog(Meta(bot))