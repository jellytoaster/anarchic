
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Cop("Cop", Faction.Town)

async def interrogate(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        if (targetPlayer.assignedRole.investigationResults.copSuspicious):

            embed = disnake.Embed(title="**Your target is sided with the Mafia!**", colour=disnake.Colour(0xd0021b), description=f"** **")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/925794458136637561.webp?size=96&quality=lossless")
            embed.set_footer(text="Try convincing the other townies with your info.", icon_url=originPlayer.memberObj.display_avatar.url)
            await originPlayer.memberObj.send(embed=embed)
        else:
            embed = disnake.Embed(title="**Your target seems Innocent. You conclude that they are not suspicious.**", colour=disnake.Colour(0x7ed321), description=f"** **")
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/871791900003282964/seems_innocent_-removebg-preview.png")
            embed.set_footer(text="Try convincing the other townies with your info.", icon_url=originPlayer.memberObj.display_avatar.url)
            await originPlayer.memberObj.send(embed=embed)

class Cop(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):

        super().__init__(name, faction)
        self.investigationResults = investigationResults(False, "Your target is the law enforcer of the town.")
        self.color = 0x7ed321
        self.type = "investigative"
        self.order = 9
        self.emoji = "<:copicon2:889672912905322516>"
        self.abilities = [classes.ability.Ability(interrogate, utils.notMeAndNotDead, -1, "Interrogate", " __Investigate__ target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", "📝", "interrogate")]
        self.constants = {"shortDescription": 'A reliable law enforcer, skilled at keeping evildoers in check', "winCon" : "Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**"}