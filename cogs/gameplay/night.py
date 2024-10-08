import disnake
import asyncio
import cogs.gameplay.winConditions
import cogs.gameplay.day
import copy
import classes.player
from disnake.interactions import MessageInteraction
import classes.game
import classes.role
import classes.errorhandler
import classes.enums
import time
import utils

async def nightCycle(game:classes.game.Game):
    await cogs.gameplay.winConditions.checkForWin(game)
    if (game.finished):
        return
    
    await utils.mafiaModifySend(game.channelMafia, game, True)

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
        if (i.assignedRole.name.lower() == "mafioso"):
            yesMafioso == True

    if (yesMafioso == False):
        # Get members of the mafia
        mafiaPlayers = []
        for i in game.playervar:
            if (i.assignedRole.faction == classes.enums.Faction.Mafia):
                mafiaPlayers.append(i)

        # Decending order so larger vals execute first
        promotedPlayer:classes.player.Player = sorted(mafiaPlayers, key=lambda x: x.assignedRole.promotionOrder)[0]
        promotedPlayer.assignedRole = classes.role.Role.toRole("Mafioso")

        embed = disnake.Embed(title=f"**{promotedPlayer.memberObj.name} has been promoted to a Mafioso!**", colour=0xd0021b)

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/891739940055052328.png?size=80")
        embed.set_footer(text="Good luck", icon_url=promotedPlayer.memberObj.display_avatar.url)

        await game.channelMafia.send(embed=embed,content=promotedPlayer.memberObj.mention)


    pins = await game.channelTownSquare.pins()
    for i in pins:
        await i.unpin() 

    await sendTargetingEmbeds(game)

async def sendTargetingEmbeds(game:classes.game.Game):
    try:
        import classes.player
        ts = time.time()

        game.mafNightKill.clear()

        for i in game.playervar:
            i.defended = None
            i.isRoleBlocked = False
            i.isVoteBlocked = False
            i.playerSelectedAbility = -1
            i.assignedRole.investigationResults.reset(i)


        # Perform early passives first
        for i in game.playervar:
            for x in i.assignedRole.abilities:
                if (x.type == classes.enums.AbilityType.PassiveEarly):
                    if (x.usableFunction(i, game) and utils.chargeUsable(x.charges)):
                        x.charges -= 1
                        await x.invokeMethod(x.targetingOptions(i, game.playervar, game), i, game)


        for i in game.playervar:
            i.nightTargettedPlayers = []
            i.assignedRole.investigationResults.lookoutVisitedBy = []
            i.assignedRole.investigationResults.trackerTargetted = []
            #calculate usable abilities
            abilities = [x for x in i.assignedRole.abilities if x.type == classes.enums.AbilityType.Night]
            usableAbilities = 0 

            for abil in abilities:
                if utils.chargeUsable(abil.charges) and abil.usableFunction(i, game) == True:
                    usableAbilities += 1

            if usableAbilities == 0 and not i.dead:
                embed = disnake.Embed(title=f"**You have no abilities for the night**", colour=disnake.Colour(0xbbf6ff))

                embed.set_thumbnail(url=i.memberObj.display_avatar.url)
                embed.set_footer(text="Maybe tomorrow?", icon_url=i.memberObj.display_avatar.url)
                await i.memberObj.send(embed=embed)
                continue
            
            if usableAbilities > 1 or i.assignedRole.alwaysUseAbilitySelection:
                asyncio.create_task(sendAbilitySelectionEmbed(i, game, ts))  
            elif usableAbilities == 1:
                asyncio.create_task(sendTargetingEmbed(i, game, 0, 0))
                

        await asyncio.sleep(33)

        # First of all, put night actions into their investigation results
        for i in game.playervar:
            i:classes.player.Player
            i.assignedRole.investigationResults.lookoutVisitedBy = copy.copy(i.whoVisitedMe())
            i.assignedRole.investigationResults.trackerTargetted = copy.copy(i.nightTargettedPlayers)

        # Second of all, calculate mafia night kill
        for i in classes.player.Player.getPlayersWithRole("Mafioso", game):
            if (i.nightTargettedPlayers != []):
                game.mafNightKill.append(i.nightTargettedPlayers[0])

        # Process night actions, 1 goes first and so on
        hierarchy = sorted(game.playervar, key=lambda x: x.assignedRole.order, reverse=True)

        for i in hierarchy:
            i:classes.player.Player

            for x in i.assignedRole.abilities:
                if (x.type == classes.enums.AbilityType.Passive):
                    if (x.usableFunction(i, game) and utils.chargeUsable(x.charges)):
                        x.charges -= 1
                        await x.invokeMethod(x.targetingOptions(i, game.playervar, game), i, game)

            if (len(i.nightTargettedPlayers) == 0 and i.playerSelectedAbility == -1):
                continue

            if (i.isRoleBlocked):
                embed = disnake.Embed(title="**You were occupied!**", colour=disnake.Colour(0xffb6f0), description="**You ended up not performing your ability tonight.**")

                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1009181021859749970/1009885085002104933/IMG_0038-removebg-preview.png")
                embed.set_footer(text="Use `/status` to learn what distraction does (not inplemented yet sorry)", icon_url=i.memberObj.display_avatar.url)
                await i.memberObj.send(embed=embed)
                continue

            abilities = [x for x in i.assignedRole.abilities] 
            await abilities[i.playerSelectedAbility].invokeMethod(i.nightTargettedPlayers, i, game)

        await asyncio.sleep(5)

        await cogs.gameplay.day.dayCycle(game)
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)

