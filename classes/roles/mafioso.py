
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

class Mafioso(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target is the cold blooded hitman of the mafia.")
        self.type = "killing"
        self.color = 0xd0021b
        self.order = 8
        self.emoji = "<:maficon:891739940055052328>"
        self.roleEmbed = disnake.Embed(title="**Your role is Mafioso**", colour=disnake.Colour(0xd0021b), description="The right hand man of organized crime").set_thumbnail(url="https://images-ext-2.discordapp.net/external/ULR_Om4Caic9Xd1TXs5EtLv7AtkYTZ2XO1BL0FJsjEY/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/765738640554065962/897585492562964531/MafIcon2.png?width=467&height=467").set_footer(text="Mafia Killing 🗡️").add_field(name="**Atk ⚔️:**", value="__Basic__", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Type 🔅:**", value="**Unique Killer \🗡️**", inline=False).add_field(name="**Abilities \🗡️:**", value="**<:passive:936343832696606800> Apprentice | Passive\n<:moon:934556372421451776> Assassinate | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:maf:891739940055052328> Apprentice -**You have access to the __Mafia Night Meeting__ <:mafia:1007768566789050378>\n**<:maf:891739940055052328> Assassinate -** __Attack__ target player", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is the cold blooded hitman of the mafia. They must be the **Mafioso <:maf:891739940055052328>**", inline=False)
        self.abilities = [classes.ability.Ability(kill, utils.notMafiaAndNotDead, -1, "Assassinate", "Attack target player. They'll probably die.", "<:maficon:891739940055052328>", "kill", utils.headstart)]




