
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Framer("Framer", Faction.Mafia)

async def frame(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        targetPlayer.assignedRole.investigationResults.copSuspicious = True
        
        targetPlayer.assignedRole.investigationResults.trackerTargetted = [game.mafNightKill]

        for i in game.playervar:
            try:
                i.assignedRole.investigationResults.lookoutVisitedBy.remove(targetPlayer)
            except:
                 continue
        
        game.mafNightKill.assignedRole.investigationResults.lookoutVisitedBy = [targetPlayer]

async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return

class Framer(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):

        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is a skilled counterfeiter who fabricates information.")
        self.color = 0xd0021b
        self.promotionOrder = 1
        self.type = "deception"
        self.order = 1000
        self.emoji = "<:frameicon2:890365634913902602>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __third__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive), classes.ability.Ability(frame, utils.notMeAndNotDead, -1, "Interrogate", " __Investigate__ target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", "📝", "interrogate")]
        self.constants = {"shortDescription": 'A captivating performer working for the mob', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}




