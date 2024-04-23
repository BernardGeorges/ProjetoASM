

class HouseRequest: 

    def __init__(self, jid, energyNeeded, timeNeeded):
        self.jid = jid
        self.energyNeeded = energyNeeded
        self.timeNeeded = timeNeeded

    def getJid(self):
        return self.jid
    
    def getEnergyNeeded(self):
        return self.energyNeeded
    
    def getTimeNeeded(self):
        return self.timeNeeded