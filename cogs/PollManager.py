from discord.ext import commands

class PollManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}  

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message = reaction.message

        if message.id not in self.active_polls:
            return

        await self.active_polls[message.id](reaction)

async def setup(bot):
    await bot.add_cog(PollManager(bot))