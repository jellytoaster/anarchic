
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
from classes.enums import Faction
from  classes.investigationResults import investigationResults

# UNINISHED!!! DO NOT FORGET TO FINISH

def init():
    Attendant("Attendant", Faction.Town)

def roleblockplayer(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayers[0].isRoleBlocked = True

class Attendant(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target soothes those around them.")
        self.color = 0x7ed321
        self.type = "support"
        self.order = -1
        self.emoji = "<:atticon:957688274418286602>"
        self.abilities = [classes.ability.Ability(roleblockplayer, utils.notDead, -1, "Attend", "__Distract__ target player.", self.emoji, "attend to")]
        self.constants = {"shortDescription": 'An attractive companion with a soothing aura', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}



