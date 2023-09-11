import disnake
from classes.game import Game
from disnake.ext import commands

class PartyCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="join", description="Join the game!")
    async def join(self, inter:disnake.ApplicationCommandInteraction):
        game = Game.checkForGame(inter.guild)
        if (inter.author in game.players):
            await inter.response.send_message("You are already in the game! Did you mean to use </leave:1081377829637324801> instead?", ephemeral=True)
            return
        if (game.hasStarted):
            await inter.response.send_message("You're not allowed to leave when a game is in progress!", ephemeral=True)
        
        game.players.append(inter.author)

        embed = disnake.Embed(title=f"{inter.author.name}#{inter.author.discriminator} has joined the party!", description=f"**Current Players:**` {str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** setup", colour=disnake.Colour(0x8ef3ff))
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

        embed = disnake.Embed(title=f"{inter.author.name}#{inter.author.discriminator} has left the party!", description=f"**Current Players:**` {str(len(game.players))}`\n**Current Host:** {game.findHostMention()}\n**Setup:** setup", colour=disnake.Colour(0xf5cbff))
        embed.set_thumbnail(url=inter.author.display_avatar.url)

        if (len(game.players) == 0):
            embed.title = "The game has ended with the host's depart."
        
        await inter.response.send_message(embed=embed)