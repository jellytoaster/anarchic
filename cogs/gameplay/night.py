import disnake
import asyncio
import cogs.gameplay.winConditions
import cogs.gameplay.day
import classes.player
from disnake.interactions import MessageInteraction
import classes.game
import classes.role
import classes.errorhandler
import classes.enums
import utils

async def nightCycle(game:classes.game.Game):
    await cogs.gameplay.winConditions.checkForWin(game)
    if (game.finished):
        return
    
    await utils.modifySendPermissions(game.channelMafia, game, dead=False,alive=True)

    embed = disnake.Embed(title=f"**It is now Night {str(game.dayNum)} <:moon:934556372421451776>**", colour=disnake.Colour(0x1f0050))

    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/934556372421451776.webp?size=96&quality=lossless")
    embed.set_image(url="https://cdn.discordapp.com/attachments/765738640554065962/912890903545397258/IMG_0089.png")

    embed.add_field(name="Alive: `{}`".format(str(game.getAliveCount())), value=game.genAliveList())

    embed.add_field(name="Dead: `{}`".format(str(game.getDeadCount())), value=game.genDeadList())
    await game.channelTownSquare.send(embed=embed)

    await utils.modifySendPermissions(game.channelTownSquare, game, dead=False, alive=False)

    # Check if the mafioso is gone
    yesMafioso = False
    for i in game.playervar:
        if (i.assignedRole.name == "Mafioso"):
            yesMafioso == True

    if (yesMafioso != True):
        # Get members of the mafia
        mafiaPlayers = []
        for i in game.playervar:
            if (i.assignedRole.faction == classes.enums.Faction.Mafia):
                mafiaPlayers.append(i)

        promotedPlayer:classes.player.Player = sorted(mafiaPlayers, key=lambda x: x.assignedRole.promotionOrder, reverse=True)[0]
        promotedPlayer.assignedRole = classes.role.Role.toRole("Mafioso")

        embed = disnake.Embed(title=f"**{promotedPlayer.memberObj.name} has been promoted to a Mafioso!**", colour=0xd0021b)

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/891739940055052328.png?size=80")
        embed.set_footer(text="Good luck", icon_url=promotedPlayer.memberObj.display_avatar.url)


    pins = await game.channelTownSquare.pins()
    for i in pins:
        await i.unpin() 

    await sendTargetingEmbeds(game)


# Assume we only have 1 ability for now
async def sendTargetingEmbeds(game:classes.game.Game):
    try:
        import classes.player

        for i in game.playervar:
            i.defended = None
            i.isRoleBlocked = False
            i.isVoteBlocked = False


        # Perform early passives first
        for i in game.playervar:
            for x in i.assignedRole.abilities:
                if (x.type == classes.enums.AbilityType.PassiveEarly):
                    if (x.usableFunction(i, game) and utils.chargeUsable(x.charges)):
                        x.charges -= 1
                        await x.invokeMethod(x.targetingOptions(i, game.playervar, game), i, game)


        for i in game.playervar:
            i.nightTargettedPlayers = []
            asyncio.create_task(sendTargetingEmbed(i, game))

        await asyncio.sleep(33)

        # Process night actions, 1 goes first and so on
        hierarchy = sorted(game.playervar, key=lambda x: x.assignedRole.order, reverse=True)

        for i in hierarchy:
            i:classes.player.Player

            for x in i.assignedRole.abilities:
                if (x.type == classes.enums.AbilityType.Passive):
                    if (x.usableFunction(i, game) and utils.chargeUsable(x.charges)):
                        x.charges -= 1
                        await x.invokeMethod(x.targetingOptions(i, game.playervar, game), i, game)

            if (len(i.nightTargettedPlayers) == 0):
                continue

            if (i.isRoleBlocked):
                embed = disnake.Embed(title="**You were occupied!**", colour=disnake.Colour(0xffb6f0), description="**You ended up not performing your ability tonight.**")

                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1009181021859749970/1009885085002104933/IMG_0038-removebg-preview.png")
                embed.set_footer(text="Use `/status` to learn what distraction does", icon_url=i.memberObj.display_avatar.url)
                await i.memberObj.send(embed=embed)
                continue

            await i.assignedRole.abilities[0].invokeMethod(i.nightTargettedPlayers, i, game)


        await asyncio.sleep(5)

        await cogs.gameplay.day.dayCycle(game)
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)


