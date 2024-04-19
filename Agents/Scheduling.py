# Agent responsible for scheduling the energy produced by the sources in the system. It is responsible for the following tasks:
# 1. Receive the amount of energy produced by the sources
# 2. Receive the amount of energy requested by the houses in the system
# 3. Schedule the energy produced by the sources to the houses

from spade import agent

class SchedulingAgent(agent.Agent):

    async def setup(self):
        print("Scheduling Agent starting...")
        pass