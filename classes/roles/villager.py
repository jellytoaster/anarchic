
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Villager("Villager", Faction.Town)

class Villager(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        # imagine being a villager honestly
        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target is a dedicated to the justice of all evildoers.")
        self.color = 0x7ed321
        self.type = "vanilla"
        self.order = 0
        self.emoji = "<:townicon2:896431548717473812>"
        self.abilities = []
        self.constants = {"shortDescription": "A humble citizen who's fallen into a state of uneasy distrust", "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}