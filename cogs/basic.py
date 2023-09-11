import disnake
import config
from disnake.ext import commands

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Get help about the bot")
    async def help(self, inter:disnake.ApplicationCommandInteraction):
        await inter.response.send_message("the content here", ephemeral=True)

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
                super().__init__()
                self.add_item(RoleDropdown())

        await inter.response.send_message(embed=embed, view=RoleView())