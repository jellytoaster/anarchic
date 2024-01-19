
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums

async def protect(targetPlayers:list, originPlayer:classes.player.Player, game):
        targetPlayer:classes.player.Player = targetPlayers[0]
        targetPlayer.defended = originPlayer

class Doctor(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):

        super().__init__(name, faction)
        self.suspiciousRole = False
        self.color = 0x7ed321
        self.type = "protective"
        self.order = 10
        self.emoji = "<:docicon2:890333203959787580>"
        self.roleEmbed =  disnake.Embed(title="**Your role is Doctor**", colour=disnake.Colour(0x7ed321), description="A secret surgeon who heals people at night").set_thumbnail(url="https://cdn.discordapp.com/emojis/890333203959787580.webp?size=96&quality=lossless").set_footer(text="Town Protective 💉").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:town:1007768656341651547>**", inline=False).add_field(name="**Type 🔅:**", value="**Guardian \💗**", inline=False).add_field(name="**Abilities \💗:**", value="**<:moon:934556372421451776> Heal | Unlimited charges**", inline=False).add_field(name="**Attributes 🌟**", value="**<:docicon2:890333203959787580> Heal -** __Heal__ target player. You will grant your target a __Powerful Resistance__ for the night. Both you and your target will be notified if your target is __attacked__.", inline=False).add_field(name="**Win Condition 🏆:**", value="Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a profound surgeon. They must be a **Doctor <:docicon2:890333203959787580>**", inline=False)
        self.abilities = [classes.ability.Ability(protect, utils.notMeAndNotDead, -1, "Heal", "__Heal__ target player. You will grant your target a __Powerful Resistance__ for the night. Both you and your target will be notified if your target is __attacked__.", "💖", "heal")]




