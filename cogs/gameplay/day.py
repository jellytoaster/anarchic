import disnake
import utils
import classes.player
import classes.enums
import cogs.gameplay.night
import asyncio
import cogs.gameplay.winConditions
import classes.game
import classes.roles.jester

async def dayCycle(game:classes.game.Game):
    try:
        global isAccusation
        isAccusation = False
        game.dayNum += 1
        game.currentRound += 1

        deadPlayers = []
        for i in game.playervar:
            i:classes.player.Player
            if (i.dead and i.deathReason != None):
                game.daysWithoutDeath = 0
                deadPlayers.append(i)

        if (deadPlayers == []):
            game.daysWithoutDeath += 1

        if (game.daysWithoutDeath == 3):
            for i in game.playervar:
                await i.kill(classes.enums.DeathReason.Plague, game, True)

        await utils.mafiaModifySend(game.channelMafia, game, False)

        embed = disnake.Embed(title=f"It Is Day {game.dayNum} ☀️", color=disnake.Colour((0x7ed321)))
        
        # the website the day image was hosted on is ded 
        # embed.set_image(url="https://media.discordapp.net/attachments/765738640554065962/886652670230790214/unknown.png?ex=6612cca5&is=660057a5&hm=ee4302bd529d66529a8c97b2f6203b95a357afd486def2e0de485b5d4a704405&=&format=webp&quality=lossless&width=196&height=200")
        embed.set_footer(text="Talk, Bait, Claim.")

        #player and dead fields

        embed.add_field(name="Alive: `{}`".format(str(game.getAliveCount())), value=game.genAliveList())
        embed.add_field(name="Dead: `{}`".format(str(game.getDeadCount())), value=game.genDeadList())

        await game.channelTownSquare.send(embed=embed)

        # Show new deaths.

        embed = disnake.Embed(title=f"**Night {game.dayNum - 1} | Deaths <:rip:1125518025945268316>**", colour=disnake.Colour(0xafafaf))
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1003792593617952838.webp?size=96&quality=lossless")


        for i in game.playervar:
            i:classes.player.Player
            if (i.dead and i.deathReason != None and i.deathReason != classes.enums.DeathReason.Lynch):
                reason = utils.reasonToText(i.deathReason, f"**{i.memberObj.name}** ") + " "
                roleReveal = f"Their role was **{i.assignedRole.name}** {i.assignedRole.emoji}"
                embed.add_field(name=f"{reason}", value=f"{roleReveal}\n", inline=False)

                i.deathReason = None

        if (embed.fields == None or len(embed.fields) == 0):
            embed.add_field(name="It seemed to have been a peaceful night", value = "** **",inline=False)

        await game.channelTownSquare.send(embed=embed)

        await asyncio.sleep(2)

        await cogs.gameplay.winConditions.checkForWin(game)
        if (game.finished):
            return
        
        # check for a plague
        if (game.daysWithoutDeath == 2):
            embed = disnake.Embed(title="A plague has swept the town!", colour=disnake.Colour(0xb8e986), description="If no player **dies** by the next day, the **Plague** will **kill** everyone in the Town")

            embed.set_footer(text="Good Luck")
            await game.channelTownSquare.send(embed=embed)
            await asyncio.sleep(2)

        embed = disnake.Embed(title=f"`Day {str(game.dayNum)} ☀️ | Dawn Phase`", colour=disnake.Colour(0xbbf6ff), description="The sun is shining as another beautiful day begins\n```json\nDawn ends in 20 seconds```")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1008839043192213686.webp?size=96&quality=lossless")

        await game.channelTownSquare.send(embed=embed)

        await utils.modifySendPermissions(game.channelTownSquare, game, dead=False, alive=True)

        # perform dawn passives
        for i in game.playervar:
            for x in i.assignedRole.abilities:
                if (x.type == classes.enums.AbilityType.PassiveDawn):
                    if (x.usableFunction(i, game) and utils.chargeUsable(x.charges)):
                        x.charges -= 1
                        await x.invokeMethod(x.targetingOptions(i, game.playervar, game), i, game)

        await asyncio.sleep(20)

        await asyncio.create_task(votingCycle(game))
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)

    isAccusation = False

