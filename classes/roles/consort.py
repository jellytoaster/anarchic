
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Consort("Consort", Faction.Mafia)

def roleblockplayer(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayers[0].isRoleBlocked = True

class Consort(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is a seductive dancer.")
        self.color = 0xd0021b
        self.promotionOrder = 3
        self.type = "support"
        self.order = 0
        self.emoji = "<:consicon2:890336628269281350>"
        self.roleEmbed = disnake.Embed(title="**Your role is Consort**", colour=disnake.Colour(0xd0021b), description="A captivating performer working for the mob").set_thumbnail(url="https://cdn.discordapp.com/emojis/890336628269281350.webp?size=96&quality=lossless").set_footer(text="Mafia Support 🥀").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Type 🔅:**", value="**Unique Manipulative \🎵**", inline=False).add_field(name="**Abilities \🎵:**", value="**<:passive:936343832696606800> Legacy | Passive\n<:passive:936343832696606800> Own Tricks | Passive\n<:moon:934556372421451776> Captivate | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:consicon2:890336628269281350> Legacy -** If all **Mafia Killing \🗡️** are dead, you have a priority of __3__ to become a **Mafioso <:maf:891739940055052328>**. You have access to the __Mafia Night Meeting__ <:mafia:1007768566789050378>.\n**<:consicon2:890336628269281350> Own Tricks -** You are immune to __Distractions__.\n<:consicon2:890336628269281350> **Captivate - **__Distract__ target player.", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a seductive dancer. They must be the **Consort <:consicon2:890336628269281350>**", inline=False)
        self.abilities = [classes.ability.Ability(roleblockplayer, utils.notMafiaAndNotDead, -1, "Capivate", "__Distract__ target player.", self.emoji, "distract")]




