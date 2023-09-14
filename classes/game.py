if __name__ == "__main__":

    
    from classes import player

from classes import setupData
import classes.enums
import disnake

allGuildGames = {}


class Game():
    def __init__(self, guild:disnake.Guild) -> None:
        self.players:list(disnake.Member) = []
        self.playervar:list(player.Player) = []
        self.hasStarted = False
        self.guild = guild
        allGuildGames[guild.id] = self
        self.setupData:setupData.SetupData = setupData.SetupData(self)
        self.channelTownSquare = None
        self.channelStartChannel = None
        self.channelMafia = None
        self.channelGraveyard = None
        self.rolePlayer = None
        self.roleDead = None
        self.dayNum = 0
        self.finished = False
        self.daysWithoutDeath = 0

    def reset(self):
        self.playervar:list(player.Player) = []
        self.hasStarted = False
        self.channelTownSquare = None
        self.channelStartChannel = None
        self.channelGraveyard = None
        self.rolePlayer = None
        self.roleDead = None
        self.dayNum = 0
        self.finished = False
        self.daysWithoutDeath = 0


    def findGuildGame(id:int):
        for i in allGuildGames.keys():
            if (i == id):
                return allGuildGames[i]
            
        return None
    
    def findHostMention(self):
        try:
            return self.players[0].mention
        except:
            return "None"
        
    def isHost(self, user:disnake.Member):
        if (user == self.players[0]):
            return True
        return False

    def checkForGame(guild:disnake.Guild):
        if (Game.findGuildGame(guild.id) == None):
            return Game(guild)
        return (Game.findGuildGame(guild.id))
    
    def genPlayerList(self):
        return "\n".join([player.mention for player in self.players])
    
    def genAliveList(self):
        alivePlayers = [player.memberObj.mention for player in self.playervar if not player.dead]
        res = "\n".join(alivePlayers) if alivePlayers else ":x: **None**"
        return res
    
    def getAliveCount(self):
        return sum(1 for player in self.playervar if not player.dead)

    def getDeadCount(self):
        return sum(1 for player in self.playervar if player.dead)
    
    def genDeadList(self, withRoles=False):
        if (withRoles):
            deadPlayers = []
            for player in self.playervar:
                if (player.dead and player.deathReason != None):
                    deadPlayers.append(player.memberObj.mention + f" - **{player.assignedRole.name} {player.assignedRole.emoji} **")
                else:
                    deadPlayers.append(player.memberObj.mention + " - **???** ")

            res = "\n".join(deadPlayers) if deadPlayers else ":x: **None**"
            return res
        else:
            deadPlayers = [player.memberObj.mention for player in self.playervar if player.dead]
            res = "\n".join(deadPlayers) if deadPlayers else ":x: **None**"
            return res

        