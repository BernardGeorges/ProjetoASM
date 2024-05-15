from spade import behaviour
from aux_classes.Energy import Energy
from aux_classes.HouseRequest import HouseRequest
from spade.message import Message
import jsonpickle
import time


class DistributeEnergy(behaviour.CyclicBehaviour):

    async def send_energy(self, request : HouseRequest):
        energy = Energy(request.getEnergyNeeded(), 1)

        msg = Message(to=request.getJid())
        print("TO: {}".format(request.getTo()))
        if request.getTo() == "battery":
            print("     Energy: {} sent to battery".format(request.getEnergyNeeded()))
            msg.set_metadata("performative", "charge_battery")
        else:
            msg.set_metadata("performative", "energy_transfer")
            print("     Energy: {} sent to house: {}".format(request.getEnergyNeeded(),request.getJid()))	

        msg.body = jsonpickle.encode(energy)
        await self.send(msg)



    async def receive_values(self):
        msg = await self.receive(timeout=75)
        if msg:
            performative = msg.get_metadata('performative')
            body =  msg.body
            if(performative == "energy_transfer"):
                print("     DistributeEnergy: Energy Produced received")
                body : Energy = jsonpickle.decode(body)
                print("     DistributeEnergy: Message Received \n Energy Produced: {} kWh, Valid Time: {}h".format(body.get_energy(), body.get_validTime()))
                self.received_energy = body                
            elif(performative == "send_schedule"):
                print("     DistributeEnergy: Schedule received")
                body = jsonpickle.decode(body)
                self.received_schedule = body
            elif(performative == "get_battery"):
                print("     DistributeEnergy: Battery Level requested")
                battery = self.agent.battery.get_charge_left()
                msg = msg.make_reply()
                msg.set_metadata("performative", "inform_battery")
                msg.body = str(battery)
                await self.send(msg)
            else:
                print("     DistributeEnergy: incorrect message received")

    async def distribute(self, requests, producedEnergy):
        hours_passed = 0
        timeout = producedEnergy.get_validTime()
        energyProduce = producedEnergy.get_energy()
        energyAmount = 0
        while hours_passed < timeout:
            print("     DistributeEnergy: sending energy")
            print("     DistributeEnergy: requests: {}".format(requests))
            for request in requests: 
                if request.getTimeNeeded() == hours_passed:
                    requests.remove(request)
                else:   
                    print("     DistributeEnergy: time: {}, hours_passed: {}".format(request.getTimeNeeded(), hours_passed))
                    if request.getSource() == "production":
                        energyProduce = energyProduce - request.getEnergyNeeded()
                    elif request.getSource() == "battery":
                        energyAmount = self.agent.battery.discharge(request.getEnergyNeeded())
                    if energyAmount < 0 or energyProduce < 0:
                        print("     Scheduling error: Not enough energy in the battery")
                        raise("     Scheduling error: Not enough energy in the battery")
                    await self.send_energy(request)
            hours_passed += 1
            if hours_passed <= timeout:
                time.sleep(10)
                print("     DistributeEnergy: waiting for next hour")
            print("     DistributeEnergy: hours passed: {}/timeout: {}".format(hours_passed, timeout))
        print("     DistributeEnergy: Distribution finished")
        return energyProduce


    async def run(self):
        #print("     DistributeEnergy: Running")
        self.received_energy = None
        self.received_schedule = None

        while self.received_energy == None or self.received_schedule == None:
            await self.receive_values()

        # Receive the energy produced by the energy sources
        print("     Received Schedule: ".format(self.received_schedule))
        requests = self.received_schedule

        energyLeft = await self.distribute(requests, self.received_energy)
        
        if energyLeft > 0:
            self.agent.battery.charge(energyLeft)

        print("                     Distribution finished")