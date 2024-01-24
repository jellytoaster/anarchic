class investigationResults():
    def __init__(self, cop:bool, consig:str):
        self.copSuspicious = cop
        self.consigliereFlavorText = consig

        # investigative roles will use this because framer could modify this without breaking actual targets
        self.lookoutVisitedBy = []
        self.trackerTargetted = []