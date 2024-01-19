
import utils
import classes.role as role
import disnake
import classes.ability
import classes.player
import classes.enums

class Associate(role.Role):
    def __init__(self, name: str, faction: classes.enums.Faction):
        super().__init__(name, faction)
        self.suspiciousRole = True
        self.color = 0xd0021b
        self.promotionOrder = 10
        self.order = 0
        self.type = "vanilla"
        self.emoji = "<:mafia:1007768566789050378>"
        self.roleEmbed = disnake.Embed(title="**Your role is Associate**", colour=disnake.Colour(0xd0021b), description="An agent of organized crime, working for the Mafia").set_thumbnail(url="https://cdn.discordapp.com/emojis/1006333104920735787.webp?size=96&quality=lossless").set_footer(text="Mafia Vanilla 🌷").add_field(name="**Atk ⚔️:**", value="None", inline=True).add_field(name="**Res 🛡️:**", value="None", inline=True).add_field(name="**Faction 📌:**", value="**Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Type 🔅:**", value="**Social \💬**", inline=False).add_field(name="**Abilities \💬:**", value="**<:passive:936343832696606800> Legacy | Passive**", inline=False).add_field(name="**Attributes 🌟**", value="**<:assoicon:1006333104920735787> Legacy -** If all **Mafia Killing \🗡️** are dead, you have the lowest priority to become a **Mafioso <:maf:891739940055052328>**. You have access to the __Mafia Night Meeting__ <:mafia:1007768566789050378>.", inline=False).add_field(name="**Win Condition 🏆:**", value="Kill all those who may rival the **Mafia <:mafia:1007768566789050378>**", inline=False).add_field(name="**Investigation Results \🔎:**", value="**Cop <:copicon2:889672912905322516>:** Your target is sided with the **Mafia <:mafia:1007768566789050378>**\n**Consigliere <:consigicon2:896154845130666084>:** Your target is a loyal goon affiliated with the Mafia. They must be an  **Associate <:assoicon:1006333104920735787>**", inline=False)
        self.abilities = []




