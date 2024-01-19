import disnake
import classes.errorhandler
import random
import utils
import classes.game
import cogs.gameplay.night
import asyncio
import disnake.ext.commands.errors as error
import copy
import classes.enums
from classes import player, role
from cogs import setupManagement
from disnake.ext import commands
import classes.enums
import classes.role

def assignRoles(game:classes.game.Game):
    roles = copy.deepcopy(game.setupData.roles)
    for i in game.players:
        newPlayer = player.Player(i, game)

        selection:str = random.choice(roles)

        if (utils.isContraction(selection)):
            if "random" in selection.lower():
                # Just any role that follows the faction
                # Pick a role that fits the faction
                randomList = []
                for i in classes.role.Role.allRoles:
                    i:classes.role.Role
                    if (selection.split()[1].lower() == i.faction.value):
                        randomList.append(i.name)

                finalSelection = random.choice(randomList)
            else:
                # Category, e.g Mafia Killing <-- killing role and is mafia
                randomList = []
                for i in classes.role.Role.allRoles:
                    i:classes.role.Role
                    if (selection.split()[0].lower() == i.faction.value.lower() and selection.split()[1].lower() == i.type.lower()):
                        randomList.append(i.name)

                finalSelection = random.choice(randomList)
        else:
            finalSelection = selection

        newPlayer.assignedRole = copy.deepcopy(role.Role.toRole(finalSelection))
        roles.remove(selection)
       
async def sendRoles(game:classes.game.Game):
    for i in game.players:
        await i.send(embed=player.Player.get(i.id, game).assignedRole.roleEmbed)


async def genChannels(game:classes.game.Game):
    guild = game.guild
    category = await guild.create_category("Anarchic")
    townsquare = game.channelTownSquare = await guild.create_text_channel("town-square", category=category)
    graveyard = game.channelGraveyard = await guild.create_text_channel("graveyard", category=category)
    mafiacontacts = game.channelMafia = await guild.create_text_channel("mafia-contacts", category=category)

    game.rolePlayer = await utils.createRoleIfNotExist(game.guild, "[Anarchic] Player")
    game.roleDead = await utils.createRoleIfNotExist(game.guild, "[Anarchic] Dead")

    for i in game.guild.members:
        if (game.rolePlayer in i.roles):
            await i.remove_roles(game.rolePlayer)

    for i in game.players:
        i:disnake.Member
        await i.add_roles(game.rolePlayer)

    # Modify send permissions for channels
    await utils.modifySendPermissions(townsquare, game, dead=False,alive=False)
    await utils.modifySendPermissions(mafiacontacts, game, dead=False,alive=True)

    # Modify read permissions for channels
    await utils.modifyReadPermissions(townsquare, game, dead=True,alive=True)
    await utils.modifyReadPermissions(graveyard, game, dead=True,alive=False)

    await utils.makePrivate(townsquare)
    await utils.makePrivate(graveyard)
    await utils.makePrivate(mafiacontacts)



    embed = disnake.Embed(title="**Welcome to Anarchic.**", colour=disnake.Colour(0x6efff3), description="Anarchic is game of deceit and deception, based off of the Mafia Party game. To learn how to play, check below.")

    embed.set_image(url="https://cdn.discordapp.com/attachments/878437549721419787/882712063904976926/welcome.png")
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%3Fwidth%3D468%26height%3D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?width=374&height=374")
    embed.set_footer(text="Good luck.")

    embed.add_field(name="**How to Play💡**", value="Each player is secretly assigned a role at the start of the game and has to fulfill their goal. To see the list of roles, try typing `/roles`. The game alternates between a day and night cycle. For more infomation, use `/howtoplay`.", inline=False)
    embed.add_field(name="**Rules :pushpin:**", value="Here are a list of rules to follow.", inline=False)
    embed.add_field(name="**No Screenshoting :camera_with_flash:**", value="Screenshoting is strictly forbidden, as it is cheeating ruins the game for everyone.", inline=False)
    embed.add_field(name="**No Copy And Pasting :pencil:**", value="Copy and pasting is also considered breaking the rules, as it is also cheating.", inline=False)
    embed.add_field(name="No Direct Messaging 💬", value="Direct Messaging is not allowed as it ruins many game mechanics. ",inline=False)
    embed.add_field(name="Names Policy :man_gesturing_no:", value="Names must be set to a typeable english name, for players to be able to select you.",inline=False)

    await townsquare.send(embed=embed)

    embed = disnake.Embed(title="**Welcome to the Graveyard <:rip:872284978354978867>!**", colour=disnake.Colour(0x300036), description="This is a place for dead players to talk, discuss and complain about the living.")

    embed.set_image(url="https://cdn.discordapp.com/attachments/878437549721419787/883854521753813022/unknown.png")
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/EedL1z9T7uNxVlYBIUQzc_rvdcYeTJpDC_4fm7TQZBo/%3Fwidth%3D468%26height%3D468/https/media.discordapp.net/attachments/765738640554065962/893661449216491540/Anarchic.png?width=374&height=374")

    embed.add_field(name="**Rules :pushpin:**", value="Here are some guidelines to follow.", inline=False)
    embed.add_field(name="No Dead Info :newspaper2:.", value="Do not give dead info. Once you're dead, you're dead. You may only talk about the game here.", inline=False)
    embed.add_field(name="Only Preview :eyes:", value="Specators are not allowed to interact in any way with the living .", inline=False)

    await graveyard.send(embed=embed)



