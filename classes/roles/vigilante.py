
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from classes.investigationResults import investigationResults

async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    success = await targetPlayer.kill(classes.enums.DeathReason.Enforcer, game)
    if (success and targetPlayer.assignedRole.faction == classes.enums.Faction.Town):
        embed = disnake.Embed(title="**You could not get over the guilt of killing a Townie <:town:1007768656341651547>**", colour=disnake.Colour(0x7ed321), description="You have lost all charges of __Eliminate__ <:vgicon:890339050865696798>")

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/890339050865696798.webp?size=96&quality=lossless")
        embed.set_footer(text="You can still help your team", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
        originPlayer.assignedRole.abilities[0].charges = 0

def dayone(player, game):
    if (game.dayNum == 1):
        return False
    return True

class Vigilante(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Town
        self.investigationResults = investigationResults(False, "Your target is willing to bend the law to enact justice.")
        self.color = 0xd0021b
        self.order = 8
        self.type = "killing"
        self.emoji = "<:vgicon:890339050865696798>"
        self.abilities = [classes.ability.Ability(kill, utils.notMeAndNotDead, 3, "Shoot", "__Attack__ target player. If you kill a **Town <:town:1007768656341651547>**, lose all charges of __Eliminate__ <:vgicon:890339050865696798>. Cannot be used **Night 1 <:moon:934556372421451776>**.", "<:vgicon:890339050865696798>", "shoot", dayone)]
        self.constants = {"shortDescription": 'A skilled observer who keeps an eye on the evils', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}




