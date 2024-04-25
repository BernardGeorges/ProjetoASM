from spade import behaviour
from spade.message import Message
import jsonpickle
from aux_classes.HouseRequest import HouseRequest

class InformEnergyNeeded_behav(behaviour.CyclicBehaviour):

    async def run(self):
        #print("             InformEnergyNeeded_behav: Running")

        # wait to receive the start signal from the scheduler
        receiveStart = await self.receive(timeout=10)
        print("             InformEnergyNeeded_behav: Message received")

        if receiveStart: 
            performative = receiveStart.get_metadata('performative')
            if(performative == "inform_start"):
                print("             House: Start signal received")
                maxTime = int(receiveStart.body)
                # get Energy Request from the house
                request : HouseRequest = self.agent.getNeededEnergy(maxTime)
                self.agent.currentRequest = request
                # Send the energy request to the scheduler        
                receiveStart = receiveStart.make_reply()
                receiveStart.set_metadata("performative", "inform_needed")
                receiveStart.body = jsonpickle.encode(request)
                await self.send(receiveStart)
                print("             House: Sending energy request to Scheduler")
            elif(performative == "request_battery"):
                print("             House: Battery Level requested")
                battery = self.agent.battery
                msg = receiveStart.make_reply()
                msg.set_metadata("performative", "inform_battery")
                msg.body = jsonpickle.encode(battery)
                await self.send(msg)
            else:
                 print("            House: Message not understood")
        else:
            print("             House: No message received")

        print("                     InformEnergyNeeded_behav: Finished")

        