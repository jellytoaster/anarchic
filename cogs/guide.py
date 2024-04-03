import disnake
from disnake.ext import commands

guideEmbeds = {
    "party": disnake.Embed(title="How to play Anarchic - Party", colour=disnake.Colour(0xcf9dd9), description="Before playing a game of Anarchic, a party needs to be set up before starting!\n\nTo join a party, use </join:1000038596994138132>. The first player to join a party is the **host**. Hosts can change roles in the setup, kick members from the party, and start the game. To leave a party, use </leave:1000038596994138133>.\n\nGathering members is not the only requirement to starting a game. You also need a valid **setup**!\n\nYou can add roles to your setup by using </setup add:1000038596994138135> to add a role to your party, with the option to add multiple at a time. The same applies to </setup remove:1000038596994138135>, of course removing roles. If you're looking for inspiration for setups, use </setup preset:1000038596994138135>, loading a preset setup made by the developers.\n\nAfter creating your setup and gathering players, you can start the game using </start:1000038596994138136>!").add_field(name="Commands Used", value="╰ `/join` - Join a party\n╰ `/leave` - Leave a party\n╰ `/setup add` - Add a role to the setup\n╰ `/setup remove` - Remove a role from the setup\n╰ `/setup preset` - Use a preset setup\n╰ `/start` - Start the game!\n"),
    "roles/abilities" : disnake.Embed(title="How to play Anarchic - Roles/Abilities", colour=disnake.Colour(0xcf9dd9), description="Anarchic has special and unique **roles** with a variety of purposes. For example, the <:copicon2:889672912905322516> **Cop** can investigate players to see if they are aligned with the <:mafia:1007768566789050378> **Mafia**.\n\nEvery <:moon:934556372421451776> **Night** (or day), your role can perform specific :star2: **Abilities**. You can investigate, protect, or even kill! When you get a direct message from the bot asking you for a target/ability selection, you can use the dropdown at the bottom of the message to make your selection.\n\nDuring the selection period, you can alter your decision until time runs out. After **30** seconds, the selection will be locked and if you didn't make one by then, you will do nothing for that phase."),
    "daytime" : disnake.Embed(title="How to play Anarchic - Daytime", colour=disnake.Colour(0xcf9dd9), description="After the horrors of the <:moon:934556372421451776> **Night**, the sun rises and players can discuss on who the <:mafia:1007768566789050378> **Mafia** is. Beware, as after discussion awaits a phase where you can vote on players to be <:lynch:1010226047456915547> **Lynched**!\n\nWhen a day starts, all players will be notified as to the players who have died on the last <:moon:934556372421451776> **Night**. After this, the **dawn** phase begins. During the dawn phase, players with dawn :star2: **abilities** can use their ability, while players can discuss on their investigation results, and more importantly who the <:mafia:1007768566789050378> **Mafia** is.\n\nSoon after, the **noon** phase begins. Players can vote on other players to <:lynch:1010226047456915547> **Lynch**. To start a <:trial:1010903922916991006> **trial**, there must be votes from half the alive player count plus one. In other words, there must be a majority vote to start a <:trial:1010903922916991006> **trial**.\n\nDuring a <:trial:1010903922916991006> **trial**, the accused player can defend themselves and list reasons why they should not be <:lynch:1010226047456915547> **lynched**. Then, players may decide if they are guilty or not. If majority of the players think the accused are guilty, they will be <:lynch:1010226047456915547> **lynched** and their role will be revealed to everyone. If players decide they are innocent or the voting results in a tie, the accused will not be <:lynch:1010226047456915547> **lynched**, and the <:moon:934556372421451776> **night** phase will begin."),
    "nighttime" : disnake.Embed(title="How to play Anarchic - Nighttime", colour=disnake.Colour(0xcf9dd9), description="When the sun sets, the <:moon:934556372421451776> **Night** phase begins. During this phase, most roles can perform their :star2: **abilities**, like investigations, protections, and possibly even killings.\n\nWhen the <:moon:934556372421451776> **Night** starts, you will recieve a message in direct messages asking you for a target. If you have multiple abilities, you will be asked to choose which ability to perform for the night. You also have the ability to choose to do nothing for the night.\n\nAfter **30** seconds, your choice will be locked and cannot be changed. Then, all actions will be processed. Actions go in this order:\n• \🎭 **Roleblocking**\n• \💉 **Protections**\n• \🔎 **Investigations**\n• \🗡️ **Killings**\n\nAfter actions have been processed, the day phase begins, and it repeats..."),
    "winning" : disnake.Embed(title="How to play Anarchic - Winning", colour=disnake.Colour(0xcf9dd9), description="This is fun and all, but how do you win the game? There are multiple conditions for the game to end. Some are good, but some aren't...\n\nThe game checks if win conditions have been met at the start of the <:sun:1008839043192213686> **Day**, and the start of the <:moon:934556372421451776> **Night**. Each role has their own win conditions. For example, the <:town:1007768656341651547> **Town**'s win condition is to defeat all members of the <:mafia:1007768566789050378> **Mafia**. 🪓 **Neutral** roles have their own seperate win conditions.\n\nIf all players have died in one night, it is considered a **draw**. Neither side wins, except for 🪓 **Neutrals**, which acheive a win depending on if they have fulfilled the win condition on their role card.\n\nSomething to worry about is the **Plague**, which will occur when no players have died for __three__ days in a row. On the __second__ day, players will be reminded to <:lynch:1010226047456915547> **Lynch** or kill a player or all players will **die** on the following day.")
}


