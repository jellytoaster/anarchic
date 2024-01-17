from typing import Optional
import disnake
import config
from disnake.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Get help about the bot")
    async def help(inter:disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(title="**Welcome to Anarchic!**", colour=disnake.Colour(0xf8e71c), description="Anarchic is a brand new way to play the pouplar game Mafia. To quickly set up, use `/join` and invite your friends!")

        embed.set_thumbnail(url=inter.guild.icon.url)
        embed.set_footer(text="Try using one of the commands!", icon_url=inter.author.avatar.url)

        embed.add_field(name="⇒ **Categories**", value="**Party** - `/help party`\n**Setup** - `/help setup`")

        class HelpChooser(disnake.ui.StringSelect):
            def __init__(self):
                options = [
                    disnake.SelectOption(
                        label="Info", description="Learn about the bot", emoji="ℹ️", value="info"
                    ),
                    disnake.SelectOption(
                        label="Party", description="Category for joining and leaving games", emoji="🎉", value="party"
                    ),
                    disnake.SelectOption(
                        label="Setup", description="Category for adding roles to a setup", emoji="🧰", value='setup'
                    )
                ]
                super().__init__(placeholder="Choose a category for more detail...", min_values=1, max_values=1, options=options)


            async def callback(self, inter: disnake.MessageInteraction):
                await inter.response.edit_message(embed=createEmbed(self.values[0], inter.author), view=HelpView())

        class HelpView(disnake.ui.View):
            def __init__(self) -> None:
                super().__init__(timeout=180)
                self.add_item(HelpChooser())

        await inter.response.send_message(embed=embed, view=HelpView())


        def createEmbed(type:str, author:disnake.Member):
            helpEmbeds = {
                "party": disnake.Embed(title="**Help - Party**", colour=disnake.Colour(0xf8e71c), description="You can use commands in this category for joining and leaving games, and also host only options like kicking users from your lobby.\n\n***NOTE: An asterisk in front of a command is host only***").add_field(name="⇒ **Commands**", value="**╰ Join party**\n   `/join`\n**╰ Leave party**\n   `/leave`\n**╰ View party**\n   `/party`\n**╰ Kick a player***\n   `/kick [user]`\n**╰ Promote a player***\n   `/host [user]`\n**╰ Start game***\n   `/start`"),
                "setup" : disnake.Embed(title="**Help - Setup**", colour=disnake.Colour(0xf8e71c), description="You can use commands in this category for modifying setups. Setups define what roles appear in your game, so make sure you create balanced setups when playing with friends.\n\n***NOTE: An asterisk in front of a command is host only***").add_field(name="⇒ **Commands**", value="**╰ View setup**\n   `/setup view`\n**╰ Add role to setup***\n   `/setup add [role] [amount]`\n**╰ Remove role from setup***\n   `/setup remove [role] [amount]`\n**╰ Use a preset setup***\n   `/setup preset [setup]`\n**╰ Clear setup***\n   `/setup clear`"),
                "info" : disnake.Embed(title="**Help - Info**", colour=disnake.Colour(0xf8e71c), description="You can use commands in this category for seeing general info about the bot. You can see info about roles, and other stuff.").add_field(name="⇒ **Commands**", value="**╰ Help**\n   `/help`\n**╰ View role info**\n   `/roles`\n")

            }

            return helpEmbeds[type].set_thumbnail(author.guild.icon.url).set_footer(text="Try using one of the commands!", icon_url=author.avatar.url)
