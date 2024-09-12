
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
from classes.enums import Faction
from  classes.investigationResults import investigationResults

# UNINISHED!!! DO NOT FORGET TO FINISH

def init():
    Jailkeeper("Jailkeeper", Faction.Town)

def jailkeep(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayers[0].isRoleBlocked = True

    targetPlayers[0].defended = (originPlayer, False)

class Jailkeeper(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Town
        self.investigationResults = investigationResults(False, "Your target owns a jail.")
        self.color = 0x7ed321
        self.type = "protective"
        self.order = -1
        self.emoji = "<:jkicon:1226319232925565049>"
        self.abilities = [classes.ability.Ability(jailkeep, utils.notDead, -1, "Jailkeep", "__Jailkeep__ target player. They will be __roleblocked__ and __protected__ for the night. You will **not** be notified if they are attacked.", self.emoji, "jailkeep")]
        self.constants = {"shortDescription": 'The one person that owns a jail for some reason', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}



