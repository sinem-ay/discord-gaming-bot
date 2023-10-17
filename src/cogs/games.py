import os
from typing import List, Optional
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context

from util.util import team_generator

GUILD_ID = int(os.environ["GUILD_ID"])


class Games(commands.Cog, name="games"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Check if the bot is active")
    async def hello(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Hello!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="assign_teams", description="Assign online users into n teams up to 4"
    )
    async def assign_teams(self, interaction: discord.Interaction, teams: int):
        online_users = [
            member.name
            for member in interaction.guild.members
            if member.status == discord.Status.online and member != self.bot.user
        ]
        teams_list = team_generator(online_users, teams)
        title_teams = ""
        for teams in teams_list:
            users = ", ".join(teams["users"])
            title_teams += f"{teams['team_number']}: {users}\n"
        embed = discord.Embed(
            title=title_teams,
            description=f"GLHF!",
            color=0x9C84EF,
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot), guild=discord.Object(id=GUILD_ID))
