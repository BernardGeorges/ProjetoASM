from spade import agent
import random

from Behaviours.HouseBehav import HouseBehav
from aux_classes.HouseRequest import HouseRequest
from aux_classes.Battery import Battery 

class HouseAgent(agent.Agent):

    energyNeeded = {'unoccupied': (5,15), 'occupied': (10,50)}

    async def setup(self):
        #print("House Agent starting...")
        self.battery = Battery(5, 10, 250, self.jid.__str__())
        self.currentRequest = None

        behav = HouseBehav()
        self.add_behaviour(behav)



    def getNeededEnergy(self, maxTime = 10):
        request = HouseRequest(self.jid.__str__(), random.uniform(self.energyNeeded['occupied'][0], self.energyNeeded['occupied'][1]), random.randint(1, maxTime), self.battery.get_charge_left())
        return request

