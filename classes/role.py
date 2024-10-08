from classes.enums import Faction
from classes.investigationResults import investigationResults
from classes.contraction import Contraction
import string
import disnake
import utils

class Role:
    allRoles:list = []
    def __init__(self):
        self.name:str = self.__class__.__name__.replace("_", " ")
        self.emoji:str = ""
        self.color:int = 0x000000
        self.faction:Faction = Faction.Town
        self.type:str = ""
        """Used for adding roles to role groups. This must be one of the \"types\" in `contraction.py`."""

        self.investigationResults:investigationResults = investigationResults(False, "you should not see this")

        self.promotionOrder:int = 0
        """Only applies for Mafia roles. The smaller the number, the higher priority they will be promoted to a Mafioso. If the order is the same, it will go through the player list (join order)"""
        self.alwaysUseAbilitySelection:bool = False
        """If set to `True`, the ability selection embed will appear even if the player only has one ability to choose."""
        self.cannotAppearInRoleGroup:bool = False
        """Determines if the role is allowed to appear in role groups like Random Town, Mafia Killing, etc. This is used on Villager and Associate."""

        self.abilities:list = []
        self.order = 0 # 0 is first, higher numbers have their role action processed later
        """The order as their ability runs. The smaller the number, the earlier their abilities run."""
        self.constants:dict = {"winCon": "Just win!", "shortDescription": "A role."}
    
        return self

    def toRole(name:str):
        for i in Role.allRoles:
            if (i.name.lower() == name.lower()):
                return i
            
        if "mafia" in name.lower(): # TEMPOARY HOTFIX PLEASE CHANGE THIS
            return Role.toRole("associate")
            
        return None
    
    def buildEmbed(self):
        embed = disnake.Embed(title=f"Your role is {self.name}", description=self.constants["shortDescription"], color=self.color)
        
        emojis = {"passive": "<:passive:936343832696606800>","passived1": "<:passive:936343832696606800>","passivedusk": "<:passive:936343832696606800>","passivedawn": "<:passive:936343832696606800>","passiveearly": "<:passive:936343832696606800>",2:":sun",3:":sunset: i hope this is a real emoji", "night": "<:moon:934556372421451776>"}
        factionalEmojis = {"mafia" : "<:mafia:1007768566789050378>", "town":"<:town:1007768656341651547>", "neutral" : "<:hhicon2:891429754643808276>"}
        abilities = ""
        for i in self.abilities:
            if i.visible:
                charge = f'{"- " + utils.chargeCountSimpleSimple(i.charges) if i.type.value != "passive" else ""}'
                abilities += f"{emojis[i.type.value]} **{i.name} ({string.capwords(i.type.value)}) {charge}**\n{i.description}\n\n"

        if (abilities != ""):
            embed.add_field("__Abilities__ 🌟", abilities, inline=False)
        embed.add_field("__Win Condition__ 🏆", f"*{self.constants['winCon']}*", inline=False)

        embed.set_footer(text=f"{string.capwords(self.faction.value)} {string.capwords(self.type)}", icon_url=f"https://cdn.discordapp.com/emojis/{factionalEmojis[self.faction.value.lower()].split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        embed.set_thumbnail(f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        return embed
    
    def buildEmbedSimple(self):
        embed = disnake.Embed(title="The " + self.name, description=self.constants["shortDescription"], color=self.color)
        
        emojis = {"passive": "<:passive:936343832696606800>","passived1": "<:passive:936343832696606800>","passivedusk": "<:passive:936343832696606800>","passivedawn": "<:passive:936343832696606800>","passiveearly": "<:passive:936343832696606800>",2:":sun",3:":sunset: i hope this is a real emoji", "night": "<:moon:934556372421451776>"}
        factionalEmojis = {"mafia" : "<:mafia:1007768566789050378>", "town":"<:town:1007768656341651547>", "neutral" : "<:hhicon2:891429754643808276>"}
        abilities = ""
        for i in self.abilities:
            if i.visible:
                charge = f'{"- " + utils.chargeCountSimpleSimple(i.charges) if i.type.value != "passive" else ""}'
                abilities += f"{emojis[i.type.value]} **{i.name} ({string.capwords(i.type.value)}) {charge}**\n{i.description}\n\n"

        if (abilities != ""):
            embed.add_field("__Abilities__ 🌟", abilities, inline=False)
        embed.add_field("__Win Condition__ 🏆", f"*{self.constants['winCon']}*", inline=False)

        embed.set_footer(text=f"{string.capwords(self.faction.value)} {string.capwords(self.type)}", icon_url=f"https://cdn.discordapp.com/emojis/{factionalEmojis[self.faction.value.lower()].split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        embed.set_thumbnail(f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        return embed
    
    def buildInvestigationResults(self):
        factionalEmojis = {"mafia" : "<:mafia:1007768566789050378>", "town":"<:town:1007768656341651547>", "neutral" : "<:hhicon2:891429754643808276>"}
        embed = disnake.Embed(title=F"The {self.name} - Investgiation Results", colour=disnake.Color(self.color))

        embed.set_thumbnail(url=self.getIconUrl())

        embed.add_field(name="<:copicon2:889672912905322516> **Cop**", value="Your target seems <:inno:873636640227205160> **Innocent**." if not self.investigationResults.copSuspicious else "Your target is sided with the <:mafia:1007768566789050378> **Mafia**!", inline=False)
        embed.add_field(name="<:consigicon2:896154845130666084>**Consigliere**", value=f"{self.investigationResults.consigliereFlavorText} They must be a {self.emoji} **{self.name}**.", inline=False)

        embed.set_footer(text=f"{string.capwords(self.faction.value)} {string.capwords(self.type)}", icon_url=f"https://cdn.discordapp.com/emojis/{factionalEmojis[self.faction.value.lower()].split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64")

        return embed
    
    def getIconUrl(self):
        return f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64"