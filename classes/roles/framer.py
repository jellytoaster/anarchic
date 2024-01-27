
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Framer("Framer", Faction.Mafia)

async def frame(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        targetPlayer.assignedRole.investigationResults.copSuspicious = True
        
        targetPlayer.assignedRole.investigationResults.trackerTargetted = [game.mafNightKill]

        for i in game.playervar:
            try:
                i.assignedRole.investigationResults.lookoutVisitedBy.remove(targetPlayer)
            except:
                 continue
        
        game.mafNightKill.assignedRole.investigationResults.lookoutVisitedBy = [targetPlayer]

class Framer(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):

        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is a skilled counterfeiter who fabricates information.")
        self.color = 0xd0021b
        self.promotionOrder = 1
        self.type = "deception"
        self.order = 1000
        self.emoji = "<:frameicon2:890365634913902602>"
        self.roleEmbed = disnake.Embed(title="**Your role is Framer**", colour=disnake.Colour(0xd0021b), description="A skilled deceiver who sets investigations astray").set_thumbnail(url="https://cdn.discordapp.com/emojis/890365634913902602.webp?size=96&quality=lossless").set_footer(text="Mafia Deception 🎭").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Type 🔅:**", value="**Unique Information \🎭**", inline=False).add_field(name="**Abilities \🎭:**", value="**<:passive:936343832696606800> Legacy | Passive\n<:moon:934556372421451776> Frame | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:framed:890365634913902602> Legacy -** If all **Mafia Killing \🗡️** are dead, you have the highest priority to become a **Mafioso <:maficon:891739940055052328>**. You have access to the __Mafia Night Meeting__ <:mafia:1007768566789050378>\n<:framed:890365634913902602> **Frame - **__Frame__ target player. They will also receive __Framed__ results from using __Investigative__ abilities tonight. `/frames` for more information.", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a skilled counterfeiter who fabricates information. They must be the **Framer <:framed:890365634913902602>**", inline=False)
        self.abilities = [classes.ability.Ability(frame, utils.notMeAndNotDead, -1, "Interrogate", " __Investigate__ target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", "📝", "interrogate")]