async def votingCycle(game:classes.game.Game):
    try:
        # Setup voting variables
        condition = int(game.getAliveCount() / 2 + 1)
        statusMsg = None
        votingData = {}
        for i in game.playervar:
            votingData[i] = []

        game.votedInnocent = []
        game.votedGuilty = []



        embed = disnake.Embed(title=f"`Day {str(game.dayNum)} ☀️ | Noon Phase`", colour=disnake.Colour(0xbbf6ff), description="The sun rises to it's peak\n```json\nNoon ends in 90 seconds```")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1008839043192213686.webp?size=96&quality=lossless")

        await game.channelTownSquare.send(embed=embed)

        options = []
        for i in game.playervar:
            if (i.dead):
                continue

            options.append(disnake.SelectOption(label=f"{i.memberObj.name}", description=f"Click here to vote against {i.memberObj.name}", value = str(i.id), emoji="🗳️"))

        options.append(disnake.SelectOption(label=f"Cancel", description=f"Cancel your current vote", emoji="❌"))

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        class VotingDropdown(disnake.ui.Select):
            def __init__(self, opt:list):
                super().__init__(
                    placeholder="Vote someone...",
                    options = opt    
                )

            async def callback(self, interaction:disnake.MessageInteraction):
                nonlocal votingData
                if interaction.author not in game.players:
                    await interaction.response.send_message("You're not even in the game :skull:", ephemeral=True)
                    return
                selfPlayer = classes.player.Player.get(interaction.author.id, game)

                if (selfPlayer.dead == True):
                    await interaction.response.send_message("You cannot vote while dead <:xvote:1009959214837415966>", ephemeral=True)
                    return
                if (selfPlayer.isVoteBlocked == True):
                    await interaction.response.send_message("You have been voteblocked! You are unable to vote for today.", ephemeral=True)
                    return
            
                if (self.values[0] == "Cancel"):
                    await interaction.response.send_message(f"**__{interaction.author.name}__** has unvoted")
                    for k, v in votingData.items():
                        if (interaction.author.id in v):
                            votingData[k].remove(selfPlayer)
                        
                    await updateStatusMsg(game, votingData, condition)
                    return
                
                targetPlayer = classes.player.Player.get(int(self.values[0]), game)
                
                votingData[targetPlayer].append(selfPlayer)
                
                def calculateVotes(votes):
                    res = 0
                    for i in votes:
                        res += i.votingPower

                    return res

                await interaction.response.send_message(content=f"**__{interaction.author.name}__ <:vote:1009960345428820059>** has voted against **__{targetPlayer.memberObj.name}__ ({str(calculateVotes(votingData[targetPlayer]))}/{str(condition)})**")
                await updateStatusMsg(game, votingData, condition)
                
                if (calculateVotes(votingData[targetPlayer]) >= condition):
                    global isAccusation
                    isAccusation = True
                    await enterAccusation(game, targetPlayer, votingMsg, view)
                

        class DropdownView(disnake.ui.View):
            def __init__(self):
                super().__init__()
                
                self.add_item(VotingDropdown(options))

        async def updateStatusMsg(game, votingData, condition):
            nonlocal statusMsg
            currentlynch = await utils.getCurrentLynch(votingData, game)
            embed = disnake.Embed(title=f"**Day {game.dayNum} | Required votes for Majority: __{str(condition)}__**", colour=disnake.Colour(0x60a8f9), description=f"Current lynch: {currentlynch}")

            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1010903922916991006.webp?size=96&quality=lossless")
            embed.set_footer(text="Noon ends in 90 seconds")

            for player in game.playervar:
                if player.dead:
                    continue

                voterString = ""
                for i in votingData[player]:
                    voterString += i.memberObj.mention
                
                embed.add_field(name=f"**{len(votingData[player])} - {player.memberObj.name}**", value="`Voters:` " + voterString, inline=False)

            if statusMsg == None:
                statusMsg = await game.channelTownSquare.send(embed=embed)
                await statusMsg.pin()
            else:
                await statusMsg.edit(embed=embed)
        
        embed = disnake.Embed(title=f"**{str(int(game.getAliveCount() / 2 + 1))} votes are needed to send someone to trial <:trial:1010903922916991006>**", colour=disnake.Colour(0xf5a623))

        embed.set_image(url="https://cdn.discordapp.com/attachments/765738640554065962/913554920416874506/IMG_0097.png")
        embed.set_footer(text="Use the dropdown to vote.")


        view = DropdownView()
        votingMsg = await game.channelTownSquare.send(embed=embed, view=view)
        await updateStatusMsg(game, votingData, condition)

        await asyncio.sleep(90)
        if (isAccusation):
            return
        else:
            await asyncio.create_task(cogs.gameplay.night.nightCycle(game))
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)

