
import utils 
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums


async def kill(targetPlayers:list, originPlayer:classes.player.Player, game):
    targetPlayer:classes.player.Player = targetPlayers[0]
    await targetPlayer.kill(classes.enums.DeathReason.Jester, game, force=True)

async def voteBlock(targetPlayers:list, originPlayer:classes.player.Player, game):
    for i in targetPlayers:
        i.isVoteBlocked = True

class Jester(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = False
        self.type = "evil"
        self.color = 0xf1cbe2
        self.order = 1
        self.emoji = "<:jesticon2:889968373612560394>"
        self.roleEmbed = disnake.Embed(title="**Your role is Jester**", colour=disnake.Colour(0xf1cbe2), description="A crazed lutanic who wants to be publicly executed").set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/872147798336893019/imageedit_4_4906520050.png?ex=65b91dee&is=65a6a8ee&hm=ff3ca23cc42d80bac2df2273fc4a4974332614225c474ed0b25c5cd42e2548d6&=&format=webp&quality=lossless&width=310&height=302").set_footer(text="Neutral Evil 🪓").add_field(name="**Atk ⚔️:**", value="__Strong__", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Neutral <:hhicon2:891429754643808276>**", inline=False).add_field(name="**Type 🔅:**", value="**Social 💬**", inline=False).add_field(name="**Abilities \🗡️:**", value="**<:passive:936343832696606800> Spiteful | Passive**", inline=False).add_field(name="**Attributes 🌟**", value="**<:jesticon2:889968373612560394> Spiteful** - Upon getting lynched, all players who didn't pardon will be **occupied* the following night, and be voteblocked the following day. You will astrally attack one of these players.", inline=False).add_field(name="**Win Condition 🏆:**", value="Get yourself **Lynched** <:jesticon2:889968373612560394>", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a crazed lutanic waiting to be hung. They must be a **Jester <:jesticon2:889968373612560394>**", inline=False)
        self.abilities = [classes.ability.Ability(kill, utils.playersWhoVotedGuilty, 1, "Haunt", "Haunt a player so they die.", "<:jesticon2:889968373612560394>", "haunt", utils.jesterDeathCheck),classes.ability.Ability(voteBlock, utils.playersWhoVotedGuilty, -1, "jester voteblock", "voteblock guiltiers", "💀", "voteblock", utils.jesterDeathCheck, classes.enums.AbilityType.Passive)]