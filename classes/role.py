from classes.enums import Faction
from classes.contraction import Contraction
import string
import disnake
import utils

class Role:
    allRoles:list = []
    def __init__(self, name:str, faction:Faction):
        self.name = name
        self.emoji = ""
        self.color = 0x000000
        self.faction = faction
        self.type = ""
        self.investigationResults = None
        self.promotionOrder = 0
        self.abilities:list = []
        self.order = 0 # 0 is first, higher numbers have their role action processed later
        self.constants = {"winCon": "Just win!", "shortDescription": "A role."}
        
        Role.allRoles.append(self)
        return self

    def toRole(name:str):
        for i in Role.allRoles:
            if (i.name.lower() == name.lower()):
                return i
            
        return None
    
    def buildEmbed(self):
        embed = disnake.Embed(title=f"Your role is {self.name}", description=self.constants["shortDescription"], color=self.color)
        
        emojis = {"passive": "<:passive:936343832696606800>", "night": "<:moon:934556372421451776>"}
        factionalEmojis = {"mafia" : "<:mafia:1007768566789050378>", "town":"<:town:1007768656341651547>", "neutral" : "<:hhicon2:891429754643808276>"}
        abilities = ""
        for i in self.abilities:
            if i.visible:
                charge = f'{"- " + utils.chargeCountSimple(i.charges) if i.type.value != "passive" else ""}'
                abilities += f"{emojis[i.type.value]} **{i.name} ({string.capwords(i.type.value)}) {charge}**\n{i.description}\n\n"

        if (abilities != ""):
            embed.add_field("__Abilities__ 🌟", abilities, inline=False)
        embed.add_field("__Win Condition__ 🏆", f"*{self.constants['winCon']}*", inline=False)

        embed.set_footer(text=f"{string.capwords(self.faction.value)} {string.capwords(self.type)}", icon_url=f"https://cdn.discordapp.com/emojis/{factionalEmojis[self.faction.value.lower()].split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        embed.set_thumbnail(f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        return embed
    
    def buildEmbedSimple(self):
        embed = disnake.Embed(title="The " + self.name, description=self.constants["shortDescription"], color=self.color)
        
        emojis = {"passive": "<:passive:936343832696606800>", "night": "<:moon:934556372421451776>"}
        factionalEmojis = {"mafia" : "<:mafia:1007768566789050378>", "town":"<:town:1007768656341651547>", "neutral" : "<:hhicon2:891429754643808276>"}
        abilities = ""
        for i in self.abilities:
            if i.visible:
                charge = f'{"- " + utils.chargeCountSimple(i.charges) if i.type.value != "passive" else ""}'
                abilities += f"{emojis[i.type.value]} **{i.name} ({string.capwords(i.type.value)}) {charge}**\n{i.description}\n\n"

        if (abilities != ""):
            embed.add_field("__Abilities__ 🌟", abilities, inline=False)
        embed.add_field("__Win Condition__ 🏆", f"*{self.constants['winCon']}*", inline=False)

        embed.set_footer(text=f"{string.capwords(self.faction.value)} {string.capwords(self.type)}", icon_url=f"https://cdn.discordapp.com/emojis/{factionalEmojis[self.faction.value.lower()].split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        embed.set_thumbnail(f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        return embed