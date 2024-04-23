#Agent responsible for managing the energy of the multiple sources in the system. It is responsible for the following tasks:
#1. Receve the energy produced by the energy sources
#2. Receive the houses and the amount of energy to send 
#3. Send the energy produced to the correct houses

from spade import agent

class DistributorAgent(agent.Agent):

    async def setup(self):
        print("Distributor Agent starting...")
        pass