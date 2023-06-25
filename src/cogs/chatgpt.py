import os
import openai
import discord
from discord import app_commands
from discord.ext import commands

GUILD_ID = int(os.environ["GUILD_ID"])


class ChatGPT(commands.Cog, name="chatgpt"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="chat", description="Chat GPT extension")
    async def chat(self, interaction: discord.Interaction, *, message: str):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": message}]
        )
        await interaction.response.send_message(
            completion["choices"][0]["message"]["content"]
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ChatGPT(bot), guild=discord.Object(id=GUILD_ID))
