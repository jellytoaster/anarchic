from classes.enums import Faction

class Role:
    
    allRoles:list = []
    def __init__(self, name:str, faction:Faction):
        self.name = name
        self.emoji = ""
        self.color = 0x000000
        self.faction = faction
        self.type = ""
        self.suspiciousRole = False
        self.promotionOrder = 0
        self.abilities:list = []
        self.roleEmbed = None
        self.order = 0 # 0 is first, higher numbers have their role action processed later
        Role.allRoles.append(self)

    def toRole(name:str):
        for i in Role.allRoles:
            if (i.name.lower() == name.lower()):
                return i
            
        return None