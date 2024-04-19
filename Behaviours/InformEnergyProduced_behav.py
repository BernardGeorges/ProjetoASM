from spade import behaviour
from spade.message import Message  
from aux_classes import Energy

class InformEnergyProduced_behav(behaviour.PeriodicBehaviour):
    async def run(self):
        print("InformEnergyProduced_behav: Running")

        energySource = self.agent.energySource
        energyProduced = energySource.get_generatedEnergy()

        print("Energy Produced: {} kWh".format(energyProduced))

        scheduler_jid = self.get("scheduler_jid")
        distributor_jid = self.get("distributor_jid")

        energy = Energy(energyProduced)

        msgScheduler = Message(to=scheduler_jid)
        msgScheduler.body = str(energyProduced)
        await self.send(msgScheduler)

        print("Msg with Energy Produced sent to Scheduler")
        
        msgDistributor = Message(to=distributor_jid)
        msgDistributor.body = energy
        await self.send(msgDistributor)

        print("Energy Produced sent to Distributor")