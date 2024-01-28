
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

class Consigliere(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is the ingenious advisor to the Mafia.")
        self.color = 0xd0021b
        self.type = "support"
        self.promotionOrder = 2
        self.order = -5
        self.emoji = "<:consigicon2:896154845130666084>"
        self.roleEmbed = disnake.Embed(title="**Your role is Consigliere**", colour=disnake.Colour(0xd0021b), description="A resourceful investigator who gathers intelligence for the mafia").set_thumbnail(url="https://cdn.discordapp.com/emojis/896154845130666084.webp?size=96&quality=lossless").set_footer(text="Mafia Support 🥀").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Type 🔅:**", value="**Unique Information \🔎**", inline=False).add_field(name="**Abilities \🔎:**", value="**<:passive:936343832696606800> Legacy | Passive\n<:moon:934556372421451776> Examine | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:consigicon2:896154845130666084> Legacy -** If all **Mafia Killing \🗡️** are dead, you have a priority of __2__ to become a **Mafioso <:maf:891739940055052328>**. You have access to the __Mafia Night Meeting__ <:mafia:1007768566789050378>.\n<:consigicon2:896154845130666084> **Examine - **__Investigate__ target player. You wil learn their true role.", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is the ingenious advisor to the Mafia. They must be the **Consigliere <:consigicon2:896154845130666084>**", inline=False)
        self.abilities = [classes.ability.Ability(examine, utils.notMeAndNotDead, -1, "Examine", " Examine target player. You will learn if they are __Innocent__ <:inno:873636640227205160>, __sided__ with the **Mafia <:mafia:1007768566789050378>**, or __Psychotic__ <:psycho:877584821180825691>.", "📝", "examine")]




