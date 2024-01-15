import disnake
import os
import sys
import disnake.ext.commands.errors
import disnake.utils
from disnake import Option, OptionType
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

import config
import classes.game
import utils


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

    @commands.slash_command(name="delcategory", description="Delete the current category. Debugging purposes only.", guild_ids=config.TEST_GUILDS)
    @commands.check(adminCheck)
    async def delca(inter):
        if (inter.author.id not in config.WHITELIST):
            await inter.response.send_message("no", ephemeral=True)
            return
        for i in inter.channel.category.channels:
            await i.delete()

        await inter.channel.category.delete()

    @commands.slash_command(name="restart", description="Restart the bot. Developers only.", guild_ids=config.TEST_GUILDS)
    @commands.check(adminCheck)
    async def restart(inter):
        await inter.response.send_message("Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)


    @commands.slash_command(name="forcejoin", description="Force someone to join the game.", options=[Option("player", "The user to harass and forcefully join", OptionType.user, True)], guild_ids=config.TEST_GUILDS)
    @commands.check(adminCheck)
    async def fj(inter, player):
        game = classes.game.Game.checkForGame(player.guild)
        if (player in game.players):
            await iter.response.send_message("They are already in the game! Did you mean to use </leave:1081377829637324801> instead?", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("They're not allowed to join when a game is in progress!", ephemeral=True)
            return
        
        game.players.append(player)

        embed = disnake.Embed(title=f"{player.display_name} has joined the party!", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0x8ef3ff))
        embed.set_thumbnail(url=player.display_avatar.url)

        await inter.response.send_message(embed=embed)
        