import disnake
import traceback
import utils

async def handle(channel, error):
    embed = disnake.Embed(title="Oops, an error occured!", colour=disnake.Colour(0xd0021b), description=f"```{str(error)}```{utils.errorToText(str(error))}")

    embed.set_footer(text="Use /end to end the game.")
    embed.add_field(name="Potential Fix", value=utils.errorToFix(str(error)))
    await channel.send(embed=embed)

    if ("This error is undocumented and has been automatically reported to the developers." in embed.description):
        traceback.print_stack()
        traceback.print_exc()