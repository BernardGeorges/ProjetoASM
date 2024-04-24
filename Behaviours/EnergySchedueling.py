from spade import behaviour
from spade.message import Message
from aux_classes.Energy import Energy
from aux_classes.HouseRequest import HouseRequest
import jsonpickle

class EnergySchedueling_behav(behaviour.CyclicBehaviour):

    #Send to the distributor the schedule made by the scheduler
    async def __send_energy(self, requests):
            print("send_schedule")
            distributor_jid = self.agent.get("distributor_jid")
            print(distributor_jid)
            msg = Message(to=distributor_jid)
            msg.set_metadata("performative", "send_schedule")
            msg.body = jsonpickle.encode(requests)
            await self.send(msg)



    #Send signal to the houses that the scheduling is starting
    #Receives the energy needed by the houses and the time they need it
    #Returns the requests in a sorted list
    async def __request_needed_energy(self, maxTime):
        ret = []
        print("energyNeeded")
        houses_jid = self.agent.get("house_jid")
        print(houses_jid)
        for house in houses_jid:
            msg = Message(to=house)
            msg.set_metadata("performative", "inform_start")
            msg.body = str(maxTime)
            await self.send(msg)
            print("Scheduler: sending scheduler start")
        i = houses_jid.__len__()
        while i > 0:
            msg = await self.receive(timeout=5)
            if msg:
                print("Scheduler: Message received")
                performative = msg.get_metadata('performative')
                if(performative == "inform_needed"):
                    print("Scheduler: Energy Needed received")
                    body : HouseRequest = jsonpickle.decode(msg.body)
                    print("Scheduler: Message Received \n Energy Needed: {} kWh, Valid Time: {}h".format(body.getEnergyNeeded(), body.getTimeNeeded()))
                    i -= 1
                    ret.append(body)
            else:
                print("Scheduler: No message received")
                i = 0
        return sorted(ret)
        

    async def run(self):

        print("EnergySchedueling_behav: Running")

        # Receive the energy produced by the energy sources
        msg = await self.receive(timeout=10)

        if msg:
            print("Scheduler: Message received")
            performative = msg.get_metadata('performative')
            if(performative == "inform_production"):
                print("Scheduler: Energy Produced received")
                body =  msg.body
                body : Energy = jsonpickle.decode(body)
                energyProduce = body.get_energy()
                time = body.get_validTime()
                print("Scheduler: Message Received \n Energy Produced: {} kWh, Valid Time: {}h".format(energyProduce, time))
                
                orders = await self.__request_needed_energy(time)
                print("Scheduler: Orders received")

                await self.__send_energy(orders)
                print("Scheduler: Orders sent to distributor")
        else:
            print("Scheduler: No message received")

        print("Scheduler: scheduling done")
        