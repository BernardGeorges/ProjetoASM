# Agent responsible for scheduling the energy produced by the sources in the system. It is responsible for the following tasks:
# 1. Receive the amount of energy produced by the sources
# 2. Receive the amount of energy requested by the houses in the system
# 3. Schedule the energy produced by the sources to the houses

from spade import agent
from Behaviours.EnergySchedueling import EnergySchedueling_behav
from Behaviours.smoothStop import smoothStop

class SchedulingAgent(agent.Agent):

    housesSubscribed = []

    async def setup(self):
        print("Scheduling Agent starting...")
        behav = EnergySchedueling_behav()
        self.add_behaviour(behav)

    def revisedStop(self):
        print("Scheduling Agent stopping...")
        stopBehav = smoothStop()
        self.add_behaviour(stopBehav)
        while not stopBehav.is_done():
            pass
        print("         Scheduler: stop message sent")
        self.stop()
        