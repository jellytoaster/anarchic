
import utils
import classes.role as role
import disnake
import random
import classes.ability
import classes.player
import classes.enums

def twoPoints(me, game):
    return me.externalRoleData["points"] == 2

def headHunterN1Targetting(me, allPlayers, game):
    return [player for player in allPlayers if player.assignedRole.faction == classes.enums.Faction.Town and player.assignedRole.name != "mayor"]

async def firstTarget(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.externalRoleData["points"] = 0

    if targetPlayers == []:
        originPlayer.externalRoleData["target"] = None
        targetembed = disnake.Embed(title=f"**Well that sucks...**", colour=disnake.Colour(0x39556b), description=f"Looks nobody was an englible candidate for you! You may choose a target the following night.")

        targetembed.set_thumbnail(url=targetPlayer.memberObj.display_avatar.url)
        targetembed.set_footer(text="...", icon_url=targetPlayer.memberObj.display_avatar.url)
        await originPlayer.memberObj.send(embed=targetembed)
        return
    
    originPlayer.externalRoleData["target"] = random.choice(targetPlayers)


    targetPlayer = originPlayer.externalRoleData["target"]

    targetembed = disnake.Embed(title=f"**Your target is {targetPlayer.memberObj.name}.**", colour=disnake.Colour(0x39556b), description=f"Your target has wronged you and now it's time for them to pay. Get them lynched in order to win.")

    targetembed.set_thumbnail(url=targetPlayer.memberObj.display_avatar.url)
    targetembed.set_footer(text="If your target dies at night, you can choose another one at night.", icon_url=targetPlayer.memberObj.display_avatar.url)
    await originPlayer.memberObj.send(embed=targetembed)
async def vengance(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.externalRoleData["target"] = targetPlayers[0]

async def rest(targetPlayers:list, originPlayer:classes.player.Player, game):
    originPlayer.kill(classes.enums.DeathReason.Headhunter, game, True)
class Headhunter(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = False
        self.color = 0x334f64
        self.type = "evil"
        self.order = 10
        self.emoji = "<:hhicon2:891429754643808276>"
        self.roleEmbed = disnake.Embed(title="**Your role is Headhunter**", colour=disnake.Colour(0x334f64), description="A vengeance-seeking outsider who holds a grudge against the town").set_thumbnail(url="https://cdn.discordapp.com/emojis/891429754643808276.webp?size=96&quality=lossless").set_footer(text="Neutral Evil 🪓").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="__Barrier__", inline=True).add_field(name="**Faction 📌:**", value="**Neutral <:hhicon2:891429754643808276>**", inline=False).add_field(name="**Type 🔅:**", value="**Unique Social \🪓**", inline=False).add_field(name="**Abilities \🪓:**", value="**<:passive:936343832696606800> - Vengeful\n<:moon:934556372421451776> Vengeance | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:hhicon2:891429754643808276>  Vengeful -** A random **Town <:town:1007768656341651547>** starts the game as your __Target__. The **Mayor <:mayoricon:922566007946629131>** cannot be your __Target__ this way.\n**<:hhicon2:891429754643808276>  Vengeance -** __Astrally__ mark target player. They are now your new __Target__.", inline=False).add_field(name="**Win Condition 🏆:**", value="Survive to see **two** targets **lynched <:hhicon2:891429754643808276>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copp:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target sentences the condemned to their fate. They must be the **Headhunter <:hhicon2:891429754643808276>**", inline=False)
        self.abilities = [classes.ability.Ability(firstTarget, headHunterN1Targetting, -1, "Vengeful", "A random Town :town~2: starts the game as your Target. The Mayor :mayoricon: cannot be your Target this way.", "<:hhicon2:891429754643808276>", "target", utils.notDead, classes.enums.AbilityType.DayOne), classes.ability.Ability(vengance, utils.notMeAndNotDead, -1, "Vengance", "__Astrally__ mark target player. They are now your new __Target__.", "<:hhicon2:891429754643808276>", "target", utils.notDead), classes.ability.Ability(rest, utils.literallyAnyone, 1, "rest", "you win!", "🤓", "h", twoPoints, classes.enums.AbilityType.PassiveEarly)]




