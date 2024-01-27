from typing import Optional
import classes.contraction
import disnake
import string
import utils
import base64
from disnake.ext import commands
import classes.role
from classes import enums, setupData
from classes import game as Game

# Setup import/export helpers
def encode(data:setupData.SetupData, name:str):
    return  "ANARCHIC||" + name + "||" + "||".join(data.roles)

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

        embed = disnake.Embed(title=setupData.type.value + setupData.generateSetupNameWithoutNumbers(), colour=disnake.Colour(0xcd95ff))
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
        
        if (role not in [string.capwords(e.name) for e in classes.role.Role.allRoles] + [string.capwords(e.display_name) for e in classes.contraction.Contraction.allContractions]):
            await inter.response.send_message("That isn't a role.", ephemeral=True)
            return
        
        if (amount > 10):
            await inter.response.send_message("Don't you think that's too much?", ephemeral=True)
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
        if (role not in [string.capwords(e.name) for e in classes.role.Role.allRoles] + [string.capwords(e.display_name) for e in classes.contraction.Contraction.allContractions]):
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
        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
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

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
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

        embed = disnake.Embed(title=f"**Applied Preset: {game.setupData.generateSetupNameWithoutNumbers()}**", colour=disnake.Colour(0xcd95ff))
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/O3tABe1id1w0dcI-B8MMo-DgXI9Co9xNaS6QSbjKU2o/%3Fsize%3D1024/https/cdn.discordapp.com/icons/753967387149074543/c908a07ef8d6165ab31770e4b47f38ca.webp")
        embed.add_field(name=game.setupData.generateSetupName(), value=game.setupData.generateSetupList(), inline=False)
        embed.set_footer(text="You can modify the preset setup.", icon_url=inter.author.display_avatar.url)
        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="export", description="Export a setup as text that can be re-imported", options=[disnake.Option("name", "Name your setup!", disnake.OptionType.string)])
    async def export(inter:disnake.ApplicationCommandInteraction, name="Custom Setup"):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return
        if (game.setupData.type == enums.SetupDataType.Preset):
            await inter.response.send_message("It's a preset. Why do you want to export it?", ephemeral=True)
            return

        encodedData = base64.b64encode(base64.b64encode(str.encode(encode(game.setupData, name)))).decode()

        naming = ""
        if (name != "Custom Setup"):
            naming = f" named **{name}**"

        embed = disnake.Embed(title="Setup exported!", colour=disnake.Colour(0xcd95ff), description=f"Your **{len(game.setupData.roles)} player** setup{naming} has been exported into easy copy-pastable text.\n```{encodedData}```")

        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421")
        embed.set_footer(text="Share it with your friends!", icon_url=inter.author.display_avatar.url)

        await inter.response.send_message(embed=embed)

    @setup.sub_command(name="import", description="Import a setup that you got from your friends to a beautiful, balanced, setup.")
    async def imprt(inter:disnake.ApplicationCommandInteraction):
        game:Game.Game = Game.Game.checkForGame(inter.guild)

        if (len(game.players) == 0):
            await inter.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
            return
        if (inter.author != game.players[0]):
            await inter.response.send_message("You are not the host!", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return

        class DataRequestModal(disnake.ui.Modal):
            def __init__(self) -> None:
                components = [
                    disnake.ui.TextInput(
                        label="Setup code",
                        placeholder="Enter a setup code here...",
                        custom_id="code",
                        style=disnake.TextInputStyle.short
                    )
                ]

                super().__init__(title="Input setup code", components=components)

            async def callback(self, interaction:disnake.ModalInteraction):
                data = None
                try:
                    data = setupData.SetupData.fromData(base64.b64decode(base64.b64decode(str.encode(interaction.text_values["code"]))).decode(), game)
                except:
                    await interaction.response.send_message("Your data is invalid!", ephemeral=True)
                    return

                embed = disnake.Embed(title="Import Setup?", colour=disnake.Colour(0xcd95ff), description=f"Do you want to import this **{len(data.roles)} player** setup?")
                embed.add_field(data.generateSetupName(), data.generateSetupList())

                embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421")

                class ImportSetupConfirmation(disnake.ui.View):
                    def __init__(self, *, timeout: float | None = 180) -> None:
                        super().__init__(timeout=timeout)

                    async def on_timeout(self) -> None:
                        for child in self.children:
                            child.disabled = True

                        orgMsg = await interaction.original_message()
                        newEmbed = orgMsg.embeds[0].set_footer(text="This interaction has timed out. Use /setup import again to use the buttons.")

                        await interaction.edit_original_message(embed=newEmbed, view=self)

                    @disnake.ui.button(label="Yes", style=disnake.ButtonStyle.green, emoji="✅")
                    async def yes(self, button, confirminteraction):
                        game.setupData = data

                        if (len(game.players) == 0):
                            await confirminteraction.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
                            return
                        if (confirminteraction.author != game.players[0]):
                            await confirminteraction.response.send_message("You are not the host!", ephemeral=True)
                            return
                        if (game.hasStarted):
                            await confirminteraction.response.send_message("The game has already started!", ephemeral=True)
                            return
                        
                        game.setupData = data

                        embed = disnake.Embed(title="Setup imported!", colour=disnake.Colour(0xcd95ff), description=f"Your **{len(game.setupData.roles)} player** setup has been imported into your party.")
                        embed.add_field(game.setupData.generateSetupName(), game.setupData.generateSetupList())

                        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421")
                        embed.set_footer(text="Have fun!", icon_url=inter.author.display_avatar.url)

                        for child in self.children:
                            child.disabled = True

                        await confirminteraction.response.edit_message(embed=embed, view=self)


                    @disnake.ui.button(label="No", style=disnake.ButtonStyle.red, emoji="❌")
                    async def nah(self, button, confirminteraction):
                        if (len(game.players) == 0):
                            await confirminteraction.response.send_message("There is no game yet. Use </join:1081377829637324800> to join!", ephemeral=True)
                            return
                        if (confirminteraction.author != game.players[0]):
                            await confirminteraction.response.send_message("You are not the host!", ephemeral=True)
                            return
                        if (game.hasStarted):
                            await confirminteraction.response.send_message("The game has already started!", ephemeral=True)
                            return

                        embed = disnake.Embed(title="Setup import cancelled.", colour=disnake.Colour(0xcd95ff), description=f"Your **{len(data.roles)} player** setup has **not** been imported.")
                        embed.add_field(data.generateSetupName(), data.generateSetupList())

                        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421")
                        embed.set_footer(text="Maybe next time?", icon_url=inter.author.display_avatar.url)

                        for child in self.children:
                            child.disabled = True

                        await confirminteraction.response.edit_message(embed=embed, view=self)


                await interaction.response.send_message(embed=embed, view=ImportSetupConfirmation())             

        await inter.response.send_modal(DataRequestModal())

    @preset.autocomplete("name")
    async def presetAutocomplete(inter:disnake.ApplicationCommandInteraction, userInput:str):
        userInput=userInput.lower()
        return [string.capwords(setup.replace("~HS", "")) for setup in setupData.presetSetups.keys() if userInput in setup.lower()]
    
    @setup_addRole.autocomplete("role")
    @setup_removeRole.autocomplete("role")
    async def autoCompleteRole(inter, input):
        if (input == ""):
            return [string.capwords(e.name) for e in classes.role.Role.allRoles] + [string.capwords(e.display_name) for e in classes.contraction.Contraction.allContractions if e.show == True] 
        return [string.capwords(e.name) for e in classes.role.Role.allRoles if input.lower() in e.name.lower()] + [string.capwords(e.display_name) for e in classes.contraction.Contraction.allContractions if input.lower() in e.display_name.lower() and e.show == True] 
