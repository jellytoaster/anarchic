
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums
from classes.enums import Faction

def init():
    Jester("Jester", Faction.Neutral)

async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    await targetPlayer.kill(classes.enums.DeathReason.Jester, game, force=True)

async def roleBlock(targetPlayers:list, originPlayer:classes.player.Player, game):
    for i in targetPlayers:
        i.isRoleBlocked = True

class Jester(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = False
        self.type = "evil"
        self.color = 0xf1cbe2
        self.order = 1
        self.emoji = "<:jesticon2:889968373612560394>"
        self.roleEmbed = disnake.Embed(title="**Your role is Jester**", colour=disnake.Colour(0xf1cbe2), description="A crazed lunatic who wants to be publicly executed").set_thumbnail(url="https://cdn.discordapp.com/emojis/889968373612560394.webp?size=128").set_footer(text="Neutral Evil 🪓").add_field(name="**Atk ⚔️:**", value="__Strong__", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Neutral <:hhicon2:891429754643808276>**", inline=False).add_field(name="**Type 🔅:**", value="**Social 💬**", inline=False).add_field(name="**Abilities \🗡️:**", value="**<:passive:936343832696606800> Spiteful | Passive**", inline=False).add_field(name="**Attributes 🌟**", value="**<:jesticon2:889968373612560394> Spiteful** - Upon getting lynched, all players who didn't pardon will be **occupied** the following night. You will astrally attack one of these players.", inline=False).add_field(name="**Win Condition 🏆:**", value="Get yourself **Lynched** <:jesticon2:889968373612560394>", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a crazed lunatic waiting to be hung. They must be a **Jester <:jesticon2:889968373612560394>**", inline=False)
        self.abilities = [classes.ability.Ability(kill, utils.playersWhoVotedGuilty, 1, "Haunt", "Haunt a player so they die.", "<:jesticon2:889968373612560394>", "haunt", utils.jesterDeathCheck, classes.enums.AbilityType.Night),classes.ability.Ability(roleBlock, utils.playersWhoVotedGuilty, -1, "jester roleblock", "roleblock guiltiers", "💀", "roleblock", utils.jesterDeathCheck, classes.enums.AbilityType.PassiveEarly)]