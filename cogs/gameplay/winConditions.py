import disnake
import utils
import classes.player
import classes.game
import classes.enums

async def checkForWin(game:classes.game.Game):
    differentFactions = []

    for player in game.playervar:
        if player.assignedRole.faction not in differentFactions and player.dead == False:
            differentFactions.append(player.assignedRole.faction)


    if (len(differentFactions) <= 1):
        game.finished = True
        embed = disnake.Embed()

        if (len(differentFactions) == 0):
            # it's a draw since everyone die
            embed = disnake.Embed(title="**__Draw :crescent_moon:__**", colour=disnake.Colour(0xb0c9c9))
            embed.set_image(url="https://images-ext-2.discordapp.net/external/LlOBlIZEHHfRmfQn8_dhpUD6gN0CUWMecRcDZjd9CTs/%3Fwidth%3D890%26height%3D701/https/media.discordapp.net/attachments/765738640554065962/877706810763657246/unknown.png?width=805&height=634")
            
        elif (differentFactions[0] == classes.enums.Faction.Town):
            embed.title="**__<a:win:878421027703631894> The Town Wins <:town:1007768656341651547> <a:win:878421027703631894>!__**"
            embed.set_image(url="https://media.discordapp.net/attachments/765738640554065962/879065891751464960/unknown.png?width=560&height=701")
            embed.color = 0x7ed321

            # Make all townies win
            for x in game.playervar:
                if (x.assignedRole.faction == classes.enums.Faction.Town):
                    x.wins = True
        elif (differentFactions[0] == classes.enums.Faction.Mafia):
            embed.title="**__<a:win:878421027703631894> The Mafia Wins <:mafia:1007768566789050378> <a:win:878421027703631894>!__**"
            embed.set_image(url="https://images-ext-2.discordapp.net/external/8FKjo7N-8O9yztX8HF_1nF-PE-UxoWfsdQuzXcr4koo/%3Fwidth%3D744%26height%3D634/https/media.discordapp.net/attachments/765738640554065962/871849580533268480/unknown.png")
            embed.color = 0xd0021b  

            # Make all townies win
            for x in game.playervar:
                if (x.assignedRole.faction == classes.enums.Faction.Mafia):
                    x.wins = True
        
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%3Fwidth%3D468%26height%3D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?width=374&height=374")
        embed.set_footer(text="Use /end to finalize the game and /start to play a new one.", icon_url="https://cdn.discordapp.com/attachments/878437549721419787/883074983759347762/anarpfp.png")

        factionNames = {
            classes.enums.Faction.Town: "**__Town <:town:1007768656341651547>__**",
            classes.enums.Faction.Mafia: "**__Mafia <:mafia:1007768566789050378>__**",
            classes.enums.Faction.Neutral: "**__Neutral 🪓__**"
        }

        for faction, field_name in factionNames.items():
            message = ""
            for player in game.playervar:
                if player.assignedRole.faction != faction or player.id == 0:
                    continue

                emoji = "🏆" if player.wins else "❌"

                message += f" {emoji} "

                if player.dead:
                    message += "~~"

                message += f"**{player.assignedRole.name.capitalize()} {player.assignedRole.emoji}**"

                if player.dead:
                    message += "~~"

                message += f" - {player.memberObj.mention}\n"

            if message == "":
                message = "**:x: None**"

            embed.add_field(name=field_name, value=message, inline=False)
    
        await game.channelTownSquare.send(embed=embed)

        embed.set_footer(text="Use /end in the channel the game took place in.", icon_url="https://cdn.discordapp.com/attachments/878437549721419787/883074983759347762/anarpfp.png")
        await game.channelStartChannel.send(embed=embed)
            
        # Free all channels
        await utils.modifySendPermissions(game.channelTownSquare, game, dead=True, alive=True)
        await utils.modifyReadPermissoins(game.channelGraveyard, game, dead=True, alive=True)
        await utils.modifySendPermissions(game.channelGraveyard, game, dead=True, alive=True)
        await utils.modifyReadPermissoins(game.channelMafia, game, dead=True,alive=True)
        await utils.modifySendPermissions(game.channelMafia, game, dead=True,alive=True)