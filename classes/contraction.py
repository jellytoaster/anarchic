import string

class Contraction():
    allContractions = []
    def __init__(self, faction, type, displayname, emoji = "") -> None:
        self.faction = faction
        self.type = type
        self.display_name = displayname
        self.emoji = emoji

        Contraction.allContractions.append(self)

    def getContraction(name):
        return [e for e in Contraction.allContractions if e.display_name == string.capwords(name.lower())][0]

    def initContractions():
        # Town Roles
        Contraction("town", "", "Random Town", "🏠")
        Contraction("town", "investigative", "Town Investigative", "🔍")
        Contraction("town", "killing", "Town Killing", "🔫")
        Contraction("town", "protective", "Town Protective", "💉")        

        # Mafia Roles
        Contraction("mafia", "", "Random Mafia", "🌹")
        Contraction("mafia", "killing", "Mafia Killing", "🔪")
        Contraction("mafia", "support", "Mafia Support", "💖")     

        # Neutral Roles
        Contraction("neutral", "", "Random Neutral", "🤷‍♂️")
        Contraction("neutral", "evil", "Neutral Evil", "🪓")