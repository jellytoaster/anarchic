from classes import setupData
import classes.enums
import disnake

allGuildGames = {}


class Game():
    def __init__(self, guild:disnake.Guild) -> None:
        from classes.player import Player
        self.players:list[disnake.Member] = []
        self.playervar:list[Player] = []
        self.hasStarted:bool= False
        self.guild:disnake.Guild = guild

        self.setupData:setupData.SetupData = setupData.SetupData(self)
        self.channelTownSquare:disnake.TextChannel = None
        self.channelStartChannel:disnake.TextChannel = None
        self.channelMafia:disnake.TextChannel = None
        self.channelGraveyard:disnake.TextChannel = None
        self.rolePlayer:disnake.Role = None
        self.roleDead:disnake.Role = None
        self.dayNum:int = 0
        self.finished:bool = False
        self.daysWithoutDeath:int = 0
        self.accusedPlayer:Player = None
        self.votedInnocent:list[Player] = []
        self.votedGuilty:list[Player] = []
        self.headStart:bool = False
        self.currentRound:int = 0
        self.mafNightKill:list[Player] = []

        allGuildGames[guild.id] = self

    def reset(self):
        from classes.player import Player
        self.playervar:list[Player] = []
        self.hasStarted = False
        self.channelTownSquare = None
        self.channelStartChannel = None
        self.channelGraveyard = None
        self.rolePlayer = None
        self.roleDead = None
        self.dayNum = 0
        self.headStart = False
        self.finished = False
        self.daysWithoutDeath = 0
        self.accusedPlayer = None
        self.votedInnocent = []
        self.votedGuilty = []
        self.currentRound = 0
        self.mafNightKill = []


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

        