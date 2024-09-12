
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Doctor("Doctor", Faction.Town)

async def protect(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        targetPlayer.defended = (originPlayer, True)

class Doctor(role.Role):
    def __init__(self):

        super().__init__()
        self.faction = Faction.Town
        self.investigationResults = investigationResults(False, "Your target is a profound surgeon.")
        self.color = 0x7ed321
        self.type = "protective"
        self.order = 10
        self.emoji = "<:docicon2:890333203959787580>"
        self.abilities = [classes.ability.Ability(protect, utils.notDead, -1, "Heal", "__Heal__ target player. You will grant your target a __Powerful Resistance__ for the night. Both you and your target will be notified if your target is __attacked__.", "💖", "heal")]
        self.constants = {"shortDescription": 'A secret surgeon who heals people at night', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}



