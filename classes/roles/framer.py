
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
        self.investigationResults = investigationResults(True, "Your target is the law enforcer of the town.")
        self.color = 0xd0021b
        self.type = "deception"
        self.order = 1000
        self.emoji = "<:frameicon2:890365634913902602>"
        self.roleEmbed = disnake.Embed(title="**Your role is Cop**", colour=disnake.Colour(0x7ed321), description="A reliable law enforcer, skilled at keeping evildoers in check").set_thumbnail(url="https://images-ext-1.discordapp.net/external/6F0TiBYTjsCJCwFVmFo3CtXHTZ-gDly0cUEaka7m_Rg/%3Fsize%3D80/https/cdn.discordapp.com/emojis/889672912905322516.png").set_footer(text="Town Investigative 🔎").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:town:1007768656341651547>**", inline=False).add_field(name="**Type 🔅:**", value="**Information \🔎**", inline=False).add_field(name="**Abilities \🔎:**", value="**<:moon:934556372421451776> Interrogate | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:copicon2:889672912905322516> Interrogate -** __Investigate__ target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", inline=False).add_field(name="**Win Condition 🏆:**", value="Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is the law enforcer of the town. They must be a **Cop <:copicon2:889672912905322516>**", inline=False)
        self.abilities = [classes.ability.Ability(frame, utils.notMeAndNotDead, -1, "Interrogate", " __Investigate__ target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", "📝", "interrogate")]




