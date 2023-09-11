from enum import Enum

class Role(Enum):
    Cop = "cop"
    Mafioso = "mafioso"

class SetupDataType(Enum):
    Custom = 1
    Preset = 2
    AllAny = 3