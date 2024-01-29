
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Recon("Recon", Faction.Mafia)

async def stakeout(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    visitedPlayers = targetPlayer.whoVisitedMe()
    visitedPlayers.remove(originPlayer)

    if (len(visitedPlayers)) == 0:
        await originPlayer.memberObj.send(embed=disnake.Embed(title=f"Nobody visited your target last night.", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=originPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url))
    else:
        if len(visitedPlayers) > 1:
            title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
        else:
            title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

        embed = disnake.Embed(title=f"Your target was visited by {title} last night!", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
    
    if (len(targetPlayer.nightTargettedPlayers) == 0):
        embed = disnake.Embed(title=f"Your target did not visit anyone last night.", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=targetPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
        return

    visitedPlayers = targetPlayer.nightTargettedPlayers

    if len(visitedPlayers) > 1:
        title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
    else:
        title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

    embed = disnake.Embed(title=f"Your target visited {title} last night!", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
    await originPlayer.memberObj.send(embed=embed)
async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return


class Recon(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target lurks in shadows.")
        self.color = 0xd0021b
        self.type = "support"
        self.promotionOrder = 4
        self.order = 0
        self.emoji = "<:recon:1200834864845438977>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __fourth__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive), classes.ability.Ability(stakeout, utils.notMafiaAndNotDead, -1, "Stakeout", "__Stake out__ target player. You will learn who your target visits, and who visits your target.", "🔭", "watch over")]
        self.constants = {"shortDescription": 'A counterintelligence agent, specialized in the gathering reconnaissance.', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}




