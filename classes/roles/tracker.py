
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction

def init():
    Tracker("Tracker", Faction.Town)
    
async def track(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]

        if (len(targetPlayer.nightTargettedPlayers) == 0):
            embed = disnake.Embed(title=f"Your target did not visit anyone last night.", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=targetPlayer.memberObj.display_avatar.url).set_footer(text="Interesting", icon_url=originPlayer.memberObj.display_avatar.url)
            await originPlayer.memberObj.send(embed=embed)
            return

        visitedPlayer = classes.player.Player.get(targetPlayer.nightTargettedPlayers[0].memberObj.id, game)

        embed = disnake.Embed(title=f"Your target visited {visitedPlayer.memberObj.name} last night!", colour=disnake.Colour(0x7ed321)).set_thumbnail(url=visitedPlayer.memberObj.display_avatar.url).set_footer(text="What were they doing?", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)

class Tracker(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = False
        self.color = 0x7ed321
        self.type = "investigative"
        self.order = 100
        self.emoji = "<:trackicon:922885543812005949>"
        self.roleEmbed = disnake.Embed(title="**Your role is Tracker**", colour=disnake.Colour(0x7ed321), description="A skilled pathfinder who scouts the night").set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/937355480467132446/TrackerIcon_2.png?ex=65bfa0d1&is=65ad2bd1&hm=685a13d132a599ba5303fb380b24ea4bb037690d9c2abae10134dca8eb2bed0c&=&format=webp&quality=lossless&width=420&height=420").set_footer(text="Town Investigative 🔎").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:town:1007768656341651547>**", inline=False).add_field(name="**Type 🔅:**", value="**Information \🔎**", inline=False).add_field(name="**Abilities \🔎:**", value="**<:moon:934556372421451776> Track | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:copicon2:889672912905322516> Track -** __Investigate__ target player. Follow target player to learn who they visit", inline=False).add_field(name="**Win Condition 🏆:**", value="Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target watches who others visit. They must be a **Tracker <:trackicon:922885543812005949>**", inline=False)
        self.abilities = [classes.ability.Ability(track, utils.notMeAndNotDead, -1, "Track", " Track target player. Follow target player to know who they visit", "🔦", "track")]




