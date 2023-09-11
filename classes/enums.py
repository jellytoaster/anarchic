from enum import Enum

class Role(Enum):
    Cop = "cop"
    Mafioso = "mafioso"
    Villager = "villager"
    Associate = "associate"
    Vigilante = "vigilante"
    Doctor = "doctor"
    Consort = "consort"

class Contractions(Enum):
    RandomTown = "Random Town"
    TownInvestigative = "Town Investigative"
    TownProtective = "Town Protective"
    RandomMafia = "Random Mafia"

class SetupDataType(Enum):
    Custom = 0
    Preset = 1
    AllAny = 2

class Faction(Enum):
    Town = "town"
    Mafia = "mafia"
    Neutral = "neutral"

class DeathReason(Enum):
    Unknown = 0
    Mafia = 1
    Enforcer = 2
    Lynch = 3
