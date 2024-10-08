import disnake
import config
import classes.enums
import classes.role
import classes.changelog
import classes.contraction
import string
from disnake.ext import commands

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # if i'm mentioned, reply to ensure i'm alive
    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if message.author.id == self.bot.user.id:
            return
        if self.bot.user.mentioned_in(message):
            await message.channel.send("Welcome to Anarchic! Use </help:1197301625224704040> for more info.", reference=message, mention_author=False)

    @commands.slash_command(name="role", description="Get info on a specific role", options=[disnake.Option(name="name", description="What role?", type=disnake.OptionType.string, required=True)])
    async def role(self, inter:disnake.ApplicationCommandInteraction, name):
        if (classes.role.Role.toRole(name) == None):
            await inter.response.send_message("That's not a role!", ephemeral=True)
            return
        
        embed = classes.role.Role.toRole(name).buildEmbedSimple()
        
        class RoleView(disnake.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=180)
                self.inter:disnake.ApplicationCommandInteraction = inter

            async def on_timeout(self) -> None:
                for child in self.children:
                    child.disabled = True

                newEmbed = embed.set_footer(text="This interaction has timed out. Use /role again to use the button.")
                await self.inter.edit_original_message(embed=newEmbed, view=self)

            @disnake.ui.button(label="Investigation Results", emoji="<:magn:1226319132061077624>", style=disnake.ButtonStyle.grey)
            async def investigationresults(self, button, intera):
                embed = classes.role.Role.toRole(name).buildInvestigationResults()
                await intera.response.send_message(embed=embed)

        view = RoleView()
        await inter.response.send_message(embed=embed, view=view)

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
                    for i in classes.role.Role.allRoles[:25]
                ]

                super().__init__(placeholder="Select a role for more info...", options=options)

            async def callback(self, inter: disnake.MessageInteraction):
                await inter.response.send_message(
                    embed=classes.role.Role.toRole(self.values[0].lower()).buildEmbedSimple(),
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

    @commands.slash_command(name="subalignments", description="Learn about subalignments and what roles fall in their category", options=[disnake.Option("faction", "What faction to use. Town if none is chosen.", disnake.OptionType.string, False, choices=["Town", "Mafia", "Neutral"])])
    async def subalignments(inter:disnake.ApplicationCommandInteraction, faction="town"):
        faction = faction.lower()
        factionColors = {"town" : 0x7ed321, "all" : 0x7ed321, "mafia": 0xd0021b, "neutral":0x9b9b9b}

        embed = disnake.Embed(title=f"Anarchic Subalignments | {string.capwords(faction)}", color=factionColors[faction], description=f"Here is a list of **{string.capwords(faction)}** roles in Anarchic")
        
        organizedRoles = {}
        for role in classes.role.Role.allRoles:
            myType = f"{role.faction.name}{role.type}"
            if (not (myType in organizedRoles)):
                organizedRoles[myType] = []
            organizedRoles[myType].append(role)

        def remove(str, toRemove):
            return str.replace(toRemove, "")

        for key, value in organizedRoles.items():
            if (key.lower().startswith(faction)):
                roles = []
                for i in value:
                    roles.append(f"{i.emoji} **{i.name}**")
                val = "\n".join(roles)

                name = f"{string.capwords(faction)} {string.capwords(key.lower().replace(faction, ''))}"
                embed.add_field(f"`{name} {classes.contraction.Contraction.getContraction(faction, key.lower().replace(faction, '')).emoji}`", val, inline=False)


        await inter.response.send_message(embed=embed) 

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
                for k, v in classes.changelog.Changelog.changelogs.items():
                    if (v.usable):
                        options.append(disnake.SelectOption(label=v.ver, description=v.description, emoji=v.emoji))

                super().__init__(placeholder="Select a version...", options=options)
            
            async def callback(self, inter:disnake.MessageInteraction):
                await inter.response.edit_message(embed=classes.changelog.Changelog.getChangelog(self.values[0]).makeEmbed().set_footer(text="Use the dropdown to see previous/future updates.", icon_url=inter.author.display_avatar.url), view=ChangelogView())

        class ChangelogView(disnake.ui.View):
            def __init__(self):
                super().__init__(timeout=180)
                self.inter:disnake.ApplicationCommandInteraction = inter

                self.add_item(ChangelogDropdown())

            async def on_timeout(self) -> None:
                for child in self.children:
                    child.disabled = True

                orgmsg:disnake.InteractionMessage = await self.inter.original_message()
                newEmbed = orgmsg.embeds[0].set_footer(text="This interaction has timed out. Use /changelog again to use the dropdown.", icon_url=inter.author.avatar.url)

                await self.inter.edit_original_message(embed=newEmbed, view=self)

        await inter.response.send_message(embed=classes.changelog.Changelog.getChangelog(config.VERSION).makeEmbed().set_footer(text="Use the dorpdown to select a version.", icon_url=inter.author.avatar.url), view=ChangelogView())

    @commands.slash_command(name="about", description="Learn about devs of Anarchic, and invite the bot to your server!")
    async def about(inter:disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="Anarchic", colour=disnake.Colour(0xff8b6c), description="*Hosts games of Anarchic, which are styled similar to the classic party game Mafia!*")

        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.set_footer(text="Invite me to your server!", icon_url=inter.author.display_avatar.url)
        embed.add_field(name="Invite me", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=887118309827432478&permissions=268954688&scope=bot+applications.commands)", inline=False)
        embed.add_field(name="Join the support server", value="[Click Here](https://discord.gg/8CF3Ccgq8c)", inline=False)
        embed.add_field(name="Anarchic Dev Team", value=f"**:art: Artists - evanzhaaa, temporary0533**\n**:computer: Programmers - jellytoaster**\n**:video_game: Designer - c.atasyl**")

        embed.add_field(name="Special Thanks", value=f"**:art: c.atasyl, skippppyyy**")

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="frames", description="Display the investigation results for player framing")
    async def frames(inter):
        embed = disnake.Embed(title="Investigation results for frames", colour=disnake.Colour(0xd0021b), description=f"As of **{config.VERSION}**, here are the results **\🔎 Town Investigative** roles will recieve if their target is <:frameicon2:890365634913902602> **Framed**.")

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/890365634913902602.webp")
        embed.set_footer(text="Try not to get framed!", icon_url=inter.author.display_avatar.url)

        embed.add_field(name="<:copicon2:889672912905322516> __Cop__", value="Your target is sided with the <:mafia:1007768566789050378> **Mafia**!", inline=False)
        embed.add_field(name="<:trackicon:922885543812005949> __Tracker__", value="Your target visited the Mafia night kill", inline=False)
        embed.add_field(name="<:loicon2:889673190392078356> __Lookout__", value="The Mafia night kill will be visited by the framed player", inline=False)
        
        await inter.response.send_message(embed=embed)

    # Option autocompletes
    @role.autocomplete("name")
    async def autoCompleteRole(inter, input):
        return [string.capwords(e.name) for e in classes.role.Role.allRoles if input.lower() in e.name.lower()]
