import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot, Context

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
GUILD_ID = int(os.environ["GUILD_ID"])


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="/", intents=intents)

    # Syncing slash commands with Setup Hook
    async def setup_hook(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(name="Type /help for command list"),
            status=discord.Status.do_not_disturb,
        )


bot = Bot()
bot.run(DISCORD_TOKEN)
