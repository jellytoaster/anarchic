import disnake
import config
from disnake.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Get help about the bot")
    async def help(inter:disnake.ApplicationCommandInteraction):
        inter.response.send_message("help? uh idk wip i guess")