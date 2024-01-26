
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction
from  classes.investigationResults import investigationResults

def init():
    Recon("Recon", Faction.Mafia)

async def check(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    visitedPlayers = targetPlayer.whoVisitedMe()
    visitedPlayers.remove(originPlayer)

    if (len(visitedPlayers)) == 0:
        await originPlayer.memberObj.send(embed=disnake.Embed(title=f"Nobody visited your target last night.", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=originPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url))
    else:
        if len(visitedPlayers) > 1:
            title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
        else:
            title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

        embed = disnake.Embed(title=f"Your target was visited by {title} last night!", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
    
    if (len(targetPlayer.nightTargettedPlayers) == 0):
        embed = disnake.Embed(title=f"Your target did not visit anyone last night.", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=targetPlayer.memberObj.display_avatar.url).set_footer(text="Interesting.", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
        return

    visitedPlayers = targetPlayer.nightTargettedPlayers

    if len(visitedPlayers) > 1:
        title = ", ".join(visitedPlayers[:-1].memberObj.name) + " and " + visitedPlayers[-1].memberObj.name
    else:
        title = visitedPlayers[0].memberObj.name if visitedPlayers else ""

    embed = disnake.Embed(title=f"Your target visited {title} last night!", colour=disnake.Colour(0xd0021b)).set_thumbnail(url=visitedPlayers[0].memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
    await originPlayer.memberObj.send(embed=embed)

class Recon(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.investigationResults = investigationResults(True, "Your target lurks in shadows.")
        self.color = 0xd0021b
        self.type = "support"
        self.promotionOrder = -1
        self.order = 0
        self.emoji = "<:loicon2:889673190392078356>"
        self.roleEmbed = disnake.Embed(title="**Your role is Recon**", colour=disnake.Colour(0xd0021b), description="You are a counterintelligence agent, specialized in the gathering reconnaissance.").set_thumbnail(url="https://cdn.discordapp.com/emojis/889673190392078356.webp?size=44&quality=lossless").set_footer(text="Mafia Support 🥀").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:townicon2:896431548717473812>**", inline=False).add_field(name="**Type 🔅:**", value="**Information \🔎**", inline=False).add_field(name="**Abilities \🔎:**", value="**<:moon:934556372421451776> Stakeout | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:loicon2:889673190392078356> Overlook -** You will learn who your target visits, and who visits your target.", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target lurks in shadows. They must be a **Recon <:loicon2:889673190392078356>**", inline=False)
        self.abilities = [classes.ability.Ability(check, utils.notMafiaAndNotDead, -1, "Overlook", "__Overlook__ target player. You will learn who visits your target.", "🔦", "watch")]




