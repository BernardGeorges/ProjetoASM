from spade import behaviour
from aux_classes.Energy import Energy
from aux_classes.HouseRequest import HouseRequest
from spade.message import Message
import jsonpickle
import time


class DistributeEnergy(behaviour.CyclicBehaviour):

    async def send_energy(self, request : HouseRequest):
        energy = Energy(request.getEnergyNeeded(), request.getTimeNeeded())

        print(request.getJid())
        msg = Message(to=request.getJid())
        msg.set_metadata("performative", "send_energy")
        msg.body = jsonpickle.encode(energy)
        await self.send(msg)

        print("Energy: {} sent to house: {}".format(request.getEnergyNeeded(),request.getJid()))	


    async def receive_values(self):
        msg = await self.receive(timeout=75)
        if msg:
            print("DistributeEnergy: Message received")
            performative = msg.get_metadata('performative')
            body =  msg.body
            if(performative == "energy_transfer"):
                print("DistributeEnergy: Energy Produced received")
                body : Energy = jsonpickle.decode(body)
                print("DistributeEnergy: Message Received \n Energy Produced: {} kWh, Valid Time: {}h".format(body.get_energy(), body.get_validTime()))
                self.received_energy = body                
            if(performative == "send_schedule"):
                print("DistributeEnergy: Energy Needed received")
                body = jsonpickle.decode(body)
                self.received_schedule = body
            else:
                print("DistributeEnergy: incorrect message received")

    async def run(self):
        print("DistributeEnergy: Running")
        self.received_energy = None
        self.received_schedule = None


        while self.received_energy == None or self.received_schedule == None:
            await self.receive_values()

        timeOut = time.time() + 60 * self.received_energy.get_validTime()

        # Receive the energy produced by the energy sources
        energyProduce = self.received_energy.get_energy()
        print(self.received_schedule)
        requests = self.received_schedule
       
        for request in requests: 
            if(energyProduce - request.getEnergyNeeded()): 
                print("Energy Produced: {}".format(energyProduce))
                await self.send_energy(request)
                energyProduce = energyProduce - request.getEnergyNeeded()
            elif self.agent.battery.getCharge() > 0:
                amount = self.agent.battery.discharge(request.getEnergyNeeded())
                possibleOffer = HouseRequest(request.getJid(), amount, 1)
                await self.send_energy(possibleOffer)
                energyProduce = energyProduce - request.getEnergyNeeded()
        
        if energyProduce > 0:
            self.agent.battery.charge(energyProduce)