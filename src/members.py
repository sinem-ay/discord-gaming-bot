import os
import discord


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("members"):
        for guild in client.guilds:
            for member in guild.members:
                await message.channel.send(member)


client.run(DISCORD_TOKEN)
