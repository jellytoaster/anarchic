
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Consigliere("Consigliere", Faction.Mafia)

async def examine(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        flavorText = targetPlayer.assignedRole.investigationResults.consigliereFlavorText

        embed = disnake.Embed(title=f"**{flavorText}**", description=f"They must be a {targetPlayer.assignedRole.emoji} **{targetPlayer.assignedRole.name}**")
        embed.set_footer(text="That's interesting", icon_url=originPlayer.memberObj.avatar.url)
        embed.set_thumbnail(f"https://cdn.discordapp.com/emojis/{targetPlayer.assignedRole.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        await originPlayer.memberObj.send(embed=embed)

async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    return

class Consigliere(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is the ingenious advisor to the Mafia.")
        self.color = 0xd0021b
        self.type = "support"
        self.promotionOrder = 2
        self.order = -5
        self.emoji = "<:consigicon2:896154845130666084>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting. If there is no living <:maficon:891739940055052328>**Mafioso**, you have the __second__ priority to become the <:maficon:891739940055052328> **Mafioso**", type=classes.enums.AbilityType.Passive), classes.ability.Ability(examine, utils.notMeAndNotDead, -1, "Examine", "__Examine__ target player. You will learn their exact role.", "🔎", "examine")]
        self.constants = {"shortDescription": 'A resourceful investigator who gathers intelligence for the Mafia.', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}