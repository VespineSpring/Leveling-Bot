from nextcord.ext import commands
import nextcord

class Leveling(commands.Cog):
    """The description for Leveling goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Leveling(bot))
