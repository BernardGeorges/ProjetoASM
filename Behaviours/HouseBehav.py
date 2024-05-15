from spade import behaviour
from spade.message import Message
import jsonpickle
from aux_classes.HouseRequest import HouseRequest

class HouseBehav(behaviour.CyclicBehaviour):

    async def run(self):
        #print("             InformEnergyNeeded_behav: Running")

        # wait to receive the start signal from the scheduler
        receiveStart = await self.receive(timeout=10)
    
        if receiveStart: 
            print("             HouseBehaviour: Message received")
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
            elif(performative == "charge_battery"):
                print("             House: Charging battery")
                body = receiveStart.body
                energy = jsonpickle.decode(body)
                self.agent.battery.charge(energy.get_energy())
            elif(performative == "energy_transfer"):
                print("             House: Energy received")
                body = receiveStart.body
                energy = jsonpickle.decode(body)
                print("             House: Energy Received \n Energy: {} kWh, Valid Time: {}h".format(energy.get_energy(), energy.get_validTime()))
            elif(performative == "inform_stop"):
                print("             House: Stop signal received")
                await self.agent.stop()
            elif(performative == "ack_stop"):
                print("             House: Stop acknoledgement received")
                await self.agent.stop()
            elif(performative == "ack_start"):
                print("             House: Start acknoledgement received")
                self.agent.remove_behaviour(self.agent.behaviours[0])
            else:
                 print("            House: Message not understood")
        print("                     HouseBehaviour: Finished")

        