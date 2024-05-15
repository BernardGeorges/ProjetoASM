from spade import behaviour
from spade.message import Message  
from aux_classes.Energy import Energy
import jsonpickle
import logging

class InformEnergyProduced_behav(behaviour.PeriodicBehaviour):

    async def run(self):

        #print("                     InformEnergyProduced_behav: Running")

        energyProduced= self.agent.energySource.get_generatedEnergy()
        scheduler_jid = self.agent.get("scheduler_jid")
        distributor_jid = self.agent.get("distributor_jid")

              
        # Informing the Scheduler about the energy produced

        msgScheduler = Message(to=scheduler_jid)
        msgScheduler.body = jsonpickle.encode(energyProduced)
        msgScheduler.set_metadata("performative", "inform_production")
        await self.send(msgScheduler)

        print("                     Source: Msg with Energy Produced sent to Scheduler")

        #Sending Energy produced to the distributer agent
        msgDistributor = Message(to=distributor_jid)
        msgDistributor.body = jsonpickle.encode(energyProduced)
        msgDistributor.set_metadata("performative", "energy_transfer")
        await self.send(msgDistributor)

        print("                     Energy Produced sent to Distributor")

        print("                     InformEnergyProduced_behav: Finished")