import classes.enums
import classes.enums
import utils
from typing import Callable

class Ability:
    import classes.player
    import classes.game


    def __init__(self, function, targetingOptions, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="", usable=utils.imNotDead, type:classes.enums.AbilityType=classes.enums.AbilityType.Night,  visible=True,requiredTargets = 1):
        self.invokeMethod = function
        self.charges= charges
        self.name = name
        self.emoji = emoji
        self.flavorText = flavorText
        self.description = description
        self.type = type
        self.usableMethod = usable
        self.targetingOptions = targetingOptions
        self.requiredTargets = requiredTargets
        self.visible = visible

    def usableFunction(self, player, game) -> bool:
        # If ability does not have enough players to target, the ability is unusable to prevent hardlock on targeting screen
        if len(self.targetingOptions(player, game.playervar, game)) < self.requiredTargets:
            return False 
        
        return self.usableMethod(player, game)

    def fromMetadata(metadata:dict, function:Callable):
        if hasattr(function, "_metadata_visible"):
            return Ability(function, metadata["targetingOptions"], metadata["charges"], metadata["name"], metadata["description"], metadata["emoji"], metadata["flavorText"], metadata["usable"], metadata["type"], False, metadata["requiredTargets"])
        return Ability(function, metadata["targetingOptions"], metadata["charges"], metadata["name"], metadata["description"], metadata["emoji"], metadata["flavorText"], metadata["usable"], metadata["type"], True, metadata["requiredTargets"])

    def getIconUrl(self) -> str:
        return f"https://cdn.discordapp.com/emojis/{self.emoji.split(':')[2].replace('>', '')}.webp?format=webp&width=76&height=64"

    async def invoke(self, targetPlayers:list, originPlayer:classes.player, game:classes.game.Game):
        await self.invokeMethod(targetPlayers, originPlayer, game)

def invisible(func:Callable):#
    """When this decorator is applied on an ability decorator, it will be invisible from the abilities you can select in game.
    """
    
    def decorator(func:Callable):
        func._metadata_visible = False
        return func

    return decorator

def earlynight_passive_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a early night passive `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.PassiveEarly,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def passivedusk_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead, requiredTargets = 1):
    """A decorator to define a passive dusk `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.PassiveDusk,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def passivedawn_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a passive dawn `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.PassiveDawn,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def passive_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a passive night `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.Passive,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def day1_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a `Ability` that only runs on the first day which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.DayOne,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def dusk_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a dusk `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.Dusk,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def dawn_ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a dawn `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.Dawn,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator

def ability(targetingOptions:Callable=utils.notMeAndNotDead, charges:int=-1, name:str="Ability", description:str="An ability description.", emoji:str="", flavorText:str="target", usable=utils.imNotDead,  requiredTargets = 1):
    """A decorator to define a night `Ability` which gets automatically added to a `Role` if defined in a file with a `Role` subclass.

    Parameters
    ----------
    targetingOptions: function
        The function to determine the players the ability is allowed to target. This should return a list of `Player`. There are targeting options used in Anarchic in `utils`.

    charges: int
        The amount of charges (times this ability can be used) applied to the ability. `-1` means unlimited charges. Defaults to `-1`.

    name: str
        The name of the ability.

    description: str
        The description of the ability.

    emoji: str
        The emoji of the ability. To forgo an emoji, use an empty string `\"\"`.

    flavorText: str
        The flavor text of the ability. They will be used like this: 
        `You will {flavorText} John tonight`,
        `Who would you like to {flavorText}?` Defaults to `\"target\"`.
    
    usable:function
        The function to determine when the ability is usable. Defaults to `utils.notDead`.

    type: classes.enums.Faction
        Determines when the ability can be used (Dawn, Dusk, Night). Defaults to `Night`.
    
    visible: bool
        Determines if this ability is visible in the target selector. For example, Shadow Syndicate uses this property to hide this ability from being used since it does nothing.

    requiredTargets: int
        How many targets the ability requires. If there are not enough targettable players, this ability cannot be used.
    """
    
    def decorator(func:Callable):
        func._metadata = {
            "targetingOptions" : targetingOptions,
            "charges" : charges,
            "name": name,
            "description" : description,
            "emoji": emoji,
            "flavorText" : flavorText,
            "usable" : usable,
            "type" : classes.enums.AbilityType.Night,
            
            "requiredTargets" : requiredTargets,
            "function" : func
        }
        return func

    return decorator