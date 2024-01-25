import classes.player
import classes.game
import classes.enums
import utils

class Ability:
    def __init__(self, function, targetingOptions, charges:int, name:str, description:str, emoji:str, flavorText:str, usable=utils.notDead, type:classes.enums.AbilityType=classes.enums.AbilityType.Night):
        self.invokeMethod = function
        self.charges= charges
        self.name = name
        self.emoji = emoji
        self.flavorText = flavorText
        self.description = description
        self.usableFunction = usable
        self.type = type
        self.targetingOptions = targetingOptions

    async def invoke(self, targetPlayers:list, originPlayer:classes.player, game:classes.game.Game):
        await self.invokeMethod(targetPlayers, originPlayer, game)