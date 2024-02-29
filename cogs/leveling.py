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
    This formula is made by me so it is called the "Skele's Leveling Formula."
    If you have made this formula so I am sorry for that. Because I didn't knew that this formula is already made.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        collection = db["Levels"]

        if message.author.bot:
            return
        
        guild_id = message.guild.id
        user_id = message.author.id

        try:
            # Check if the guild entry exists
            if not collection.count_documents({"_id": guild_id}):
                collection.insert_one({"_id": guild_id})

            # Check if the user entry exists
            data = collection.find_one({"_id": guild_id, "user": user_id})
            if not data:
                collection.update_one({"_id": guild_id}, {"$push": {"user": user_id}})
                print(f"Added user {message.author.name} to the collection.")

            data = collection.find_one({"_id": guild_id, "user": user_id})
            BASE_EXP = 50
            level = data["level"]
            xp_required = BASE_EXP + ((level * 2) ** 2 * 10)

            random_xp = random.randint(1, 10)

            collection.update_one({"_id": guild_id, "user": user_id}, {"$inc": {"xp": random_xp}})
            print(f"Gave {message.author.name} {random_xp}xp. Current XP: {data['xp'] + random_xp}")

            if data["xp"] >= xp_required:
                collection.update_one({"_id": guild_id, "user": user_id}, {"$inc": {"level": 1, "xp": -xp_required}})
                print(f"Level up! {message.author.name} leveled up to level {level + 1}. Remaining XP: {data['xp'] - xp_required}")
                await message.channel.send(f"Congratulations {message.author.mention}, you leveled up to level {level + 1}!")

        except Exception as e:
            print(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Leveling(bot))
