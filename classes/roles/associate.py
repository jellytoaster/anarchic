
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Associate("Associate", Faction.Mafia)

async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return

class Associate(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Mafia
        self.investigationResults = investigationResults(True, "Your target is a loyal goon affiliated with the Mafia.")
        self.color = 0xd0021b
        self.promotionOrder = 100
        self.order = 0
        self.type = "vanilla"
        self.emoji = "<:assoicon:1006333104920735787>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __last__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive)]
        self.constants = {"shortDescription": 'An agent of organized crime, working for the Mafia.', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}



