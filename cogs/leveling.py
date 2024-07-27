from nextcord.ext import commands
import nextcord
import random
import pymongo
import os
import dotenv

dotenv.load_dotenv()
uri = os.getenv("MONGO")

client = pymongo.MongoClient(uri)
db = client["Main"]

class Leveling(commands.Cog):
    """This bot is a template for leveling discord bots."""
    """
    The formula which is going to be used for the leveling system is:
    XP = BaseXP + ((Current Level * 2)**2 * 10)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        collection = db["Levels"]

        if message.author.bot:
            return
        
        data = collection.find_one({"_id": message.guild.id})
        if not data:
            collection.insert_one(
                {"_id": message.guild.id, "user": message.author.id, "level": 0, "xp": 0}
            )

        data = collection.find_one({"_id": message.guild.id, "user": message.author.id})

        BASE_EXP = 50
        level = data["level"]
        xp_required = BASE_EXP + ((level * 2) ** 2 * 10)

        random_xp = random.randint(1, 10)

        collection.update_one({"_id": message.guild.id, "user": message.author.id}, {"$inc": {"xp": random_xp}})

        if data["xp"] >= xp_required:
            collection.update_one({"_id": message.guild.id, "user": message.author.id}, {"$inc": {"level": 1, "xp": -xp_required}})
            await message.channel.send(f"Congratulations {message.author.mention}, you leveled up to level {level + 1}!")

    @commands.command(name="rank", description="Shows the level of a user.")
    async def rank(self, ctx, member: nextcord.Member = None):
        if not member:
            member = ctx.author

        collection = db["Levels"]

        data = collection.find_one({"_id": ctx.guild.id, "user": member.id})
        if not data:
            await ctx.send(f"{member.name} hasn't sent any messages yet.")
            return

        BASE_XP = 50
        xp = data["xp"]
        level = data["level"]
        xp_required = BASE_XP + ((level * 2) ** 2 * 10)

        await ctx.send(f"{member.name} is on level {level} with {xp}/{xp_required} xp.")

def setup(bot):
    bot.add_cog(Leveling(bot))
