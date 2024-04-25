from spade import behaviour
from spade.message import Message
from aux_classes.Energy import Energy
from aux_classes.HouseRequest import HouseRequest
from aux_classes.Battery import Battery
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
    async def __request_needed_houses(self, maxTime):
        ret = []
        print("Scheduler: getting energyNeeded ...")
        houses_jid = self.agent.get("house_jid")
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
    
    async def __request_batteries(self):
        ret = []
        print("Scheduler: getting battery values ...")
        houses_jid = self.agent.get("house_jid")
        for house in houses_jid:
            msg = Message(to=house)
            msg.set_metadata("performative", "request_battery")
            await self.send(msg)
            print("Scheduler: sending request battery")
        i = houses_jid.__len__()
        while i > 0:
            msg = await self.receive(timeout=5)
            if msg:
                print("Scheduler: Message received")
                performative = msg.get_metadata('performative')
                if(performative == "inform_battery"):
                    print("Scheduler: Battery received")
                    body : Battery = jsonpickle.decode(msg.body)
                    print("Scheduler: Message Received \n Energy Needed: {} kWh, Valid Time: {}h".format(body.getEnergyNeeded(), body.getTimeNeeded()))
                    i -= 1
                    ret.append(body)
            else:
                print("Scheduler: No message received")
                i = 0
        return sorted(ret)
    
    async def get_distribution_battery_level(self):
        msg = Message(to=self.agent.get("distributor_jid"))
        msg.set_metadata("performative", "get_battery")
        await self.send(msg)

        msg = await self.receive(timeout=5)
        if msg:
            print("Scheduler: Message received")
            performative = msg.get_metadata('performative')
            if(performative == "inform_battery"):
                print("Scheduler: Battery level received")
                body =  msg.body
                battery_level = float(body)
                print("Scheduler: Message Received \n Battery Level: {} kWh".format(battery_level))
                return battery_level
        else:
            print("Scheduler: No message received")
    
    def set_schedule(self, energyProduce, requests):
        schedule = []
        distribution_battery_level = self.get_distribution_battery_level()
        for request in requests: 
            if(energyProduce - request.getEnergyNeeded() >= 0): 
                print("Energy Produced: {}".format(energyProduce))
                request.setSource("production")
                schedule.append(request)
                energyProduce = energyProduce - request.getEnergyNeeded()
            elif(distribution_battery_level - request.getEnergyNeeded() >= 0):
                print("Energy Produced: {}".format(energyProduce))
                request.setSource("battery")
                schedule.append(request)
                distribution_battery_level = distribution_battery_level - request.getEnergyNeeded()
            else:
                print("No energy available")

        if(energyProduce > 0 or distribution_battery_level > 0):
            batteries = self.__request_batteries()
            sorted(batteries)
            for battery in batteries:
                if(energyProduce - battery.getEnergyNeeded() >= 0): 
                    print("Energy Produced: {}".format(energyProduce))
                    request = HouseRequest(battery.get_owner(), battery.get_charging_rate(), -1, -1)
                    request.setSource("production")
                    schedule.append(request)
                    energyProduce = energyProduce - battery.getEnergyNeeded()
                elif(distribution_battery_level - battery.getEnergyNeeded() >= 0):
                    print("Energy Produced: {}".format(energyProduce))
                    request = HouseRequest(battery.get_owner(), battery.get_charging_rate(), -1, -1)
                    request.setSource("battery")
                    schedule.append(request)
                    distribution_battery_level = distribution_battery_level - battery.getEnergyNeeded()
                else:
                    print("No energy available")
                schedule.append(battery)
        
        return schedule

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
                
                orders = await self.__request_needed_houses(time)
                print("Scheduler: Orders received")

                schedule = self.set_schedule(energyProduce, orders)

                await self.__send_energy(schedule)
                print("Scheduler: schedule sent to distributor")
        else:
            print("Scheduler: No message received")

        print("Scheduler: scheduling done")
        