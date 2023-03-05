import os
import discord
from discord.ext import commands


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Bot is activate")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "Hello":
        await message.channel.send(f"Hello {message.author}")


client.run(DISCORD_TOKEN)
