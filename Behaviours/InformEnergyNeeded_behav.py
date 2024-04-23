from spade import behaviour
from spade.message import Message
import jsonpickle
from aux_classes.HouseRequest import HouseRequest

class InformEnergyNeeded_behav(behaviour.PeriodicBehaviour):

    async def run(self):
        print("InformEnergyProduced_behav: Running")

        # wait to receive the start signal from the scheduler
        receiveStart = await self.receive(timeout=80)

        if receiveStart: 
            performative = receiveStart.get_metadata('performative')
            if(performative == "inform_start"):
                maxTime = int(receiveStart.body)
                # get Energy Request from the house
                request : HouseRequest = self.agent.getNeededEnergy(maxTime)
                
                # Send the energy request to the scheduler        
                receiveStart = receiveStart.make_reply()
                receiveStart.set_metadata("performative", "inform_needed")
                receiveStart.body = jsonpickle.encode(request)
                await self.send(receiveStart)
                print("House: Sending energy request to Scheduler")
        