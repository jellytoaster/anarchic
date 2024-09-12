
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Jester("Jester", Faction.Neutral)

async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    await targetPlayer.kill(classes.enums.DeathReason.Jester, game, force=True)

async def roleBlock(targetPlayers:list, originPlayer:classes.player.Player, game):
    for i in targetPlayers:
        i.isRoleBlocked = True

class Jester(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Neutral
        self.investigationResults = investigationResults(False, "Your target is a crazed lunatic waiting to be hung.")
        self.type = "evil"
        self.color = 0xf1cbe2
        self.order = 1
        self.emoji = "<:jesticon2:889968373612560394>"
        self.abilities = [classes.ability.Ability(kill, utils.playersWhoVotedGuilty, 1, "Haunt", "Haunt a player so they die.", "<:jesticon2:889968373612560394>", "haunt", utils.jesterDeathCheck, classes.enums.AbilityType.Night),classes.ability.Ability(roleBlock, utils.playersWhoVotedGuilty, -1, "jester roleblock", "roleblock guiltiers", "💀", "roleblock", utils.jesterDeathCheck, classes.enums.AbilityType.PassiveEarly, False)]
        self.constants = {"shortDescription": 'A crazed lunatic who wants to be publicly executed', "winCon" : "Get yourself **Lynched <:jesticon2:889968373612560394>**"}
