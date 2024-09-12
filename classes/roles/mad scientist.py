
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

@classes.ability.invisible
@classes.ability.passive_ability(
        targetingOptions=utils.nobody,
        charges=-1,
        name="Shadow Syndicate",
        description="You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have a chance to become the <:maficon:891739940055052328> **Mafioso**",
)
async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return


@classes.ability.ability(
    utils.notDead,
    -1,
    "Miracle Injection",
    "Inject a player, preventing them from dying and preventing investigations for tonight. You will know if they are attacked. You may target yourself.",
    "🧪",
    "inject"
)
async def miracleinjection(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    targetPlayer.defended = (originPlayer, True)

class Mad_Scientist(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Mafia
        self.investigationResults = investigationResults(True, "Your target is a crazed scientist.")
        self.color = 0xd0021b
        self.type = "support"
        self.promotionOrder = 5
        self.order = 0
        self.emoji = "<:recon:1200834864845438977>"
        self.constants = {"shortDescription": 'A crazed scientist able to manipulate faces at will.', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}