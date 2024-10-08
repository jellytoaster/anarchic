
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Mafioso("Mafioso", Faction.Mafia)

async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    attack = await targetPlayer.kill(classes.enums.DeathReason.Mafia, game)
    if (attack == False):
        embed = disnake.Embed(title="**Your attack failed**", colour=disnake.Colour(0x363636))

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/878379179106787359.png?v=1")
        embed.set_footer(text="Interesting", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)

async def doNothing(targetPlayers:list, originPlayer:classes.player.Player, game):
    pass
class Mafioso(role.Role):
    def __init__(self):
        super().__init__()
        self.faction = Faction.Mafia
        self.investigationResults = investigationResults(True, "Your target is the cold blooded hitman of the mafia.")
        self.type = "killing"
        self.color = 0xd0021b
        self.order = 8
        self.emoji = "<:maficon:891739940055052328>"
        self.abilities = [classes.ability.Ability(doNothing, utils.notMeAndNotDead, -1, "Shadow Syndicate", " You have access to Mafia night meeting.", type=classes.enums.AbilityType.Passive), classes.ability.Ability(kill, utils.notMafiaAndNotDead, -1, "Assassinate", "Attack target player. They'll probably die.", "<:maficon:891739940055052328>", "kill", utils.headstart)]
        self.constants = {"shortDescription": 'The right hand man of organized crime', "winCon" : "You win when all members of the **Town** <:townicon2:896431548717473812> have been defeated."}



