
import utils
import classes.role as role
import disnake
import random
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Headhunter("Headhunter", Faction.Neutral)

def twoPoints(me, game):
    return me.externalRoleData["points"] == 2

def headHunterN1Targetting(me, allPlayers, game):
    return [player for player in allPlayers if player.assignedRole.faction == classes.enums.Faction.Town and player.assignedRole.name != "mayor"]

async def firstTarget(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.externalRoleData["points"] = 0

    if targetPlayers == []:
        originPlayer.externalRoleData["target"] = None
        targetembed = disnake.Embed(title=f"**Well that sucks...**", colour=disnake.Colour(0x39556b), description=f"Looks nobody was an englible candidate for you! You may choose a target the following night.")

        targetembed.set_thumbnail(url=targetPlayer.memberObj.display_avatar.url)
        targetembed.set_footer(text="...", icon_url=targetPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=targetembed)
        return
    
    originPlayer.externalRoleData["target"] = random.choice(targetPlayers)


    targetPlayer = originPlayer.externalRoleData["target"]

    targetembed = disnake.Embed(title=f"**Your target is {targetPlayer.memberObj.name}.**", colour=disnake.Colour(0x39556b), description=f"Your target has wronged you and now it's time for them to pay. Get them lynched in order to win.")

    targetembed.set_thumbnail(url=targetPlayer.memberObj.display_avatar.url)
    targetembed.set_footer(text="If your target dies at night, you can choose another one at night.", icon_url=targetPlayer.memberObj.display_avatar.url)
    await originPlayer.memberObj.send(embed=targetembed)
async def vengance(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.externalRoleData["target"] = targetPlayers[0]

async def rest(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.kill(classes.enums.DeathReason.Headhunter, game, True)
class Headhunter(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target sentences the condemned to their fate.")
        self.color = 0x334f64
        self.type = "evil"
        self.order = 10
        self.emoji = "<:hhicon2:891429754643808276>"
        self.abilities = [classes.ability.Ability(firstTarget, headHunterN1Targetting, -1, "Vengeful", "A random Town :town~2: starts the game as your Target. The Mayor :mayoricon: cannot be your Target this way.", "<:hhicon2:891429754643808276>", "target", utils.notDead, classes.enums.AbilityType.DayOne), classes.ability.Ability(vengance, utils.notMeAndNotDead, -1, "Vengance", "__Astrally__ mark target player. They are now your new __Target__.", "<:hhicon2:891429754643808276>", "target", utils.notDead), classes.ability.Ability(rest, utils.literallyAnyone, 1, "rest", "you win!", "🤓", "h", twoPoints, classes.enums.AbilityType.PassiveEarly, False)]
        self.constants = {"shortDescription": 'A vengeance-seeking outsider who holds a grudge against the town', "winCon" : "Get two of your targets <:lynch:1010226047456915547> **lynched**"}


