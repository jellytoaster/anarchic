import disnake

class Changelog():
    changelogs = {}
    def __init__(self, version, emoji, title, description, color, highlights:list, adds:list, changes:list, fixes:list) -> None:
        self.emoji = emoji
        self.ver = version
        self.title = title
        self.description = description
        self.color = color

        self.highlights = highlights
        self.adds = adds
        self.changes = changes
        self.fixes = fixes
        
        Changelog.changelogs[version] = self

    def makeEmbed(self) -> disnake.Embed:
        embed = disnake.Embed(
            title=f"Anarchic {self.ver} - {self.title}",
            description=self.description,
            color=disnake.Color(self.color)
        )
        
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421")

        def format(icon, items):
            return f"{icon} " + f"\n{icon} ".join(items) if items else None

        embed.add_field(name="Highlights", value=format('<:highlight:1199861697989586965>', self.highlights), inline=False)
        embed.add_field(name="New Features", value=format('<:add:1034558781847261194>', self.adds), inline=False)
        embed.add_field(name="Game Changes", value=format('<:change:1034559083627429918>', self.changes), inline=False)
        embed.add_field(name="Bug Fixes", value=format('<:remove:1198401946567049327>', self.fixes), inline=False)

        return embed

    def initChangelogs():
        Changelog("1.0.0", "<:anarchic:1126529977362427934>", "Initial Release", "Welcome to Anarchic!", 0x7ed321, [],["Added 7 roles: Cop, Mafioso, Doctor, Consort, Vigilante, Villager, and Associate", "Added general gameplay mechanics"], [], [])

        Changelog("1.1.0", "<:hhicon2:891429754643808276>", "Neutrals Update", "Two new roles arrive, but they don't seem to be siding with anyone... I wonder what they want?", 0x8c8c8c, 
        ["Beware of the <:jesticon2:889968373612560394> **Jester**! This lunatic may seem harmless, but they can haunt and roleblock you if you <:lynch:1010226047456915547> **lynch** them.","Somebody has wronged you... and you must get revenge! This is the <:hhicon2:891429754643808276> **Headhunter**, who must **lynch** two of their targets before they can rest in peace."],
        ["Added Jester", "Added Headhunter", "Added `/help`", "Added `/changelog`", "Added setup import/export with `/setup import` and `/setup export`"], ["Fate-deciding results now say none if nobody votes", "Empty setups now say \"Empty\" for setup names"], ["Fixed issues with party commands with default avatars", "/host now works properly", "Fixed issues with /setup while there is no party"])

        Changelog("1.2.0", "<:loicon2:889673190392078356>", "Investigative Update", "Unleash a package of 5 new investigative roles!", 0xb8e986, 
        ["Beware of the <:jesticon2:889968373612560394> **Jester**! This lunatic may seem harmless, but they can haunt and roleblock you if you <:lynch:1010226047456915547> **lynch** them.","Somebody has wronged you... and you must get revenge! This is the <:hhicon2:891429754643808276> **Headhunter**, who must **lynch** two of their targets before they can rest in peace."],
        ["Added Lookout", "Added Tracker", "Added Consigliere", "Added Recon", "Added Framer", "Added `/subalignments`", "Added `/role [role]`"], ["", ""], [])


    def getChangelog(version:str):
        return Changelog.changelogs[version]