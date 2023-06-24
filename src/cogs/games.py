import discord
from discord.ext import commands
from discord.ext.commands import Context


class Games(commands.Cog, name="games"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="hello", description="Check if the bot is active")
    async def hello(self, ctx: Context):
        embed = discord.Embed(
            title=f"Hello {ctx.message.author}!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))