async def enterAccusation(game:classes.game.Game, targetPlayer:classes.player.Player, votingMsg, votingMsgView):
    try:
        for i in votingMsgView.children:
            i.disabled = True
        await votingMsg.edit(view=votingMsgView)

        game.accusedPlayer = targetPlayer

        embed = disnake.Embed(title=f"**{targetPlayer.memberObj.name} is on trial <:trial:1010903922916991006>**", colour=disnake.Colour(0xbbf6ff), description="What is your defense?")

        embed.set_thumbnail(url=targetPlayer.memberObj.display_avatar.url)
        embed.set_footer(text="You have 20 seconds to defend yourself")

        await game.channelTownSquare.send(embed=embed)


        await asyncio.sleep(20)

        embed = disnake.Embed(title=f"**It is time to decide on {targetPlayer.memberObj.name}'s fate**", colour=disnake.Colour(0xbbf6ff), description="You may choose to **Guilty \✅** or **Pardon \❌** the player on stand.")

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1010903922916991006.webp?size=44&quality=lossless")
        embed.set_footer(text="You have 20 seconds to vote", icon_url=targetPlayer.memberObj.display_avatar.url)

        game.votedInnocent = []
        game.votedGuilty = []

        class Fatedecider(disnake.ui.View):
            def __init__(self):
                super().__init__()

            @disnake.ui.button(label="Guilty", style=disnake.ButtonStyle.green, emoji="<:lynch:1010226047456915547>")
            async def guilty(self, button, inter):
                if inter.author not in game.players:
                    await inter.response.send_message("You're not even in the game :skull:", ephemeral=True)
                    return
                selfPlayer = classes.player.Player.get(inter.author.id, game)
                if (selfPlayer.dead):
                    await inter.response.send_message("You cannot vote while dead!", ephemeral=True)
                    return
                if (selfPlayer.id == targetPlayer.id):
                    await inter.response.send_message("You can't vote on your own trial!", ephemeral=True)
                    return
                if (inter.author.id in game.votedInnocent):
                    game.votedInnocent.remove(selfPlayer)

                if (inter.author.id not in game.votedGuilty):
                    game.votedGuilty.append(selfPlayer)
                else:
                    await inter.response.send_message("nah", ephemeral=True)
                    return

                await inter.response.send_message(content=f"You have __**Guiltied**__ <:vote:1009960345428820059> {targetPlayer.memberObj.name} ", ephemeral=True)
                await game.channelTownSquare.send(f"**__{selfPlayer.memberObj.name}__ <:vote:1009960345428820059>** has voted")

            @disnake.ui.button(label="Pardon", style=disnake.ButtonStyle.red, emoji="<:inno:873636640227205160>")
            async def inno(self, button, inter):
                if inter.author not in game.players:
                    await inter.response.send_message("You're not even in the game :skull:", ephemeral=True)
                    return
                selfPlayer = classes.player.Player.get(inter.author.id, game)
                if (selfPlayer.dead):
                    await inter.response.send_message("You cannot vote while dead!", ephemeral=True)
                    return
                if (selfPlayer.id == targetPlayer.id):
                    await inter.response.send_message("You can't vote on your own trial!", ephemeral=True)
                    return
                if (inter.author.id in game.votedGuilty):
                    game.votedGuilty.remove(selfPlayer)
                    
                if (inter.author.id not in game.votedInnocent):
                    game.votedInnocent.append(selfPlayer)
                else:
                    await inter.response.send_message("nah", ephemeral=True)
                    return

                await inter.response.send_message(content=f"You have marked {targetPlayer.memberObj.name} as __**Innocent**__ <:xvote:1009959214837415966>", ephemeral=True)
                await game.channelTownSquare.send(f"**__{selfPlayer.memberObj.name}__ <:vote:1009960345428820059>** has voted")

        msg = await game.channelTownSquare.send(embed=embed, view=Fatedecider())

        class DisableFate(disnake.ui.View):
            def __init__(self):
                super().__init__()

            @disnake.ui.button(label="Guilty", style=disnake.ButtonStyle.green, disabled = True)
            async def guilty(self, button, inter):
                pass

            @disnake.ui.button(label="Pardon", style=disnake.ButtonStyle.red, disabled = True)
            async def inno(self, button, inter):
                pass

        


        await asyncio.sleep(20)
        await msg.edit(view=DisableFate())

        embed = None
        await utils.modifySendPermissions(game.channelTownSquare, game, dead=False, alive=False)

        # Calculate Results
        winner = -1 # -1 for no data yet
        if (len(game.votedGuilty) > len(game.votedInnocent)):
            winner = 1 # 1 for lynch
        elif (len(game.votedGuilty) <= len(game.votedInnocent)):
            winner = 2 # 2 for innocent
        else:
            winner = 2 # 0 for ties

        if (winner == 1):
            embed = disnake.Embed(title="**Trial Results**", colour=disnake.Colour(0xff6363), description=f"The Town has decided to lynch **{targetPlayer.memberObj.name}** on a vote of **__{len(game.votedGuilty)}__** - **__{len(game.votedInnocent)}__**")
        if (winner == 2):
            embed = disnake.Embed(title="**Trial Results**", colour=disnake.Colour(0xa3ffc2), description=f"The Town has decided to pardon **{targetPlayer.memberObj.name}** on a vote of **__{len(game.votedGuilty)}__** - **__{len(game.votedInnocent)}__**")

        embed = utils.createVotingResults(embed, game, game.votedGuilty, game.votedInnocent)
        
        await game.channelTownSquare.send(embed=embed)

        if (winner == 1):
            await asyncio.sleep(3)
            targetPlayer:classes.player.Player
            await targetPlayer.kill(classes.enums.DeathReason.Lynch, game, True)

            embed = disnake.Embed(title=f"{targetPlayer.memberObj.name}'s role", colour=disnake.Colour(0xff6363), description=f"Their role was **{targetPlayer.assignedRole.name}** {targetPlayer.assignedRole.emoji}")

            embed.set_image(url="https://images-ext-1.discordapp.net/external/4P42Xlx0OwuRydI3QSE8l3eweFEqd_tlVJcdZF9ZO6I/%3Fwidth%3D805%26height%3D634/https/images-ext-2.discordapp.net/external/LlOBlIZEHHfRmfQn8_dhpUD6gN0CUWMecRcDZjd9CTs/%253Fwidth%253D890%2526height%253D701/https/media.discordapp.net/attachments/765738640554065962/877706810763657246/unknown.png?width=724&height=570")
            embed.set_footer(text="Rest in Peace")
            await game.channelTownSquare.send(embed=embed)
            await asyncio.sleep(3)
            if (targetPlayer.assignedRole.name.lower() == "jester"):
                embed = disnake.Embed(title="**The Jester has been lynched**", colour=disnake.Colour(0xffc3e7), description=f"All players who voted **Guilty** will be occupied the following **Night <:moon:934556372421451776>**. In addition, a player who voted **Guilty** will be haunted by the **Jester {targetPlayer.assignedRole.emoji}**")

                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/889968373612560394.webp?size=96&quality=lossless")
                embed.set_footer(text="The Jester always get their revenge")
                await game.channelTownSquare.send(embed=embed)
                targetPlayer.wins = True
                await asyncio.sleep(2)
            for i in classes.player.Player.getPlayersWithRole("headhunter", game):
                if (i.externalRoleData["target"] == targetPlayer):
                    i.externalRoleData["points"] += 1
                    i.externalRoleData["target"] = None

                    if (i.externalRoleData["points"] == 2):
                        i.wins = True


        else:
            await asyncio.sleep(5)

        await asyncio.create_task(cogs.gameplay.night.nightCycle(game))
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)