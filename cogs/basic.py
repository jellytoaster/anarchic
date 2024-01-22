import disnake
import config
import classes.enums
import classes.role
import string
from disnake.ext import commands

class basic(commands.Cog):
    changelogs = [("1.0.0", disnake.Embed(title="**Anarchic 1.0.0 - Initial Release**", colour=disnake.Colour(0xeb8110), description="Welcome to Anarchic, a totally safe town where absoloutely nothing bad can happen! *(citations needed)*").add_field(name="**New Features**", value="<:add:1034558781847261194> Meet the first batch of roles! Interrogate with the <:copicon2:889672912905322516> **Cop**, Kill with the <:maficon:891739940055052328> **Mafioso**, and do much more with the <:vgicon:890339050865696798> **Vigilante**, <:docicon2:890333203959787580> **Doctor**, and <:consicon2:890336628269281350> **Consort**.\n<:add:1034558781847261194> Want to play Anarchic? Quickly join and leave a game with `/join` and `/leave`.\n<:add:1034558781847261194> Maybe you don't know what a role does. `/roles` can help! It shows you every role in Anarchic and includes a handy dandy dropdown for you to select a role to see in detail.", inline=False), "Initial release!", "<:anarchic:1009910329322512464>"),
                  ("1.1.0", disnake.Embed(title="**Anarchic 1.1.0 - Neutrals Update**", colour=disnake.Colour(0x8c8c8c), description="Two new roles arrive, but they don't seem to be siding with anyone... I wonder what they want?").add_field(name="**New Features**", value="<:add:1034558781847261194> Beware of the <:jesticon2:889968373612560394> **Jester**! This lunatic may seem harmless, but they can haunt and roleblock you if you <:lynch:1010226047456915547> **lynch** them.\n<:add:1034558781847261194> Somebody has wronged you... and you must get revenge! This is the <:hhicon2:891429754643808276> **Headhunter**, who must lynch two of their targets before they can rest in peace.\n<:add:1034558781847261194> Need help? `/help` shows you every command in the bot if you really need it.\n<:add:1034558781847261194> Look in the past! Use `/changelog` to see what new features have been added update after update.\n<:add:1034558781847261194> Share setups with your friends! Use `/setup export` to get a copy-pastable version of your current setup. Your friends can import your setup with `/setup import`!", inline=False).add_field(name="**Game Changes**", value="<:change:1034559083627429918> Fate-deciding results now say none if nobody votes\n<:change:1034559083627429918> Empty setups now say \"Empty\" for setup names", inline=False).add_field(name="**Bug Fixes**", value="<:remove:1198401946567049327> Fixed issues with party commands with default avatars\n<:remove:1198401946567049327> /host now works properly\n<:remove:1198401946567049327> Fixed issues with /setup while there is no party", inline=False), "Neutrals and more", "<:hhicon2:891429754643808276>"),
                  ("1.1.1", disnake.Embed(title="**Anarchic 1.1.1**", colour=disnake.Colour(0x8c8c8c), description="Boring minor update").add_field(name="**Game Changes**", value="<:change:1034559083627429918> Importing setups now have a confirmation"), "Minor Update", "🔧"),
                  ("1.2.0", disnake.Embed(title="**Anarchic 1.2.0 - Investigatives Update**", colour=disnake.Colour(0x318004), description="Two new roles arrive, but they don't seem to be siding with anyone... I wonder what they want?").add_field(name="**New Features**", value="<:add:1034558781847261194> Beware of the <:jesticon2:889968373612560394> **Jester**! This lunatic may seem harmless, but they can haunt and roleblock you if you <:lynch:1010226047456915547> **lynch** them.\n<:add:1034558781847261194> Somebody has wronged you... and you must get revenge! This is the <:hhicon2:891429754643808276> **Headhunter**, who must lynch two of their targets before they can rest in peace.\n<:add:1034558781847261194> Need help? `/help` shows you every command in the bot if you really need it.\n<:add:1034558781847261194> Look in the past! Use `/changelog` to see what new features have been added update after update.\n<:add:1034558781847261194> Share setups with your friends! Use `/setup export` to get a copy-pastable version of your current setup. Your friends can import your setup with `/setup import`!", inline=False).add_field(name="**Game Changes**", value="<:change:1034559083627429918> Fate-deciding results now say none if nobody votes\n<:change:1034559083627429918> Empty setups now say \"Empty\" for setup names", inline=False).add_field(name="**Bug Fixes**", value="<:remove:1198401946567049327> Fixed issues with party commands with default avatars\n<:remove:1198401946567049327> /host now works properly\n<:remove:1198401946567049327> Fixed issues with /setup while there is no party", inline=False), "Neutrals and more", "<:hhicon2:891429754643808276>")
                  ]

    def getChangelog(version:str):
        return next((i for i in basic.changelogs if i[0] == version), None)


    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="role", description="Get info on a specific role", options=[disnake.Option(name="name", description="What role?", type=disnake.OptionType.string, required=True)])
    async def role(self, inter:disnake.ApplicationCommandInteraction, name):
        if (classes.role.Role.toRole(name) == None):
            await inter.response.send_message("That's not a role!", ephemeral=True)
            return

        await inter.response.send_message(embed=classes.role.Role.toRole(name).roleEmbed)

    @commands.slash_command(name="roles", description="Get a description of every role in Anarchic")
    async def roles(self, inter: disnake.ApplicationCommandInteraction):
        import classes.role
        import classes.enums
        embed = disnake.Embed(title=f"Anarchic Roles (as of {config.VERSION})", colour=disnake.Colour(0xf5a623))

        role_fields = {  
            classes.enums.Faction.Town: {"name": "__<:town:1007768656341651547> **Town**__", "roles": []},
            classes.enums.Faction.Mafia: {"name": "__<:mafia:1007768566789050378> **Mafia**__", "roles": []},
            classes.enums.Faction.Neutral: {"name": "__:axe: **Neutral**__", "roles": []}
        }

        for i in classes.role.Role.allRoles:
            i: classes.role.Role
            role_info = f"{i.emoji} {i.name}\n"
            role_fields[i.faction]["roles"].append(role_info)

        for _, data in role_fields.items():
            embed.add_field(name=data["name"], value="".join(data["roles"]), inline=True)

        class RoleDropdown(disnake.ui.StringSelect):
            def __init__(self):
                options = [
                    disnake.SelectOption(
                        label=i.name,
                        description="Click to view more info about this",
                        emoji=i.emoji,
                        value=i.name
                    )
                    for i in classes.role.Role.allRoles
                ]

                super().__init__(placeholder="Select a role for more info...", options=options)

            async def callback(self, inter: disnake.MessageInteraction):
                await inter.response.send_message(
                    embed=classes.role.Role.toRole(self.values[0].lower()).roleEmbed,
                    ephemeral=True
                )

        class RoleView(disnake.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=180)
                self.add_item(RoleDropdown())
                self.inter:disnake.ApplicationCommandInteraction = inter

            async def on_timeout(self) -> None:
                for child in self.children:
                    child.disabled = True

                newEmbed = embed.set_footer(text="This interaction has timed out. Use /roles again to use the dropdown.")

                await self.inter.edit_original_message(embed=newEmbed, view=self)

        view = RoleView()
        await inter.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="changelog", description="Learn about the latest features")
    async def changelog(inter:disnake.ApplicationCommandInteraction):
        # Reminding myself which emojis to use
        # Addition = <:add:1034558781847261194>
        # Bug Fixes = <:remove:1198401946567049327>
        # Changes = <:change:1034559083627429918>
        # Quality of Life changes = <:orange:1198402176607862946>

        class ChangelogDropdown(disnake.ui.StringSelect):
            def __init__(self):
                options = []
                for n in basic.changelogs:
                    options.append(disnake.SelectOption(label=n[0], description=n[2], emoji=n[3]))

                super().__init__(placeholder="Select a version...", options=options)
            
            async def callback(self, inter:disnake.MessageInteraction):
                await inter.response.edit_message(embed=basic.getChangelog(self.values[0])[1].set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421").set_footer(text="Use the dropdown to see previous/future updates.", icon_url=inter.author.display_avatar.url), view=ChangelogView())

        class ChangelogView(disnake.ui.View):
            def __init__(self):
                super().__init__(timeout=180)
                self.inter:disnake.ApplicationCommandInteraction = inter

                self.add_item(ChangelogDropdown())

            async def on_timeout(self) -> None:
                for child in self.children:
                    child.disabled = True

                orgmsg:disnake.InteractionMessage = await self.inter.original_message()
                newEmbed = orgmsg.embeds[0].set_footer(text="This interaction has timed out. Use /changelog again to use the dropdown.")

                await self.inter.edit_original_message(embed=newEmbed, view=self)

        await inter.response.send_message(embed=basic.getChangelog(config.VERSION)[1].set_thumbnail(url="https://images-ext-1.discordapp.net/external/zvBfC-Hei3zC-NkTa_MJ1t-lx4Fu6dXoB-5uzicvPYE/https/images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%253Fwidth%253D468%2526height%253D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?format=webp&quality=lossless&width=421&height=421").set_footer(text="Use the dropdown to see previous/future updates.", icon_url=inter.author.display_avatar.url), view=ChangelogView())

    @commands.slash_command(name="about", description="Learn about devs of Anarchic, and invite the bot to your server!")
    async def about(inter):
        embed = disnake.Embed(title="Anarchic", colour=disnake.Colour(0xff8b6c), description="*Hosts games of Anarchic, which are styled similar to the classic party game Mafia!*")

        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.set_footer(text="Invite me to your server!", icon_url=inter.author.display_avatar.url)
        embed.add_field(name="Invite me", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=887118309827432478&permissions=268954688&scope=bot+applications.commands)", inline=False)
        embed.add_field(name="Join the support server", value="[Click Here](https://discord.gg/8CF3Ccgq8c)", inline=False)
        embed.add_field(name="Anarchic Dev Team", value=f"**:art: Artists - evanzhaaa, temporary0533**\n**:computer: Programmers - jellytoaster**\n**:video_game: Designer - c.atasyl**")

        await inter.response.send_message(embed=embed)

    @role.autocomplete("name")
    async def autoCompleteRole(inter, input):
        return [string.capwords(e.name) for e in classes.role.Role.allRoles if input.lower() in e.name.lower()]
