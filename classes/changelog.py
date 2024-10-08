import disnake

class Changelog():
    changelogs = {}
    def __init__(self, version, emoji, title, description, color, highlights:list, adds:list, changes:list, fixes:list, balance:list=[], usable=True) -> None:
        self.emoji = emoji
        self.ver = version
        self.title = title
        self.description = description
        self.color = color

        self.highlights = highlights
        self.adds = adds
        self.changes = changes
        self.fixes = fixes
        self.balance = balance
        
        self.usable = usable

        Changelog.changelogs[version] = self

    def noPatch(self):
        return '.'.join(self.ver.split('.')[0:2])

    def makeEmbed(self) -> disnake.Embed:
        embed = disnake.Embed(
            title=f"Anarchic {self.ver} - {self.title}",
            description=self.description,
            color=disnake.Color(self.color)
        )
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1009910329322512464.webp?size=128&quality=lossless")

        def format(icon, items):
            return f"{icon} " + f"\n{icon} ".join(items) if items else ":x: **None**"

        if (self.highlights != []):
            embed.add_field(name="💫 Highlights", value=format('<:highlight:1199861697989586965>', self.highlights), inline=False)
        if (self.adds != []):
            embed.add_field(name="🎯 New Features", value=format('<:add:1034558781847261194>', self.adds), inline=False)
        if (self.changes != []):
            embed.add_field(name="🛠️ Game Changes", value=format('<:change:1034559083627429918>', self.changes), inline=False)
        if (self.fixes != []):
            embed.add_field(name="🐞 Bug Fixes", value=format('<:remove:1198401946567049327>', self.fixes), inline=False)
        if (self.balance != []):
            embed.add_field(name="🛝 Balance Changes", value=format('<:remove:1198401946567049327>', self.balance), inline=False)

        return embed
    
    def makeJustHighlights(self) -> disnake.Embed:
        embed = disnake.Embed(
            title=f"Anarchic {self.noPatch()} coming soon!",
            description=f"*See what's coming in Anarchic {self.noPatch()}, the {self.title}!*",
            color=disnake.Color(self.color)
        )
        
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1009910329322512464.webp?size=128&quality=lossless")

        def format(icon, items):
            return f"{icon} " + f"\n{icon} ".join(items) if items else ":x: **None**"

        if (self.highlights != []):
            embed.add_field(name="Highlights", value=format('<:highlight:1199861697989586965>', self.highlights), inline=False)

        return embed

    def initChangelogs():
        Changelog("1.0.0", "<:anarchist:1147669124042981378>", "Initial Release", "Welcome to Anarchic!", 0x7ed321, [],["Added 7 roles: Cop, Mafioso, Doctor, Consort, Vigilante, Villager, and Associate", "Added general gameplay mechanics"], [], [])

        Changelog("1.1.0", "<:hhicon2:891429754643808276>", "Neutrals Update", "Two new roles arrive, but they don't seem to be siding with anyone... I wonder what they want?", 0x8c8c8c, 
        ["Beware of the <:jesticon2:889968373612560394> **Jester**! This lunatic may seem harmless, but they can haunt and roleblock you if you <:lynch:1010226047456915547> **lynch** them.","Somebody has wronged you... and you must get revenge! This is the <:hhicon2:891429754643808276> **Headhunter**, who must **lynch** two of their targets before they can rest in peace."],
        ["Added Jester", "Added Headhunter", "Added `/help`", "Added `/changelog`", "Added setup import/export with `/setup import` and `/setup export`"], ["Fate-deciding results now say none if nobody votes", "Empty setups now say \"Empty\" for setup names"], ["Fixed issues with party commands with default avatars", "/host now works properly", "Fixed issues with /setup while there is no party"])

        Changelog("1.2.0", "<:loicon2:889673190392078356>", "Investigative Update", "Unleash a package of 5 new investigative roles!", 0xb8e986, 
        ["Who needs the <:copicon2:889672912905322516> **Cop** when you have the <:loicon2:889673190392078356> **Lookout** and <:trackicon:922885543812005949> **Tracker**? These two investigative roles will keep the <:mafia:1007768566789050378> **Mafia** on their toes.","On the other hand, there is the <:frameicon2:890365634913902602> **Framer**, creating counterfeit information with the <:consigicon2:896154845130666084> **Consigliere** and <:recon:1200834864845438977> **Recon** giving information to the Mafia, so watch out!"],
        ["Added Lookout", "Added Tracker", "Added Consigliere", "Added Recon", "Added Framer", "Added `/subalignments`", "Added `/frames`", "Added `/role [role]`"], ["Role embeds have been overhauled to be simpler", "The bot now has a cool looking banner"], ["Fixed visual bug with flavor text"])

        Changelog("1.3.0", "<:mayoricon:922566007946629131>", "Law Enforcement Update", "911", 0x8b572a, 
        ["Introducing the <:mayoricon:922566007946629131> **Mayor**! They will lead the town to victory, with their increased voting influence!", "Knock knock, the <:jkicon:1226310301574758462> **Jailkeeper**'s here! The <:jkicon:1226310301574758462> **Jailkeeper** can protect someone for one night, while roleblocking them."],
        ["Added Mayor"], ["Discriminators have been removed because Discord removed them", "Simplified role embeds now have a button to show investigation results"], ["Fixed issue with `/help`", "Missing images from embed thumbnails/images have been restored"], ["Doctor can now heal themselves during the night"], False)



    def getChangelog(version:str):
        return Changelog.changelogs[version]