async def sendTargetingEmbed(i:classes.player.Player, game):
    abilities = [x for x in i.assignedRole.abilities if x.type == classes.enums.AbilityType.Night]
    data = None

    playerSelectedAbility = 0
    if (abilities == [] or not utils.chargeUsable(abilities[playerSelectedAbility].charges) or abilities[playerSelectedAbility].usableFunction(i, game) == False):
        if (not i.dead):
            embed = disnake.Embed(title=f"**You have no abilities for the night**", colour=disnake.Colour(0xbbf6ff))

            embed.set_thumbnail(url=i.memberObj.display_avatar.url)
            embed.set_footer(text="Maybe tomorrow?", icon_url=i.memberObj.display_avatar.url)
            await i.memberObj.send(embed=embed)
        return

    if (i.isRoleBlocked):
        embed = disnake.Embed(title="**You were occupied!**", colour=disnake.Colour(0xffb6f0), description="**You ended up not performing your ability tonight.**")

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1009181021859749970/1009885085002104933/IMG_0038-removebg-preview.png")
        embed.set_footer(text="Use `/status` to learn what distraction does", icon_url=i.memberObj.display_avatar.url)
        await i.memberObj.send(embed=embed)
        return

    
    #Generate embed
    emb = disnake.Embed(title=f"**{i.assignedRole.name} {i.assignedRole.emoji} | <:moon:934556372421451776> {abilities[playerSelectedAbility].name}**", colour=disnake.Colour(i.assignedRole.color), description=f"**{i.assignedRole.emoji} {abilities[playerSelectedAbility].name} -** {abilities[playerSelectedAbility].description}").set_footer(text="You have 30 seconds to make a descision", icon_url=i.memberObj.display_avatar.url).add_field(name="**Use the Dropdown below to react with a target!**", value="** **", inline=False)
    
    # Generate targetting list
    allowedPlayers = abilities[playerSelectedAbility].targetingOptions(i, game.playervar, game)
    
    class TargetingDropdown(disnake.ui.StringSelect):
        def __init__(self):
            options = []

            for x in allowedPlayers:
                options.append(disnake.SelectOption(label=x.memberObj.name, description=f"Click to target {x.memberObj.name}", emoji=abilities[playerSelectedAbility].emoji, value=str(x.memberObj.id)))

            options.append(disnake.SelectOption(label="Do nothing", value="abstain", description="Do nothing tonight", emoji="❌"))

            super().__init__(placeholder="Select a player to target...", min_values=1, max_values=1, options=options)

        async def callback(self, interaction: MessageInteraction):
            selfPlayer:classes.player.Player = classes.player.Player.get(interaction.author.id, game)

            if (self.values[0] == "abstain"):

                embed = disnake.Embed(title=f"**You decide to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))
                embed.set_footer(text="You can change your action", icon_url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed)
                selfPlayer.nightTargettedPlayers.clear()
            else:
                targettedPlayer:classes.player.Player = classes.player.Player.get(int(self.values[0]), game)

                selfPlayer.nightTargettedPlayers.clear()
                selfPlayer.nightTargettedPlayers.append(targettedPlayer)

                embed = disnake.Embed(title=f"**You decide to {selfPlayer.assignedRole.abilities[0].flavorText} {targettedPlayer.memberObj.name} tonight**", colour=disnake.Colour(0xbbf6ff))

                embed.set_thumbnail(url=targettedPlayer.memberObj.display_avatar.url)
                embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=interaction.author.display_avatar.url)

                await interaction.response.send_message(embed=embed)


    class TargetingDropdownView(disnake.ui.View):
        def __init__(self) -> None:
            nonlocal data
            super().__init__(timeout=30)
            data = self

            self.add_item(TargetingDropdown())

    msg = await i.memberObj.send(embed=emb, view=TargetingDropdownView())
    await asyncio.sleep(30)
        
    for child in data.children:
        child.disabled = True

    await msg.edit(view=data)

    if (len(i.nightTargettedPlayers) == 0):
        embed = disnake.Embed(title=f"**Your final decision is to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))

        embed.set_thumbnail(url=i.memberObj.display_avatar.url)
        embed.set_footer(text="You can't change your decision anymore", icon_url=i.memberObj.display_avatar.url)
        await i.memberObj.send(embed=embed)
    else:    
        embed = disnake.Embed(title=f"**Your final decision is to {i.assignedRole.abilities[0].flavorText} {i.nightTargettedPlayers[0].memberObj.name} tonight**", colour=disnake.Colour(0xbbf6ff))

        embed.set_thumbnail(url=i.nightTargettedPlayers[0].memberObj.display_avatar.url)
        embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=i.memberObj.display_avatar.url)
        await i.memberObj.send(embed=embed)

        if (abilities[playerSelectedAbility].charges > 0):
            abilities[playerSelectedAbility].charges -= 1