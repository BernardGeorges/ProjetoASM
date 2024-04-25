

class HouseRequest: 

    def __init__(self, jid, energyNeeded, timeNeeded, battery_left):
        self.jid = jid
        self.energyNeeded = energyNeeded
        self.timeNeeded = timeNeeded
        self.battery_left = battery_left
        self.source = None

    def getJid(self):
        return self.jid
    
    def getEnergyNeeded(self):
        return self.energyNeeded
    
    def getTimeNeeded(self):
        return self.timeNeeded
    
    def getBatteryLeft(self):
        return self.battery_left
    
    def setSource(self, source):
        self.source = source

    def getSource(self):
        return self.source
    
    def __lt__(self, obj): 
        return self.energyNeeded * self.timeNeeded < obj.energyNeeded * obj.timeNeeded
  
    def __gt__(self, obj): 
        return self.energyNeeded * self.timeNeeded > obj.energyNeeded * obj.timeNeeded
  
    def __le__(self, obj): 
        return self.energyNeeded * self.timeNeeded <= obj.energyNeeded * obj.timeNeeded
  
    def __ge__(self, obj): 
        return self.energyNeeded * self.timeNeeded >= obj.energyNeeded * obj.timeNeeded
  
    def __eq__(self, obj): 
        return self.energyNeeded == obj.energyNeeded and self.timeNeeded == obj.timeNeeded and self.jid == obj.jid
    
    def __repr__(self): 
        return ("(House: {}, Energy Needed: {} kWh, needed Time: {}h)".format(self.getJid(),self.getEnergyNeeded(), self.getTimeNeeded()))