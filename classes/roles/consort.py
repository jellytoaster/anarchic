
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Consort("Consort", Faction.Mafia)

def roleblockplayer(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayers[0].isRoleBlocked = True

async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return


class Consort(role.Role):
    def __init__(self):
        super().__init__()
        
        self.faction = Faction.Mafia
        self.investigationResults = investigationResults(True, "Your target is a seductive dancer.")
        self.color = 0xd0021b
        self.promotionOrder = 4
        self.type = "support"
        self.order = -1
        self.emoji = "<:consicon2:890336628269281350>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __second__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive), classes.ability.Ability(roleblockplayer, utils.notMafiaAndNotDead, -1, "Capivate", "__Distract__ target player.", self.emoji, "distract")]
        self.constants = {"shortDescription": 'A captivating performer working for the mob', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}



