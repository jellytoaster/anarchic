
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums


async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    targetPlayer.kill(classes.enums.DeathReason.Enforcer)
    if (targetPlayer.assignedRole.faction == classes.enums.Faction.Town):
        embed = disnake.Embed(title="**You could not get over the guilt of killing a Town <:town:1007768656341651547>**", colour=disnake.Colour(0x7ed321), description="You have lost all charges of __Eliminate__ <:vgicon:890339050865696798>")

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/890339050865696798.webp?size=96&quality=lossless")
        embed.set_footer(text="You can still help your faction", icon_url=originPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=embed)
        originPlayer.assignedRole.abilities[0].charges = 0

def isUsable(game):
    if (game.dayNum == 1):
        return False
    return True

class Vigilante(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = True
        self.color = 0xd0021b
        self.order = 8
        self.type = "killing"
        self.targetingOptions = utils.notMeAndNotDead
        self.emoji = "<:vgicon:890339050865696798>"
        self.roleEmbed = disnake.Embed(title="**Your role is Vigilante**", colour=disnake.Colour(0x7ed321), description="A rogue enforcer with an eye for justice").set_thumbnail(url="https://cdn.discordapp.com/emojis/890339050865696798.webp?size=96&quality=lossless").set_footer(text="Town Killing 🔫").add_field(name="**Atk ⚔️:**", value="__Basic__", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:town:1007768656341651547>**", inline=False).add_field(name="**Type 🔅:**", value="**Killer \🔫**", inline=False).add_field(name="**Abilities \🔫:**", value="**<:moon:934556372421451776> Eliminate | 3 charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:vgicon:890339050865696798>  Eliminate -** __Attack__ target player. If you kill a **Town <:town:1007768656341651547>**, lose all charges of __Eliminate__ <:vgicon:890339050865696798>. Cannot be used **Night 1 <:moon:934556372421451776>**.", inline=False).add_field(name="**Win Condition 🏆:**", value="Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is willing to bend the law to enact justice. They must be a **Vigilante <:vgicon:890339050865696798>**", inline=False)
        self.abilities = [classes.ability.Ability(kill, 3, "Shoot", "__Attack__ target player. If you kill a **Town <:town:1007768656341651547>**, lose all charges of __Eliminate__ <:vgicon:890339050865696798>. Cannot be used **Night 1 <:moon:934556372421451776>**.", "<:vgicon:890339050865696798>", "shoot", isUsable)]




