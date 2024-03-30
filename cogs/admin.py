import disnake
import os
import classes.changelog
import classes.contraction
import sys
import disnake.ext.commands.errors
import disnake.utils
from disnake import Option, OptionType
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction
import cogs.basic as basic
import classes.role as roles
import config
import classes.game
import utils
import string


class adminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def adminCheck(inter):
        def predicate(inter):
            return inter.author.id in config.WHITELIST
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter:ApplicationCommandInteraction, error:Exception):
        if (type(error) == disnake.ext.commands.errors.CheckFailure):
            await inter.response.send_message("You don't have permission!", ephemeral=True)
        else:
            try:
                await inter.response.send_message(f"Something went wrong! Error:\n```{str(error)}```", ephemeral=True)
            except:
                pass
            finally:
                raise error

    @commands.slash_command(name="delcategory", description="Delete the current category. Debugging purposes only.", guild_ids=config.ADMIN_GUILDS)
    @commands.check(adminCheck)
    async def delca(inter):
        if (inter.author.id not in config.WHITELIST):
            await inter.response.send_message("no", ephemeral=True)
            return
        for i in inter.channel.category.channels:
            await i.delete()

        await inter.channel.category.delete()

    @commands.slash_command(name="restart", description="Restart the bot. Developers only.", guild_ids=config.ADMIN_GUILDS)
    @commands.check(adminCheck)
    async def restart(inter):
        await inter.response.send_message("Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)


    @commands.slash_command(name="forcejoin", description="Force someone to join the game.", options=[Option("player", "The user to harass and forcefully join", OptionType.user, True)], guild_ids=config.ADMIN_GUILDS)
    @commands.check(adminCheck)
    async def fj(inter, player):
        game = classes.game.Game.checkForGame(player.guild)

        if (game.hasStarted):
            await inter.response.send_message("They're not allowed to join when a game is in progress!", ephemeral=True)
            return
        
        game.players.append(player)

        embed = disnake.Embed(title=f"{player.display_name} has joined the party!", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0x8ef3ff))
        embed.set_thumbnail(url=player.display_avatar.url)

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="sendchangelog", description="send changelog to a channel", options=[Option("channel", "wher", OptionType.channel, True), Option("version", "ver", OptionType.string, True)], guild_ids=config.ADMIN_GUILDS)
    @commands.check(adminCheck)
    async def sendchangelog(self, inter, channel, version):
        embed = classes.changelog.Changelog.getChangelog(version).makeEmbed().set_footer(text="Have fun!", icon_url=self.bot.user.display_avatar.url)
        await channel.send(embed=embed)
        await inter.response.send_message('done', ephemeral=True)

    @commands.slash_command(name="sendcomingsoon", description="send a coming soon changelog to a channel", options=[Option("channel", "wher", OptionType.channel, True), Option("version", "ver", OptionType.string, True)], guild_ids=config.ADMIN_GUILDS)
    @commands.check(adminCheck)
    async def sendSoon(self, inter, channel, version):
        embed = classes.changelog.Changelog.getChangelog(version).makeJustHighlights().set_footer(text="Coming soon!", icon_url=self.bot.user.display_avatar.url)
        await channel.send(embed=embed)
        await inter.response.send_message('done', ephemeral=True)

    @commands.slash_command(name="buildembed", description="Build an embed based on its role data. A human should modify the generated code first.", options=[Option("role", "What role?", disnake.OptionType.string, True)], guild_ids=config.DEV_GUILDS)
    @commands.check(adminCheck)
    async def buildEmbed(inter, role):
        selectedRole:roles.Role = roles.Role.toRole(role.lower())

        embed = disnake.Embed(title=f"Your role is {string.capwords(selectedRole.name)}", description="[FLAVOR TEXT HERE.]", color=selectedRole.color)
        embed.set_thumbnail(selectedRole.getIconUrl())

        embed.add_field("**Atk :crossed_swords::**", "idk change this")
        embed.add_field("**Res :shield::**", "idk change this")

        embed.add_field("**Faction :pushpin::**", f"**{string.capwords(selectedRole.faction.value)}** {utils.emojis[selectedRole.faction.value.lower()]}", inline=False)

        embed.add_field("**Type :low_brightness::**", f"**{string.capwords(selectedRole.type)}**", inline=False)

        # Generate Abilities
        abilities = ""
        emojis = {"passive": "<:passive:936343832696606800>", "night": "<:moon:934556372421451776>"}
        for i in selectedRole.abilities:
            abilities += f"{emojis[i.type.value]} **{i.name} | {utils.chargeCountSimple(i.charges)}**"

        if (abilities == ""):
            abilities = ":x: **None**"

        embed.add_field("**Abilities :door::**", abilities, inline=False)

        attributes = ""
        for i in selectedRole.abilities:
            attributes += f"{i.emoji} **{i.name}** - {i.description}**"

        if (attributes == ""):
            attributes = ":x: **None**"

        embed.add_field("**Attributes :star2::**", attributes, inline=False)

        embed.add_field("**Win Condition :trophy:**", "idfk you tell me", inline=False)

        embed.add_field("**Investigation Results 🔎**", f"  **Cop <:copicon2:889672912905322516>:** {utils.innoFlavor(selectedRole.investigationResults.copSuspicious)}\n**Consigliere <:consigicon2:896154845130666084>:** {selectedRole.investigationResults.consigliereFlavorText} They must be a **{selectedRole.name}** {selectedRole.emoji}", inline=False)

        embed.set_footer(text=f"{string.capwords(selectedRole.faction.value)} {string.capwords(selectedRole.type)} {classes.contraction.Contraction.getContraction(selectedRole.faction.value.lower(), selectedRole.type.lower()).emoji}")

        class MakeMeCode(disnake.ui.View):
            def __init__(self, *, timeout: float | None = 180) -> None:
                super().__init__(timeout=timeout)

            @disnake.ui.button(label="Make me code!")
            async def generateCode(self, button, interaction):
                code = "```\n"

                code += f"disnake.Embed(title=\"{embed.title}\", description=\"{embed.description}\", color=disnake.Color({embed.color.__str__().replace('#', '')})).set_thumbnail(url=\"{embed.thumbnail.url}\").add_field(\"{embed.fields[0].name}\", \"{embed.fields[0].value}\").add_field(\"{embed.fields[1].name}\", \"{embed.fields[1].value}\").add_field(\"{embed.fields[2].name}\", \"{embed.fields[2].value}\", inline=False).add_field(\"{embed.fields[3].name}\", \"{embed.fields[3].value}\", inline=False).add_field(\"{embed.fields[4].name}\", \"{embed.fields[4].value}\", inline=False).add_field(\"{embed.fields[5].name}, {embed.fields[5].value}\", inline=False).add_field(\"{embed.fields[6].name}\", \"{embed.fields[6].value}\", inline=False).add_field(\"{embed.fields[7].name}\", \"{embed.fields[7].value}\", inline=False).set_footer(text=\"{embed.footer.text}\")"

                code += "```"

                await interaction.response.send_message(code)

        await inter.response.send_message(embed=embed, view=MakeMeCode())

    @buildEmbed.autocomplete("role")
    async def autoCompleteRole(inter, input):
        return [string.capwords(e.name) for e in classes.role.Role.allRoles] 