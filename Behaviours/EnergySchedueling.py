from spade import behaviour
from spade.message import Message
from aux_classes.Energy import Energy
import jsonpickle

class EnergySchedueling_behav(behaviour.PeriodicBehaviour):

    #Send signal to the houses that the scheduling is starting
    async def __request_needed_energy(self, maxTime):
        print("energyNeeded")
        houses_jid = self.agent.get("house_jid")
        print(houses_jid)
        for house in houses_jid:
            msg = Message(to=house)
            msg.set_metadata("performative", "inform_start")
            msg.body = str(maxTime)
            await self.send(msg)
            print("Scheduler: sending scheduler start")

    async def run(self):

        print("EnergySchedueling_behav: Running")

        energyProduce = -1
        energyNeeded = -1

        # Receive the energy produced by the energy sources
        msg = await self.receive(timeout=75)

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
                
                await self.__request_needed_energy(time)
        else:
            print("Scheduler: No message received")

        print("Scheduler: scheduling done")
        