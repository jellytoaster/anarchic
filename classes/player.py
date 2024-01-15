from classes.game import Game
import classes.role
import disnake
import classes.enums

deathEmbeds = {classes.enums.DeathReason.Mafia : disnake.Embed(title="**You were attacked by a member of the Mafia**", colour=disnake.Colour(0xd0021b), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://cdn.discordapp.com/emojis/890328238029697044.png?size=80"),
               classes.enums.DeathReason.Enforcer : disnake.Embed(title="**You were eliminated by a Vigilante**", colour=disnake.Colour(0x7ed321), description="**You have died <:rip:878415658885480468>**").set_thumbnail(url="https://cdn.discordapp.com/emojis/890339050865696798.webp?size=96&quality=lossless"),
               classes.enums.DeathReason.Lynch : disnake.Embed(title="ur lycnhc", description="a"),
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
        self.isSuspicious = False
        self.nightTargettedPlayers = []
        self.wins = False


        game.playervar.append(self)

    def initPlayerVars(game:Game):
        for i in game.playervar:
            i.isSuspicious = i.assignedRole.suspiciousRole

    def get(id:int, game:Game):
        for i in game.playervar:
            i:Player
            if (i.id == id):
                return i
            
        return None
    
    # Kill player, True if successful and False otherwise.
    async def kill(self, deathReason:classes.enums.DeathReason, game:Game, force=False):
        if (self.defended == None or force == True):

            # Silence them for good by changing their role to dead
            self.memberObj.remove_roles(game.rolePlayer)
            self.memberObj.add_roles(game.roleDead)

            self.dead = True
            self.deathReason = deathReason
            await self.memberObj.send(embed=deathEmbeds[deathReason].set_footer(text="Rest in peace.", icon_url=self.memberObj.display_avatar.url))

            self.memberObj.remove_role()

            return True
        else:
            embed = disnake.Embed(title="**Your target was attacked last night!**", colour=disnake.Colour(0x7ed321))
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/970492620788871168/BGIcon.png")
            embed.set_footer(text="Try whispering to your target", icon_url=self.defended.memberObj.display_avatar.url)
            await self.defended.memberObj.send(embed=embed)

            embed = disnake.Embed(title="**You were attacked, but someone protected you from harm!**", colour=disnake.Colour(0x7ed321))

            embed.set_thumbnail(url="https://media.discordapp.net/attachments/765738640554065962/970492620788871168/BGIcon.png")
            embed.set_footer(text="Try coordinating with your protector... if they're still alive, that is.", icon_url=self.memberObj.display_avatar.url)
            await self.memberObj.send(embed=embed)


            return False