import disnake
import asyncio
import classes.game
from disnake.ext import commands

class endGame(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(name="end", description="End the current game. Can only be used when an existing game is finished.")
    async def endGame(self, inter:disnake.ApplicationCommandInteraction):
        currentGame = classes.game.Game.checkForGame(inter.guild)
        if (currentGame.finished == False):
            await inter.response.send_message("There has to be a finished game for this command to work.", ephemeral=True)
            return
        
        if (inter.channel != currentGame.channelTownSquare):
            await inter.response.send_message("You have to use this command in " + currentGame.channelTownSquare.mention + ".", ephemeral=True)
            return
        
        embed = disnake.Embed(title="Thanks for playing **Anarchic**!", colour=disnake.Colour(0xe07d7e), description="**:clock10: Deleting the channels in 5 seconds. Enjoying the bot? Consider voting for us [here](https://top.gg/bot/887118309827432478/vote)!**")
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/cBq_CGTA8KOw8vWobvuhZ3AKTEe0zii9yV2f7jZuLe0/%3Fwidth%3D374%26height%3D374/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png")

        embed.set_footer(text="Use /start to start another game.", icon_url=self.bot.user.display_avatar.url)

        await inter.response.send_message(embed=embed)

        await asyncio.sleep(5)

        for i in inter.channel.category.channels:
            await i.delete()

        await inter.channel.category.delete()

        currentGame.reset()