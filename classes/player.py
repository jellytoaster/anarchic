from classes.game import Game
import classes.role
import disnake
import classes.enums
import copy

deathEmbeds = {classes.enums.DeathReason.Mafia : disnake.Embed(title="**You were attacked by a member of the Mafia**", colour=disnake.Colour(0xd0021b), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://cdn.discordapp.com/emojis/890328238029697044.png?size=80"),
               classes.enums.DeathReason.Jester : disnake.Embed(title="**You could not get over your guilt of lynching the Jester <:jesticon2:889968373612560394>**", colour=disnake.Colour(0xf1cbe2), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://cdn.discordapp.com/emojis/889968373612560394.webp?size=80"),
               classes.enums.DeathReason.Enforcer : disnake.Embed(title="**You were eliminated by a Vigilante**", colour=disnake.Colour(0x7ed321), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://cdn.discordapp.com/emojis/890339050865696798.webp?size=96&quality=lossless"),
               classes.enums.DeathReason.Lynch : disnake.Embed(title="You have been lynched by the Town", colour=disnake.Colour(0x9b9b9b), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://images-ext-1.discordapp.net/external/4P42Xlx0OwuRydI3QSE8l3eweFEqd_tlVJcdZF9ZO6I/%3Fwidth%3D805%26height%3D634/https/images-ext-2.discordapp.net/external/LlOBlIZEHHfRmfQn8_dhpUD6gN0CUWMecRcDZjd9CTs/%253Fwidth%253D890%2526height%253D701/https/media.discordapp.net/attachments/765738640554065962/877706810763657246/unknown.png?width=724&height=570"),
               classes.enums.DeathReason.Plague : disnake.Embed(title="**You were taken by the Plague**", colour=disnake.Colour(0xb8e986), description="**You have died <:rip:878415658885480468>**"),
               classes.enums.DeathReason.Unknown : disnake.Embed(title="You died to an unknown reason")}

class Player():
    
    def __init__(self, member, game:Game) -> None:
        self.memberObj:disnake.Member = member
        self.id = member.id
        self.assignedRole:classes.role.Role = None
        self.dead = False
        self.deathReason = classes.enums.DeathReason.Unknown
        self.defended = None
        self.isRoleBlocked = False
        self.isVoteBlocked = False
        self.nightTargettedPlayers = []
        self.wins = False
        self.deathRound = 0
        self.assignedGame = game
        self.playerSelectedAbility = -1
        self.votingPower = 1
        
        self.externalRoleData = {}
        game.playervar.append(self)

    def get(id:int, game:Game):
        for player in game.playervar:
            if player.id == id:
                return player
        return None

    def getPlayersWithRole(roleName:str, game:Game):
        """Case sensitive!"""
        return [i for i in game.playervar if i.assignedRole.name == roleName]
    
    def getPlayersWithFactions(faction:classes.enums.Faction, game:Game):
        return [i for i in game.playervar if i.assignedRole.faction == faction]

    # Kill player, True if successful and False otherwise.
    async def kill(self, deathReason:classes.enums.DeathReason, game:Game, force=False):
        if (self.defended == None or force == True):

            # Silence them for good by changing their role to dead
            await self.memberObj.remove_roles(game.rolePlayer)
            await self.memberObj.add_roles(game.roleDead)

            self.dead = True
            self.deathReason = deathReason
            await self.memberObj.send(embed=deathEmbeds[deathReason].set_footer(text="Rest in peace.", icon_url=self.memberObj.display_avatar.url))

            self.deathRound = copy.copy(game.currentRound)

            return True
        else:
            if self.defended[1]:
                embed = disnake.Embed(title="**Your target was attacked last night!**", colour=disnake.Colour(0x7ed321))
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/970492620788871168/BGIcon.png")
                embed.set_footer(text="Try whispering to your target", icon_url=self.defended.memberObj.display_avatar.url)
                await self.defended[0].memberObj.send(embed=embed)

            embed = disnake.Embed(title="**You were attacked, but someone protected you from harm!**", colour=disnake.Colour(0x7ed321))

            embed.set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/970492620788871168/BGIcon.png")
            embed.set_footer(text="Try coordinating with your protector... if they're still alive, that is.", icon_url=self.memberObj.display_avatar.url)
            await self.memberObj.send(embed=embed)


            return False
        
    def whoVisitedMe(self):
        """Who visited me! This returns the real results (not framer affected)"""
        return [i for i in self.assignedGame.playervar if self in i.nightTargettedPlayers]