async def sendAbilitySelectionEmbed(originPlayer:classes.player.Player, game, timestamp):
    embed = disnake.Embed(title="Select an ability", colour=originPlayer.assignedRole.color, description="Select an ability to use for the night. You can also abstain, which will make you do nothing for the night. You have **30** seconds to pick an ability and select a target(s).")

    embed.set_thumbnail(url=originPlayer.assignedRole.getIconUrl())
    embed.set_footer(text="Use the dropdown to select an ability!", icon_url=originPlayer.memberObj.display_avatar.url)

    # generate ability list
    abilities = [x for x in originPlayer.assignedRole.abilities if x.type == classes.enums.AbilityType.Night and utils.chargeUsable(x.charges) and x.usableFunction(originPlayer, game) == True]
    for ability in abilities:
        embed.add_field(name=f"<:moon:934556372421451776> **{ability.name}** | {utils.chargeCountSimpleSimple(ability.charges)}", value=ability.description, inline=False)

    embed.add_field(name=":x: **Do nothing**", value="Do nothing for the night", inline=False)

    msg = None

    class AbilitySelectionDropdown(disnake.ui.StringSelect):
        def __init__(self):
            options = []
            for ability in abilities:
                options.append(disnake.SelectOption(label=ability.name, description=ability.description,value=str(abilities.index(ability)), emoji=ability.emoji))

            options.append(disnake.SelectOption(label="Do nothing", description="Do nothing for the night", value="-1", emoji="❌"))

            super().__init__(
                placeholder="Select an ability...",
                min_values=1,
                max_values=1,
                options=options)
            
        async def callback(self, interaction: MessageInteraction) -> None:
            self.disabled = True

            if self.values[0] == "-1":
                await msg.edit(view=self.view)

                embed = disnake.Embed(title=f"**Your decision is to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))

                embed.set_thumbnail(url=originPlayer.memberObj.display_avatar.url)
                embed.set_footer(text="You can't change your decision anymore", icon_url=originPlayer.memberObj.display_avatar.url)
                await interaction.response.send_message(embed=embed)
            else:
                await sendTargetingEmbed(originPlayer, game, timestamp - time.time(), self.values[0], interaction)
                await msg.edit(view=self.view)
                
    class SelectionView(disnake.ui.View):
        def __init__(self) -> None:
            super().__init__(timeout=30)
            self.add_item(AbilitySelectionDropdown())

        async def on_timeout(self) -> None:
            if (originPlayer.playerSelectedAbility == -1):
                for child in self.children:
                    child.disabled = True

                await msg.edit(view=self)

                embed = disnake.Embed(title=f"**Your final decision is to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))

                embed.set_thumbnail(url=originPlayer.memberObj.display_avatar.url)
                embed.set_footer(text="You can't change your decision anymore", icon_url=originPlayer.memberObj.display_avatar.url)
                await originPlayer.memberObj.send(embed=embed)

    msg = await originPlayer.memberObj.send(embed=embed, view=SelectionView())
    


async def sendTargetingEmbed(i:classes.player.Player, game, timestamp, playerSelectedAbility, interaction = None):
    abilities = [x for x in i.assignedRole.abilities if x.type == classes.enums.AbilityType.Night]
    data = None

    timeRemaining = 30 - timestamp
    roundedTimeRemaining = int(timeRemaining)

    playerSelectedAbility = int(playerSelectedAbility)

    if (i.isRoleBlocked):
        embed = disnake.Embed(title="**You were occupied!**", colour=disnake.Colour(0xffb6f0), description="**You ended up not performing your ability tonight.**")

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1009181021859749970/1009885085002104933/IMG_0038-removebg-preview.png")
        embed.set_footer(text="Use `/status` to learn what distraction does", icon_url=i.memberObj.display_avatar.url)
        await i.memberObj.send(embed=embed)
        return

    if (abilities[playerSelectedAbility].requiredTargets == 0):
        i.playerSelectedAbility = i.assignedRole.abilities.index(abilities[playerSelectedAbility])
    
        embed = disnake.Embed(title=f"**You decide to {abilities[playerSelectedAbility].flavorText} tonight**", colour=disnake.Colour(0xbbf6ff))

        embed.set_thumbnail(url=abilities[playerSelectedAbility].getIconUrl())
        embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=i.memberObj.display_avatar.url)
        
        if interaction:
            await interaction.response.send_message(embed=embed)
        else:
            await i.memberObj.send(embed=embed)

        if (abilities[playerSelectedAbility].charges > 0):
            abilities[playerSelectedAbility].charges -= 1
        return

    #Generate embed
    emb = disnake.Embed(title=f"**{i.assignedRole.name} {i.assignedRole.emoji} | <:moon:934556372421451776> {abilities[playerSelectedAbility].name}**", colour=disnake.Colour(i.assignedRole.color), description=f"**{i.assignedRole.emoji} {abilities[playerSelectedAbility].name} -** {abilities[playerSelectedAbility].description}").set_footer(text=f"You have {roundedTimeRemaining} seconds to make a descision", icon_url=i.memberObj.display_avatar.url).add_field(name="**Use the Dropdown below to react with a target!**", value="** **", inline=False)
    
    # Generate targetting list
    allowedPlayers = abilities[playerSelectedAbility].targetingOptions(i, game.playervar, game)
    
    class TargetingDropdown(disnake.ui.StringSelect):
        def __init__(self):
            options = []

            for x in allowedPlayers:
                x:classes.player.Player
                options.append(disnake.SelectOption(label=x.memberObj.name, description=f"Click to target {x.memberObj.name}", emoji=abilities[playerSelectedAbility].emoji, value=str(x.memberObj.id)))

            options.append(disnake.SelectOption(label="Do nothing", value="abstain", description="Do nothing tonight", emoji="❌"))

            super().__init__(placeholder="Select a player to target...", min_values=abilities[playerSelectedAbility].requiredTargets, max_values=abilities[playerSelectedAbility].requiredTargets, options=options)

        async def callback(self, interaction: MessageInteraction):
            selfPlayer:classes.player.Player = classes.player.Player.get(interaction.author.id, game)

            if ("abstain" in self.values): # If abstaining is any of the options just abstain
                embed = disnake.Embed(title=f"**You decide to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))
                embed.set_footer(text="You can change your action", icon_url=interaction.author.display_avatar.url)
                await interaction.response.send_message(embed=embed)
                selfPlayer.nightTargettedPlayers.clear()
            else:
                if len(self.values) > 1: # If there are more than 1 player selected, send a special embed
                    targets:list[classes.player.Player] = []
                    
                    for target in self.values:
                        targets.append(classes.player.Player.get(int(target), game))

                    selfPlayer.nightTargettedPlayers.clear()
                    selfPlayer.nightTargettedPlayers.append(targettedPlayer)

                    embed = disnake.Embed(title=f"**You decide to {abilities[playerSelectedAbility].flavorText} {len(targets)} players tonight**", colour=disnake.Colour(0xbbf6ff))

                    embed.set_thumbnail(url=targets[0].memberObj.display_avatar.url)
                    embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=interaction.author.display_avatar.url)

                    await interaction.response.send_message(embed=embed)
                else: # Else, do stuff normally
                    targettedPlayer:classes.player.Player = classes.player.Player.get(int(self.values[0]), game)

                    selfPlayer.nightTargettedPlayers.clear()
                    selfPlayer.nightTargettedPlayers.append(targettedPlayer)

                    embed = disnake.Embed(title=f"**You decide to {abilities[playerSelectedAbility].flavorText} {targettedPlayer.memberObj.name} tonight**", colour=disnake.Colour(0xbbf6ff))

                    embed.set_thumbnail(url=targettedPlayer.memberObj.display_avatar.url)
                    embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=interaction.author.display_avatar.url)

                    await interaction.response.send_message(embed=embed)


    class TargetingDropdownView(disnake.ui.View):
        def __init__(self) -> None:
            nonlocal data
            super().__init__(timeout=timeRemaining)
            data = self

            self.add_item(TargetingDropdown())

    if not interaction:
        msg = await i.memberObj.send(embed=emb, view=TargetingDropdownView())
    else:    
        msg = await interaction.response.send_message(embed=emb, view=TargetingDropdownView())

    await asyncio.sleep(timeRemaining)
        
    for child in data.children:
        child.disabled = True

    await msg.edit(view=data)

    if (len(i.nightTargettedPlayers) == 0):
        i.playerSelectedAbility = -1
        embed = disnake.Embed(title=f"**Your final decision is to do nothing tonight**", colour=disnake.Colour(0xbbf6ff))

        embed.set_thumbnail(url=i.memberObj.display_avatar.url)
        embed.set_footer(text="You can't change your decision anymore", icon_url=i.memberObj.display_avatar.url)
        await i.memberObj.send(embed=embed)
    else:    
        i.playerSelectedAbility = i.assignedRole.abilities.index(abilities[playerSelectedAbility])
        embed = disnake.Embed(title=f"**Your final decision is to {abilities[playerSelectedAbility].flavorText} {i.nightTargettedPlayers[0].memberObj.name} tonight**", colour=disnake.Colour(0xbbf6ff))

        embed.set_thumbnail(url=i.nightTargettedPlayers[0].memberObj.display_avatar.url)
        embed.set_footer(text=utils.chargeCount(abilities[playerSelectedAbility].charges), icon_url=i.memberObj.display_avatar.url)
        
        await i.memberObj.send(embed=embed)

        if (abilities[playerSelectedAbility].charges > 0):
            abilities[playerSelectedAbility].charges -= 1