async def prep(game:classes.game.Game):
    try:
        assignRoles(game)
        await asyncio.sleep(2)
        await genChannels(game)
        
        await sendRoles(game)
        player.Player.initPlayerVars(game)
    except Exception as e:
        await classes.errorhandler.handle(game.channelTownSquare, e)
        await utils.finishGame(game)

async def start(game:classes.game.Game):
    game.dayNum += 1

    mafiaMembers = []

    # Lock mafia contacts for mafia playres first
    for i in game.playervar:
        if (i.assignedRole.faction == classes.enums.Faction.Mafia):
            mafiaMembers.append(i)
            await game.channelMafia.set_permissions(i.memberObj, read_messages=True, send_messages=True, read_message_history=True)
        else:
            await game.channelMafia.set_permissions(i.memberObj, read_messages=False, send_messages=False, read_message_history=False)
    

    embed:disnake.Embed = disnake.Embed(title="**__Your Mafia Team this game__ <:mafia:1007768566789050378>**", colour=disnake.Colour(0xd0021b))

    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/890328238029697044.png?size=80")
    embed.set_footer(text="Good luck.", icon_url="https://cdn.discordapp.com/attachments/878437549721419787/883074983759347762/anarpfp.png")

    for i in mafiaMembers:
        embed.add_field(name=f"**{i.assignedRole.name} {i.assignedRole.emoji}**", value=f"{i.memberObj.mention}", inline=False)

    message = " ".join(member.memberObj.mention for member in mafiaMembers)

    await game.channelMafia.send(embed=embed, content=message)

    embed = disnake.Embed(title="It Is Day 1 ☀️", color=disnake.Colour((0x7ed321)))
    
    embed.set_image(url="https://images-ext-2.discordapp.net/external/8cFuWNzv5vDa4TbO68gg5Up4DSxguodCGurCAtDpWgU/%3Fwidth%3D936%26height%3D701/https/media.discordapp.net/attachments/765738640554065962/878068703672016968/unknown.png")
    embed.set_footer(text="Talk, Bait, Claim.")

    if (game.finished == True):
        return

    #player and setup fields

    embed.add_field(name="Players: `{}`".format(len(game.players)), value=game.genPlayerList())
    embed.add_field(name="Setup:", value=game.setupData.generateSetupList())
    await game.channelTownSquare.send(embed=embed)
    await utils.modifySendPermissions(game.channelTownSquare, game, alive=True, dead=False)

    # Activate day one abilities
    for i in game.playervar:
        for x in i.abilities:
            if x.type == classes.enums.AbilityType.DayOne and x.usableFunction(i, game) and utils.chargeUsable(x.charges):
                x.invokeMethod(x.targetingOptions(i, game.playervar), i, game)
                x.charges -= 1

    await asyncio.sleep(15)
    await asyncio.create_task(cogs.gameplay.night.nightCycle(game))