
import utils
import classes.role as role
import classes.ability
import classes.player
from classes.enums import Faction
from classes.investigationResults import investigationResults

async def frame(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    targetPlayer.assignedRole.investigationResults.copSuspicious = True
    
    if (len(game.mafNightKill) > 0):
        targetPlayer.assignedRole.investigationResults.trackerTargetted = [game.mafNightKill[0]]

        for i in game.playervar:
            try:
                i.assignedRole.investigationResults.lookoutVisitedBy.remove(targetPlayer)
            except:
                    continue

        game.mafNightKill[0].assignedRole.investigationResults.lookoutVisitedBy = [targetPlayer]
    
async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return

class Framer(role.Role):
    def __init__(self):

        super().__init__()
        self.faction = Faction.Mafia
        self.investigationResults = investigationResults(True, "Your target is a skilled counterfeiter who fabricates information.")
        self.color = 0xd0021b
        self.promotionOrder = 1
        self.type = "deception"
        self.order = 1000
        self.emoji = "<:frameicon2:890365634913902602>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __third__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive), classes.ability.Ability(frame, utils.notMafiaAndNotDead, -1, "Frame", " __Frame__ target player. They will appear as **Suspicious** for \🔎 **Town Investigatives**, such as showing as siding with the Mafia and visiting the Mafia night kill.", "🎞️", "frame")]
        self.constants = {"shortDescription": 'A captivating performer working for the mob', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}




