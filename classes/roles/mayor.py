
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
import classes.game
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Mayor("Mayor", Faction.Town)

async def reveal(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.votingPower = 3
    print(originPlayer.playerSelectedAbility)

async def broadcastReveal(targetPlayers:list, originPlayer:classes.player.Player, game:classes.game.Game):
    embed = disnake.Embed(title=f"{originPlayer.memberObj.name} has revealed to be the mayor!", colour=disnake.Colour(0x7ed321), description=f"{originPlayer.memberObj.name} will now have __three__ votes for all voting procedures for the rest of the game.")

    embed.set_image(url="https://media.discordapp.net/attachments/765738640554065962/886652670230790214/unknown.png?ex=6612cca5&is=660057a5&hm=ee4302bd529d66529a8c97b2f6203b95a357afd486def2e0de485b5d4a704405&=&format=webp&quality=lossless&width=196&height=200")
    embed.set_thumbnail(url=originPlayer.assignedRole.getIconUrl())
    embed.set_footer(text="Good luck", icon_url=originPlayer.memberObj.avatar.url)

    await game.channelTownSquare.send(embed=embed)

def canBroadcast(originPlayer, game):
    return originPlayer.playerSelectedAbility == 0

class Mayor(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target leads the town in trials.")
        self.color = 0x7ed321
        self.type = "support"
        self.order = 0
        self.emoji = "<:mayoricon:922566007946629131>"
        self.abilities = [classes.ability.Ability(reveal, utils.nobody, 1, "Reveal", "Reveal yourself as the mayor the next day. You will have __three__ votes in all voting procedures until the rest of the game.", "<:mayoricon:922566007946629131>", "reveal", requiredTargets=0), classes.ability.Ability(broadcastReveal, utils.nobody, 1, "broadcastreveal", "a", usable=canBroadcast, type=classes.enums.AbilityType.PassiveDawn, visible=False)]
        self.alwaysUseAbilitySelection = True
        self.constants = {"shortDescription": "The leader of the town", "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}