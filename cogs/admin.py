import disnake
from disnake.ext import commands

class adminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="delcategory", description="delcategory")
    async def delca(inter):
        for i in inter.channel.category.channels:
            await i.delete()

        await inter.channel.category.delete()