def createEmbed(type:str, author:disnake.Member):
    res = guideEmbeds[type].set_footer(text="Use the dropdown to select subcategories.", icon_url=author.display_avatar.url)

    res.set_thumbnail(url="https://cdn.discordapp.com/emojis/1009910329322512464.webp?size=128&quality=lossless")

    return res

class GuideCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="guide", description="Learn how to play Anarchic", options=[disnake.Option(name="subcategory", description="Which subcategory to show", type=disnake.OptionType.string, choices=["Party","Roles/Abilities","Nighttime", "Daytime", "Winning"])])
    async def guide(inter:disnake.ApplicationCommandInteraction, subcategory:str=None):
        embed = None
    
        if (subcategory == None):
            embed = disnake.Embed(title="**How to play Anarchic**", colour=disnake.Colour(0xb8e986), description="*Learn to play Anarchic through each of the subcategories. You'll also need to put your social deduction skills to work!*")

            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1009910329322512464.webp?size=128&quality=lossless")
            embed.set_footer(text="Use the dropdown to select subcategories.", icon_url=inter.author.display_avatar.url)

            embed.add_field(name="⇒ **Subcategories**", value="🎉 **Party** - Learn how to join a party and create a setup\n🕹️ **Roles/Abilities** - Learn the powers of each role\n<:moon:934556372421451776> **Nighttime** - Learn about performing night actions\n☀️ **Daytime** - Vote and lynch the Mafia\n🏆 **Winning** - Learn win conditions for different roles")
        else:
            embed = createEmbed(subcategory.lower(), inter.author)

        class GuideChooser(disnake.ui.StringSelect):
            def __init__(self):
                options = [
                    disnake.SelectOption(
                        label="Party", description="Joining and leaving a game", emoji="🎉", value="party"
                    ),
                    disnake.SelectOption(
                        label="Roles/Abilities", description="Roles have their own unique abilities", emoji="🕹️", value="roles/abilities"
                    ),
                        disnake.SelectOption(
                        label="Daytime", description="Lynch the Mafia, and some Townies along the way", emoji="☀️", value='daytime'
                    ),
                    disnake.SelectOption(
                        label="Nighttime", description="Perform your abilities (or die)", emoji="<:moon:934556372421451776>", value='nighttime'
                    ),
                    disnake.SelectOption(
                        label="Winning", description="How do you win the game?", emoji="🏆", value='winning'
                    )
                ]
                super().__init__(placeholder="Choose a category for more detail...", min_values=1, max_values=1, options=options)


            async def callback(self, inter: disnake.MessageInteraction):
                await inter.response.edit_message(embed=createEmbed(self.values[0], inter.author), view=GuideView())

        class GuideView(disnake.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=180)
                self.add_item(GuideChooser())

        await inter.response.send_message(embed=embed, view=GuideView())