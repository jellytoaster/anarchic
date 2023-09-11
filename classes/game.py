import disnake
from classes import setupData


allGuildGames = {}


class Game():
    def __init__(self, guild:disnake.Guild) -> None:
        self.players:list(disnake.Member) = []
        self.hasStarted = False
        self.guild = guild
        allGuildGames[guild.id] = self
        self.setupData:setupData.SetupData = setupData.SetupData(self)

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
            

    def checkForGame(guild:disnake.Guild):
        if (Game.findGuildGame(guild.id) == None):
            return Game(guild)
        return (Game.findGuildGame(guild.id))