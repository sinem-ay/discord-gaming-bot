import os
import discord
from discord.ext import commands

from util.util import team_generator, get_free_games
from dynamodb.manage_table import update_rating_discord


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready() -> None:
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Bot is activate")


@client.event
async def on_message(message):
    if message.content == "Hello":
        await message.channel.send(f"Hello {message.author}")

    if message.content.startswith("/assign_teams"):
        online_users = [
            member.name
            for member in message.guild.members
            if member.status == discord.Status.online and member != client.user
        ]
        team_1, team_2 = team_generator(online_users)
        response = f"Team 1: {team_1} \nTeam 2: {team_2}"
        await message.channel.send(response)

    if message.content.startswith("/arrange_players"):
        await message.channel.send(
            "React with 👍 to the message if you are going to play tonight"
        )

        def check(reaction, user):
            return user != client.user and str(reaction.emoji) == "👍"

        _, user = await client.wait_for("reaction_add", check=check)

        online_users = [
            member.name for member in message.guild.members if str(member) == str(user)
        ]
        team_1, team_2 = team_generator(online_users)
        response = f"Team 1: {team_1} \nTeam 2: {team_2}"
        await message.channel.send(response)

    if message.content.startswith("/free_games"):
        games = get_free_games()
        for game in games:
            embed = discord.Embed(title=game["title"], url=game["url"])
            embed.set_image(url=game["image"])
            await message.channel.send(embed=embed)

    if message.content.startswith("/rate"):
        await message.channel.send(
            "Provide game name and rating from 1 to 5 for record your rating e.g., Destiny 2 - 3"
        )

        def check(m):
            return m.author == message.author

        msg = await client.wait_for("message", timeout=60, check=check)
        game_info = msg.content.split("-")
        game_name, rating = game_info[0].strip(), game_info[1].strip()
        update_rating = update_rating_discord(game_name, rating)

        if update_rating:
            await message.channel.send(
                f"Rating for {game_name} has been updated to {rating}"
            )
        else:
            await message.channel.send(f"Game {game_name} not found in the database.")


client.run(DISCORD_TOKEN)
