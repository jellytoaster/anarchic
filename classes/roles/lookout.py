
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Lookout("Lookout", Faction.Town)

async def look(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        visitedPlayers = targetPlayer.assignedRole.investigationResults.lookoutVisitedBy
        if (originPlayer in visitedPlayers):
            visitedPlayers.remove(originPlayer)

        if (len(visitedPlayers)) == 0:
            await originPlayer.memberObj.send(embed=disnake.Embed(title=f"Nobody visited your target last night.", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=originPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url))
        else:
            if len(visitedPlayers) > 1:
                title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
            else:
                title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

            embed = disnake.Embed(title=f"Your target was visited by {title} last night!", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
            await originPlayer.memberObj.send(embed=embed)

class Lookout(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target is a sleepless nightwatcher.")
        self.color = 0x7ed321
        self.type = "investigative"
        self.order = 100
        self.emoji = "<:loicon2:889673190392078356>"
        self.abilities = [classes.ability.Ability(look, utils.notMeAndNotDead, -1, "Overlook", "__Overlook__ target player. You will learn who visits your target.", "🔦", "watch")]
        self.constants = {"shortDescription": 'A rogue enforcer with an eye for justice', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}




