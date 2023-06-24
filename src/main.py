import os
import asyncio
import discord
from discord.ext.commands import Bot, Context

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        activity=discord.Game(name="Type /help for command list"),
        status=discord.Status.do_not_disturb,
    )


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


asyncio.run(load_cogs())
bot.run(DISCORD_TOKEN)
