from spade import agent
import random

from Behaviours.InformEnergyNeeded_behav import InformEnergyNeeded_behav

class HouseAgent(agent.Agent):

    energyNeeded = {'unoccupied': (5,15), 'occupied': (10,50)}

    async def setup(self):
        print("House Agent starting...")
        self.battery = 0

        behav = InformEnergyNeeded_behav(period=1)
        self.add_behaviour(behav)


    def getNeededEnergy(self):
        return random.randint(self.energyNeeded['occupied'][0], self.energyNeeded['occupied'][1])

