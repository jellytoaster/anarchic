import disnake
import config
import classes.errorhandler
import utils
import disnake.ext.commands.errors
from disnake.ext import commands

class adminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="delcategory", description="delcategory")
    async def delca(inter):
        if (inter.author.id not in config.WHITELIST):
            await inter.response.send_message("no", ephemeral=True)
            return
        for i in inter.channel.category.channels:
            await i.delete()

        await inter.channel.category.delete()