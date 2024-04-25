#Agent responsible for managing the energy of the multiple sources in the system. It is responsible for the following tasks:
#1. Notify the scheduler agent about the amount of energy produced
#2. Send the energy produced to the distributor agentS

import random
from spade import agent
import time
from aux_classes.Energy import Energy

from Behaviours.InformEnergyProduced_behav import InformEnergyProduced_behav

class EnergySource():    
        sourcesAmount = {'solar': 0, 'wind': 0, 'hidrolics': 0}
        possibleValues = {'solar' : {'Sunny' : (20,30), 'Cloudy': (2,7.5), 'Rainy': (0.4,1.5)}, 'wind' : {'low': (10,20), 'medium': (30,50), 'high': (60,80)}, 'hidrolics' : (1000,8000)}
        
        def __init__(self, solarAmount, windAmount, hidrolicsAmount, cycleTime):
            #print("Energy Source Agent starting...")
            self.sourcesAmount = {'solar': solarAmount, 'wind': windAmount, 'hidrolics': hidrolicsAmount}
            self.cycleTime = cycleTime

        def get_generatedEnergy(self):
            solar = random.uniform(self.possibleValues['solar']['Sunny'][0], self.possibleValues['solar']['Sunny'][1])
            wind = random.uniform(self.possibleValues['wind']['medium'][0], self.possibleValues['wind']['medium'][1])
            hidrolics = random.uniform(self.possibleValues['hidrolics'][0], self.possibleValues['hidrolics'][1])
            energyProduced = Energy((solar * self.sourcesAmount['solar'] + wind * self.sourcesAmount['wind'] + hidrolics * self.sourcesAmount['hidrolics']), self.cycleTime)
            return energyProduced

class EnergyManagerAgent(agent.Agent):

    async def setup(self):
        #print("Energy Manager Agent starting... ")
        solar = int(input("Enter the amount of solar panels in the system: "))
        wind = int(input("Enter the amount of wind turbines in the system: "))
        hidrolics = int(input("Enter the amount of hidrolics turbines in the system: "))
        max_time = int(input("Enter the time (in minute) between each energy prediction: "))

        self.energySource = EnergySource(solar, wind, hidrolics, max_time)

        behav = InformEnergyProduced_behav(period=60) #period is the time in seconds between each energy production which indicates the max_time
        self.add_behaviour(behav)