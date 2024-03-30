import classes.player
import classes.game
import classes.enums
import utils

class Ability:
    def __init__(self, function, targetingOptions, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="", usable=utils.notDead, type:classes.enums.AbilityType=classes.enums.AbilityType.Night, visible=True, requiredTargets = 1):
        self.invokeMethod = function
        self.charges= charges
        self.name = name
        self.emoji = emoji
        self.flavorText = flavorText
        self.description = description
        self.usableFunction = usable
        self.type = type
        self.targetingOptions = targetingOptions
        self.requiredTargets = requiredTargets
        self.visible = visible
    
    def getIconUrl(self):
        return f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64"

    async def invoke(self, targetPlayers:list, originPlayer:classes.player, game:classes.game.Game):
        await self.invokeMethod(targetPlayers, originPlayer, game)