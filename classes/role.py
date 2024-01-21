import utils
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
    
    def init():
        import classes.roles.cop
        import classes.roles.mafioso
        import classes.roles.villager
        import classes.roles.associate
        import classes.roles.doctor
        import classes.roles.vigilante
        import classes.roles.consort
        import classes.roles.jester
        import classes.roles.headhunter

        classes.roles.cop.Cop("Cop", Faction.Town)
        classes.roles.mafioso.Mafioso("Mafioso", Faction.Mafia)
        classes.roles.villager.Villager("Villager", Faction.Town)
        classes.roles.associate.Associate("Associate", Faction.Mafia)
        classes.roles.vigilante.Vigilante("Vigilante", Faction.Town)
        classes.roles.doctor.Doctor("Doctor", Faction.Town)
        classes.roles.consort.Consort("Consort", Faction.Mafia)
        classes.roles.jester.Jester("Jester", Faction.Neutral)
        classes.roles.headhunter.Headhunter("Headhunter", Faction.Neutral)