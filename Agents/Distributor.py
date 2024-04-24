#Agent responsible for managing the energy of the multiple sources in the system. It is responsible for the following tasks:
#1. Receve the energy produced by the energy sources
#2. Receive the houses and the amount of energy to send 
#3. Send the energy produced to the correct houses

from spade import agent
from Behaviours.DistributeEnergy import DistributeEnergy
from aux_classes.Battery import Battery

class DistributorAgent(agent.Agent):

    async def setup(self):
        print("Distributor Agent starting...")
        self.battery = Battery(1000, 5, 10)
        b = DistributeEnergy()


        self.add_behaviour(b)

        