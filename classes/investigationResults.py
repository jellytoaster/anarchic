import copy

class investigationResults():
    def __init__(self, cop:bool, consig:str):
        self.realCopSuspicious = cop

        self.copSuspicious = cop
        self.consigliereFlavorText = consig

        # investigative roles will use this because framer could modify this without breaking actual targets
        self.lookoutVisitedBy = []
        self.trackerTargetted = []

    def reset(self, player):
        """Resets an investigation result to its real values. Useful for unframing somebody."""
        self.copSuspicious = self.realCopSuspicious

        self.lookoutVisitedBy = player.whoVisitedMe()
        self.trackerTargetted = copy.copy(player.nightTargettedPlayers)