from spade import behaviour

class InformEnergyNeeded_behav(behaviour.PeriodicBehaviour):

    async def run(self):
        print("InformEnergyProduced_behav: Running")

        energyNeeded = self.agent.getNeededEnergy()
        

        print("Energy Needed: {} kWh".format(energyNeeded))
