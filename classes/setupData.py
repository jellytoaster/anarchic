from classes import enums
import string
import utils


class SetupData():
    def __init__(self, game) -> None:
        self.roles = []
        self.game = game
        self.type = enums.SetupDataType.Preset

    def addRole(self, role:enums.Role, amount:int):
        for _ in range(amount):
            self.roles.append(role)

    def removeRole(self, role:enums.Role, amount:int):
        # 1: Role not in list
        # 2: amount higher than roles in list
        if (role not in self.roles):
            return 1
        
        for _ in range(amount):
            try:
                self.roles.remove(role)
            except:
                return 2
        
        return 0
    
    def generateSetupList(self):
        result = "\n".join(map(lambda x: f"**{string.capwords(x)} {utils.roleEmoji(x)}**", self.roles))
        if (result == ""):
            return ":x: **None**"
        return result