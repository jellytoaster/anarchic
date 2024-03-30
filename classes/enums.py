from enum import Enum

class SetupDataType(Enum):
    Custom = "Custom Setup - "
    Preset = "Preset Setup - "
    AllAny = ""
    Imported = "Imported Setup - "

class Faction(Enum):
    Town = "town"
    Mafia = "mafia"
    Neutral = "neutral"

class DeathReason(Enum):
    Unknown = 0
    Mafia = 1
    Enforcer = 2
    Lynch = 3
    Plague = 4
    Jester = 5
    Headhunter = 6

class AbilityType(Enum):
    Passive = "passive"
    Night = "night"
    Dawn = 2
    Dusk = 3
    PassiveDawn = "passivedawn"
    PassiveDusk = "passivedusk"
    PassiveEarly = "passiveearly"
    DayOne = "passived1"
