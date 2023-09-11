import classes.player
import classes.game
import utils

class Ability:
    def __init__(self, function, charges:int, name:str, description:str, emoji:str, flavorText:str, usable=utils.true):
        self.invokeMethod = function
        self.charges= charges
        self.name = name
        self.emoji = emoji
        self.flavorText = flavorText
        self.description = description
        self.usableFunction = usable

    async def invoke(self, targetPlayers:list, originPlayer:classes.player, game:classes.game.Game):
        await self.invokeMethod(targetPlayers, originPlayer, game)