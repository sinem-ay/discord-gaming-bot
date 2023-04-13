import os
import discord
from discord.ext import commands

from util import team_generator


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

    if message.content.startswith("/assign_teams"):
        online_users = [
            member.name
            for member in message.guild.members
            if member.status == discord.Status.online
        ]
        team_1, team_2 = team_generator(online_users)
        response = f"Team 1: {team_1} \nTeam 2: {team_2}"
        await message.channel.send(response)


client.run(DISCORD_TOKEN)
