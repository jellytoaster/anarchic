from classes import enums
import string
import utils

presetSetups = {
    "pi e7" : ("πe7 :1234:", ["cop", "doctor", "villager", "villager", "villager", "consort", "mafioso"]), "generic" : ("generic :skull:",  ["cop", "doctor", "villager", "villager", "mafioso"])
}

class SetupData():
    def __init__(self, game) -> None:
        self.roles = []
        self.game = game
        self.name = ""
        self.type = enums.SetupDataType.Custom
        self.presetIndex = 0

    def addRole(self, role:enums.Role, amount:int, changeToCustom:bool=True):
        if (changeToCustom):
            self.type = enums.SetupDataType.Custom
        for _ in range(amount):
            self.roles.append(role)

    def removeRole(self, role:enums.Role, amount:int, changeToCustom:bool=True):
        # 1: Role not in list
        # 2: amount higher than roles in list
        
        if (role not in self.roles):
            return 1
        
        if (changeToCustom):
           self.type = enums.SetupDataType.Custom
        for _ in range(amount):
            try:
                self.roles.remove(role)
            except:
                return 2
        
        return 0
    
    def clear(self):
        self.roles = []

    def generateSetupList(self):
        result = "\n".join(map(lambda x: f"**{string.capwords(x)} {utils.roleEmoji(x.replace('contraction','').replace(' ', '').lower())}**", self.roles))
        if (result == ""):
            return ":x: **None**"
        return result
    
    def getPresetSetup(name:str):
        for key, value in presetSetups.items():
            if (key == name):
                return (key, value)
        return
    
    def generateSetupName(self):
        if (self.roles == []):
            return "Empty"
        elif (self.type == enums.SetupDataType.Custom):
            return f"__Custom :triangular_flag_on_post: ({len(self.roles)}P)__"
        elif (self.type == enums.SetupDataType.Preset):
            return f"__{SetupData.getPresetSetup(self.presetIndex)[1][0]} ({len(self.roles)}P)__"
        elif (self.type == enums.SetupDataType.AllAny):
            return f"__All Any :game_die: ({len(self.roles)}P)__"

    def generateSetupNameWithoutNumbers(self):
        if (self.roles == []):
            return "Empty"
        elif (self.type == enums.SetupDataType.Custom):
            return f"Custom "
        elif (self.type == enums.SetupDataType.Preset):
            return f"{SetupData.getPresetSetup(self.presetIndex)[1][0]}"
        elif (self.type == enums.SetupDataType.AllAny):
            return f"All Any"