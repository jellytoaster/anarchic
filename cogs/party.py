import asyncio
import cogs.gameplay.begin
    
from classes.game import Game

import disnake
from disnake.ext import commands

class PartyCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="party", description="View the current party")
    async def party(self, inter:disnake.ApplicationCommandInteraction):
        game = Game.checkForGame(inter.guild)

        if (len(game.players) == 0):
            await inter.response.send_message("There isn't a party to view.", ephemeral=True)
            return

        embed = disnake.Embed(title=f"{game.players[0].name}'s Party", description=f"**Current Players:** `{str(len(game.players))}`\n{game.genPlayerList()}", colour=disnake.Colour(0x8ef3ff))
        embed.set_thumbnail(url=inter.guild.icon.url)


        onlinePlayers = 0
        for i in game.players:
            i:disnake.Member
            if (i.status != disnake.Status.offline):
                onlinePlayers += 1

        embed.set_footer(text=f"{onlinePlayers}/{len(game.players)} players online", icon_url=inter.author.avatar.url)

        await inter.response.send_message(embed=embed)
    @commands.slash_command(name="join", description="Join the game!")
    async def join(self, inter:disnake.ApplicationCommandInteraction):
        game = Game.checkForGame(inter.guild)
        if (inter.author in game.players):
            await inter.response.send_message("You are already in the game! Did you mean to use </leave:1081377829637324801> instead?", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("You're not allowed to join when a game is in progress!", ephemeral=True)
            return
        
        game.players.append(inter.author)

        embed = disnake.Embed(title=f"{inter.author.display_name} has joined the party!", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0x8ef3ff))
        embed.set_thumbnail(url=inter.author.display_avatar.url)

        await inter.response.send_message(embed=embed)
        
    @commands.slash_command(description="Leave the game!")
    async def leave(self, inter:disnake.ApplicationCommandInteraction):
        game = Game.checkForGame(inter.guild)
        if (inter.author not in game.players):
            await inter.response.send_message("You're not in the game! Did you mean to use </join:1081377829637324800> instead?", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("You're not allowed to leave when a game is in progress!", ephemeral=True)
        
        game.players.remove(inter.author)

        embed = disnake.Embed(title=f"{inter.author.display_name} has left the party!", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0xf5cbff))
        embed.set_thumbnail(url=inter.author.display_avatar.url)

        if (len(game.players) == 0):
            embed.title = "The game has ended with the host's depart."
        
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Kick a player from the game", options=[disnake.Option(name="player", description="The person to kick", type=disnake.OptionType.user, required=True)])
    async def kick(self, inter:disnake.ApplicationCommandInteraction, player):
        game = Game.checkForGame(inter.guild)

        if (game.isHost(inter.author) == False):
            await inter.response.send_message("You're not the host.", ephemeral=True)
            return
        if (player not in game.players):
            await inter.response.send_message("That player is not in the game.", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("You're not allowed to kick when a game is in progress!", ephemeral=True)
        
        game.players.remove(player)

        embed = disnake.Embed(title=f"{player.display_name} has been kicked.", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0xf5cbff))
        embed.set_thumbnail(url=player.display_avatar.url)
        
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Make a new player the host", options=[disnake.Option(name="player", description="The person to promote", type=disnake.OptionType.user, required=True)])
    async def host(self, inter:disnake.ApplicationCommandInteraction, player):
        game = Game.checkForGame(inter.guild)

        if (game.isHost(inter.author) == False):
            await inter.response.send_message("You're not the host.", ephemeral=True)
            return
        if (player not in game.players):
            await inter.response.send_message("That player is not in the game.", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("You're not allowed to promote when a game is in progress!", ephemeral=True)


        game.players[game.players.index(inter.author)], game.players[game.players.index(player)] = game.players[game.players.index(player)], game.players[game.players.index(inter.author)]

        embed = disnake.Embed(title=f"{player.display_name} has been promoted!", description=f"**Current Players:** `{str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** {game.setupData.generateSetupNameWithoutNumbers()}", colour=disnake.Colour(0xf5cbff))
        embed.set_thumbnail(url=player.display_avatar.url)
        
        await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Start the game!")
    async def start(self, inter:disnake.ApplicationCommandInteraction):
        game = Game.checkForGame(inter.guild)
        if (game.hasStarted == True):
            await inter.response.send_message("The game has already started!", ephemeral=True)
            return
        if (game.isHost(inter.author) == False):
            await inter.response.send_message("You're not the host.", ephemeral=True)
            return
        if (len(game.players) < 5 and inter.author.id != 839842855970275329):
            await inter.response.send_message("You'll need at least 5 players to start any game!", ephemeral=True)
            return
        if (len(game.setupData.roles) != len(game.players)):
            await inter.response.send_message("The amount of players don't match with the setup count! You'll need **{}** players to start the game.".format(len(game.setupData.roles)), ephemeral=True)
            return
        
        # add player cont checking later
        
        game.hasStarted = True
        embed = disnake.Embed(title="Starting game...", colour=disnake.Colour(0xd7b1f9), description="We're currently setting up the required channels and roles for the game to operate. Please stand by...")
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%3Fwidth%3D468%26height%3D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png")

        await inter.response.send_message(embed=embed)

        game.channelStartChannel = inter.channel
        await cogs.gameplay.begin.prep(game)

        embed = disnake.Embed(title="A game has started!", colour=disnake.Colour(0xd7b1f9), description=f"Everyone in the game should go to {game.channelTownSquare.mention} for the game to begin.")
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%3Fwidth%3D468%26height%3D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png")

        class HelpView(disnake.ui.View):
            @disnake.ui.button(label="Not seeing the channels?", style=disnake.ButtonStyle.blurple, emoji="👀")
            async def helpButton(self, button, inter):
                embed = disnake.Embed(title="If you can't see the channels", colour=disnake.Colour(0xb5f69e), description="Due to Discord's new channel picking features, Anarchic channels may not appear when they are created as they are not in your channel list, to fix this without constantly having to add it in your channel picker, enable **Show all channels** in the server's options menu.")

                embed.set_image(url="https://media.discordapp.net/attachments/872257788015951953/1150497478416801842/image.png?width=195&height=451")
                embed.set_footer(text="Have fun!")

                await inter.response.send_message(embed=embed, ephemeral=True)

            def __init__(self) -> None:
                super().__init__()

        await inter.edit_original_message(embed=embed, view=HelpView())

        await asyncio.sleep(2)
        await cogs.gameplay.begin.start(game)
