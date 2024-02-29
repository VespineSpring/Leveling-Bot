from nextcord.ext import commands
import nextcord
import os
import dotenv

dotenv.load_dotenv()
token = os.getenv("TOKEN")

class Bot(commands.Bot):
    def __init__(self, intents: nextcord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("$"), intents=intents, **kwargs)

    async def setup_hook(self):
        for file in os.listdir("cogs"):
            try:
                if not file.endswith(".py"):
                    return
                if file == "__init__.py":
                    return
                cog = file[:-3]
                await self.load_extension(f"cogs.{cog}")
            except Exception as e:
                print(f"Could not load extension {cog} due to {e.__class__.__name__}: {e}")

    async def on_ready(self):
        await self.change_presence(status=nextcord.Status.idle, activity=nextcord.Game("made by Skele"))
        print(f"Logged on as {self.user}.")

intents = nextcord.Intents.all()
bot = Bot(intents=intents)

bot.run(token)
