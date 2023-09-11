import disnake
import string
import utils
from disnake.ext import commands
from classes import enums, setupData
from classes import game as Game

class setupManagement(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="setup", description="setup")
    async def setup(self, inter):
        pass

    @setup.sub_command(name="view", description="View the setup")
    async def view(self, inter):
        game:Game.Game = Game.Game.checkForGame(inter.guild)
        embed = disnake.Embed(title=f"**Setup**", colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=f"__Custom :triangular_flag_on_post: ({len(game.setupData.roles)}P)__", value=game.setupData.generateSetupList(), inline=False)
        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="add", description="Add an role to the setup", options=[disnake.Option("role", "The role to add", disnake.OptionType.string, True, choices=[string.capwords(e.value) for e in enums.Role]), disnake.Option("amount", "How many of that role to add", disnake.OptionType.integer, False)])
    async def setup_addRole(self, inter:disnake.ApplicationCommandInteraction, role:str, amount:int=1):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        game.setupData.addRole(role, amount)

        embed = disnake.Embed(title=f"**{string.capwords(role)} {utils.roleEmoji(role)} has been added to the custom setup!**", colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=f"__Custom :triangular_flag_on_post: ({len(game.setupData.roles)}P)__", value=game.setupData.generateSetupList(), inline=False)
        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="remove", description="Remove an role from the setup", options=[disnake.Option("role", "The role to remove", disnake.OptionType.string, True, choices=[string.capwords(e.value) for e in enums.Role]), disnake.Option("amount", "How many of that role to remove", disnake.OptionType.integer, False)])
    async def setup_addRole(self, inter:disnake.ApplicationCommandInteraction, role:str, amount:int=1):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        
        code = game.setupData.removeRole(role, amount)

        if (code == 1):
            await inter.response.send_message("The role you selected wasn't in the setup.", ephemeral=True)
            return
        else:

            embed = disnake.Embed(title=f"**{string.capwords(role)} {utils.roleEmoji(role)} has been removed from the custom setup!**", colour=disnake.Colour(0xcd95ff))
            embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
            embed.add_field(name=f"__Custom :triangular_flag_on_post: ({len(game.setupData.roles)}P)__", value=game.setupData.generateSetupList(), inline=False)
            
            if (code == 2):
                pass

            await inter.response.send_message(embed=embed)
