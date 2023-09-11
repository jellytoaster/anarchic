import disnake
from disnake.ext import commands

class adminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot