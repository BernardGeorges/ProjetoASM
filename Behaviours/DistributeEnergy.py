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
        msg.set_metadata("performative", "send_energy")
        msg.body = jsonpickle.encode(energy)
        await self.send(msg)

        print("     Energy: {} sent to house: {}".format(request.getEnergyNeeded(),request.getJid()))	


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
        print("     DistributeEnergy: hours passed: {}/timeout: {}".format(hours_passed, timeout))
        while hours_passed < timeout:
            print("     DistributeEnergy: sending energy")
            for request in requests: 
                if request.getTimeNeeded() == hours_passed:
                    requests.remove(request)
                else:
                    if request.getSource() == "production":
                        energyProduce = energyProduce - request.getEnergyNeeded()
                        if energyProduce < 0:
                            print("     Scheduling error: Not enough energy produced")
                        await self.send_energy(request)
                    elif request.getSource() == "battery":
                        energyAmount = self.agent.battery.discharge(request.getEnergyNeeded())
                        if energyAmount == 0:
                            print("     Scheduling error: Not enough energy in the battery")
                        await self.send_energy(request)
            hours_passed += 1
            if hours_passed < timeout:
                time.sleep(60)
                print("     DistributeEnergy: waiting for next hour")
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