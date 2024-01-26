import string

class Contraction():
    allContractions = []
    def __init__(self, faction, type, displayname, emoji = "", showInSetup=True) -> None:
        self.faction = faction
        self.type = type
        self.display_name = displayname
        self.emoji = emoji
        self.show = showInSetup

        Contraction.allContractions.append(self)

    def getContraction(faction, type):
        return [e for e in Contraction.allContractions if e.faction.lower() == faction.lower() and e.type.lower() == type.lower()][0]
    
    def initContractions():
        # Town Roles
        Contraction("town", "", "Random Town", "🏠")
        Contraction("town", "investigative", "Town Investigative", "🔍")
        Contraction("town", "killing", "Town Killing", "🔫")
        Contraction("town", "protective", "Town Protective", "💉")  
        Contraction("town", "vanilla", "Town Vanilla", "🏠", False)        

        # Mafia Roles
        Contraction("mafia", "", "Random Mafia", "🌹")
        Contraction("mafia", "killing", "Mafia Killing", "🔪")
        Contraction("mafia", "support", "Mafia Support", "🥀")     
        Contraction("mafia", "deception", "Mafia Deception", "🎞️")     
        Contraction("mafia", "vanilla", "Mafia Vanilla", "🌹", False)       

        # Neutral Roles
        Contraction("neutral", "", "Random Neutral", "🤷‍♂️")
        Contraction("neutral", "evil", "Neutral Evil", "🪓")