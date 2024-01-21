from enum import Enum

class Role(Enum):
    Cop = "cop"
    Mafioso = "mafioso"
    Villager = "villager"
    Associate = "associate"
    Vigilante = "vigilante"
    Doctor = "doctor"
    Consort = "consort"
    Jester = "jester"
    Headhunter = "headhunter"

class Contractions(Enum):
    RandomTown = "Random Town"
    TownInvestigative = "Town Investigative"
    TownProtective = "Town Protective"
    RandomMafia = "Random Mafia"
    RandomNeutral = "Random Neutral"
    NeutralEvil = "Neutral Evil"

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
    Passive = 0
    Night = 1
    Dawn = 2
    Dusk = 3
    PassiveDawn = 4
    PassiveDusk = 5
    PassiveEarly = 5
    DayOne = 7
