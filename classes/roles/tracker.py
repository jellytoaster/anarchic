
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Tracker("Tracker", Faction.Town)

async def track(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]

        if (len(targetPlayer.assignedRole.investigationResults.trackerTargetted) == 0):
            embed = disnake.Embed(title=f"Your target did not visit anyone last night.", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=targetPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url)
            await originPlayer.memberObj.send(embed=embed)
            return

        visitedPlayers = targetPlayer.assignedRole.investigationResults.trackerTargetted

        if len(visitedPlayers) > 1:
            title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
        else:
            title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

        embed = disnake.Embed(title=f"Your target visited {title} last night!", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)

class Tracker(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target watches who others visit.")
        self.color = 0x7ed321
        self.type = "investigative"
        self.order = 100
        self.emoji = "<:trackicon:922885543812005949>"
        self.abilities = [classes.ability.Ability(track, utils.notMeAndNotDead, -1, "Track", " Track target player. Follow target player to know who they visit", "🔦", "track")]
        self.constants = {"shortDescription": 'A skilled pathfinder who scouts to gather info', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}




