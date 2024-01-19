
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums

class Villager(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):

        super().__init__(name, faction)
        self.suspiciousRole = False
        self.color = 0x7ed321
        self.type = "vanilla"
        self.order = 0
        self.emoji = "<:townicon2:896431548717473812>"
        self.roleEmbed = disnake.Embed(title="**Your role is Villager**", colour=disnake.Colour(0x7ed321), description="You are a humble citizen who's fallen into a state of uneasy distrust").set_thumbnail(url="https://cdn.discordapp.com/emojis/1007714759409414274.webp?size=44&quality=lossless").set_footer(text="Town Vanilla 🏠").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Town <:town:1007768656341651547>**", inline=False).add_field(name="**Type 🔅:**", value="**Social \💬**", inline=False).add_field(name="**Abilities \💬:**", value="**None**", inline=False).add_field(name="**Attributes 🌟**", value="**None**", inline=False).add_field(name="**Win Condition 🏆:**", value="Eliminate all criminals who may try to harm the **Town <:town:1007768656341651547>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target seems **Innocent <:inno:873636640227205160>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a dedicated to the justice of all evildoers. They must be a **Villager <:villyicon:1007714759409414274>**", inline=False)
        self.abilities = []




