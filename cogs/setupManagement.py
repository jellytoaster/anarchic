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
        setupData = game.setupData
        if (setupData.type == enums.SetupDataType.Custom):
            title = "**Setup - Custom Setup**"
        if (setupData.type == enums.SetupDataType.Preset):
            title = "**Setup - Preset Setup**"
        if (setupData.type == enums.SetupDataType.AllAny):
            title = "**Setup - All Any**"
        embed = disnake.Embed(title=title, colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=setupData.generateSetupName(), value=setupData.generateSetupList(), inline=False)
        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="add", description="Add an role to the setup", options=[disnake.Option("role", "The role to add", disnake.OptionType.string, True), disnake.Option("amount", "How many of that role to add", disnake.OptionType.integer, False)])
    async def setup_addRole(self, inter:disnake.ApplicationCommandInteraction, role:str, amount:int=1):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        role = string.capwords(role)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return
        
        if (role not in [string.capwords(e.value) for e in enums.Role] + [string.capwords(e.value).replace('contraction', '') for e in enums.Contractions]):
            await inter.response.send_message("That isn't a role.", ephemeral=True)
            return
        
        game.setupData.addRole(role.lower(), amount)

        embed = disnake.Embed(title=f"**{string.capwords(role)} {utils.roleEmoji(role.replace(' ', '').replace('Contraction', '').lower())} (x{amount}) has been added to the custom setup!**", colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=game.setupData.generateSetupName(), value=game.setupData.generateSetupList(), inline=False)
        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="remove", description="Remove an role from the setup", options=[disnake.Option("role", "The role to remove", disnake.OptionType.string, True), disnake.Option("amount", "How many of that role to remove", disnake.OptionType.integer, False)])
    async def setup_removeRole(self, inter:disnake.ApplicationCommandInteraction, role:str, amount:int=1):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        role = string.capwords(role)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return
        if (role not in [string.capwords(e.value) for e in enums.Role] + [string.capwords(e.value).replace('contraction', '') for e in enums.Contractions]):
            await inter.response.send_message("That isn't a role.", ephemeral=True)
            return
        code = game.setupData.removeRole(role.lower(), amount)

        if (code == 1):
            await inter.response.send_message("The role you selected wasn't in the setup.", ephemeral=True)
            return
        else:

            embed = disnake.Embed(title=f"**{string.capwords(role)} {utils.roleEmoji(role.replace(' ', '').replace('Contraction', ''))} (x{amount}) has been removed from the custom setup!**", colour=disnake.Colour(0xcd95ff))
            embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
            embed.add_field(name=game.setupData.generateSetupName(), value=game.setupData.generateSetupList(), inline=False)
            
            if (code == 2):
                pass

            await inter.response.send_message(embed=embed)

    @setup.sub_command(name="clear", description="Clear the current setup")
    async def clear(self, inter:disnake.ApplicationCommandInteraction):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        if (game.isHost(inter.author) == False):
            await inter.response.send_message("You aren't the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return

        game.setupData.clear()

        await inter.response.send_message(embed=disnake.Embed(title=f"**The current setup has been cleared**", colour=disnake.Colour(0xcd95ff)))

    @setup.sub_command(name="preset", description="Set the current setup to a recommended preset", options=[disnake.Option("name", description="The name of the setup",type=disnake.OptionType.string, required=True, autocomplete=True)])
    async def preset(self, inter:disnake.ApplicationCommandInteraction, name:str):
        game:Game.Game = Game.Game.checkForGame(inter.guild)
        if (game.isHost(inter.author) == False):
            await inter.response.send_message("You aren't the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return
        if (setupData.SetupData.getPresetSetup(name.lower()) == None):
            await inter.response.send_message("A setup like that doesn't exist. Maybe you spelled it wrong?", ephemeral=True)
            return
        
        game.setupData.clear()

        presetSetup = setupData.SetupData.getPresetSetup(name.lower())
        for i in presetSetup[1][1]:
            game.setupData.addRole(i, 1, False)

        game.setupData.type = enums.SetupDataType.Preset
        game.setupData.presetIndex = presetSetup[0]

        embed = disnake.Embed(title=f"**Applied Preset: {presetSetup[0]}**", colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=game.setupData.generateSetupName(), value=game.setupData.generateSetupList(), inline=False)
        embed.set_footer(text="You can modify the preset setup")
        await inter.response.send_message(embed=embed)

    @preset.autocomplete("name")
    async def presetAutocomplete(inter:disnake.ApplicationCommandInteraction, userInput:str):
        userInput=userInput.lower()
        return [string.capwords(setup) for setup in setupData.presetSetups.keys() if userInput in setup.lower()]
    
    @setup_addRole.autocomplete("role")
    @setup_removeRole.autocomplete("role")
    async def autoCompleteRole(inter, input):
        return [string.capwords(e.value) for e in enums.Role if input.lower() in e.value.lower()] + [string.capwords(e.value).replace('contraction', '') for e in enums.Contractions if input.lower() in e.value.lower()]
