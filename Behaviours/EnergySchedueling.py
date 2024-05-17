from spade import behaviour
from spade.message import Message
from aux_classes.Energy import Energy
from aux_classes.HouseRequest import HouseRequest
from aux_classes.Battery import Battery
import jsonpickle

class EnergySchedueling_behav(behaviour.CyclicBehaviour):

    #Send to the distributor the schedule made by the scheduler
    async def __send_energy(self, requests):
            print("         send_schedule")
            distributor_jid = self.agent.get("distributor_jid")         
            msg = Message(to=distributor_jid)
            msg.set_metadata("performative", "send_schedule")
            msg.body = jsonpickle.encode(requests)
            await self.send(msg)



    #Send signal to the houses that the scheduling is starting
    #Receives the energy needed by the houses and the time they need it
    #Returns the requests in a sorted list
    async def __request_needed_houses(self, maxTime):
        ret = []
        print("         Scheduler: getting energyNeeded ...")
        houses_jid = self.agent.housesSubscribed
        for house in houses_jid:
            msg = Message(to=house)
            msg.set_metadata("performative", "inform_start")
            msg.body = str(maxTime)
            await self.send(msg)
            print("         Scheduler: sending scheduler start")
        i = houses_jid.__len__()
        while i > 0:
            msg = await self.receive(timeout=5)
            if msg:
                print("         Scheduler: Message received")
                performative = msg.get_metadata('performative')
                if(performative == "inform_needed"):
                    print("         Scheduler: Energy Needed received")
                    body : HouseRequest = jsonpickle.decode(msg.body)
                    print("         Scheduler: Message Received \n Energy Needed: {} kWh, Valid Time: {}h".format(body.getEnergyNeeded(), body.getTimeNeeded()))
                    i -= 1
                    ret.append(body)
            else:
                print("         Scheduler: No message received")
                i = 0
        return sorted(ret)
    
    async def __request_batteries(self):
        ret = []
        print("         Scheduler: getting battery values ...")
        houses_jid = self.agent.housesSubscribed
        for house in houses_jid:
            msg = Message(to=house)
            msg.set_metadata("performative", "request_battery")
            await self.send(msg)
            print("         Scheduler: sending request battery")
        i = houses_jid.__len__()
        while i > 0:
            msg = await self.receive(timeout=5)
            if msg:
                print("         Scheduler: Message received")
                performative = msg.get_metadata('performative')
                if(performative == "inform_battery"):
                    print("         Scheduler: Battery received")
                    body : Battery = jsonpickle.decode(msg.body)
                    print("         Scheduler: Message Received \n Battery Level: {} kWh from {}".format(body.get_charge_left(), body.get_max_charge()))
                    ret.append(body)
                i -= 1
            else:
                print("         Scheduler: No message received")
        print("         Scheduler: Batteries received {}".format(ret))
        return sorted(ret)
    
    async def get_distribution_battery_level(self):
        msg = Message(to=self.agent.get("distributor_jid"))
        msg.set_metadata("performative", "request_battery")
        await self.send(msg)

        msg = await self.receive(timeout=5)
        if msg:
            print("         Scheduler: Message received")
            performative = msg.get_metadata('performative')
            if(performative == "inform_battery"):
                print("         Scheduler: Battery level received")
                body =  msg.body
                battery_level = float(body)
                print("         Scheduler: Message Received \n Battery Level: {} kWh".format(battery_level))
                return battery_level
        else:
            print("         Scheduler: No message received")
    
    async def set_schedule(self, energyProduce, requests):
        print("===================Schedule=========================")
        schedule = []
        distribution_battery_level = await self.get_distribution_battery_level()
        print("         Energy Produced: {}".format(energyProduce))
        for request in requests:
            request.setTo("house") 
            if(energyProduce - request.getEnergyNeeded() >= 0): 
                print("         Energy Produced: {}".format(energyProduce))
                request.setSource("production")
                schedule.append(request)
                energyProduce = energyProduce - request.getEnergyNeeded()
            elif(distribution_battery_level - request.getEnergyNeeded() >= 0):
                print("         Battery: {}".format(energyProduce))
                request.setSource("battery")
                schedule.append(request)
                distribution_battery_level = distribution_battery_level - request.getEnergyNeeded()
            else:
                print("         No energy available")

        print("         Overproduce energy: {}".format(energyProduce))

        if(energyProduce > 0 or distribution_battery_level > 0):
            batteries = await self.__request_batteries()
            print("         batteries: {}".format(batteries)) 
            for battery in batteries:
                if(energyProduce - battery.get_charging_rate() >= 0): 
                    print("         Energy Produced: {}".format(energyProduce))
                    energyNeeded = battery.get_max_charge() - battery.get_charge_left()
                    timeNeeded = energyNeeded / battery.get_charging_rate()
                    request = HouseRequest(battery.get_owner(), battery.get_charging_rate(), timeNeeded, battery.get_charge_left(), "production", "battery")
                    schedule.append(request)
                    energyProduce = energyProduce - battery.get_charging_rate()
                elif(distribution_battery_level - battery.get_charging_rate() >= 0):
                    print("         battery: {}".format(energyProduce))
                    energyNeeded = battery.get_max_charge() - battery.get_charge_left()
                    timeNeeded = energyNeeded / battery.get_charging_rate()
                    request = HouseRequest(battery.get_owner(), battery.get_charging_rate(), timeNeeded, battery.get_charge_left(), "battery", "battery")
                    schedule.append(request)
                    distribution_battery_level = distribution_battery_level - battery.get_charging_rate()
                else:
                    print("         No energy available")
        
        if(energyProduce > 0):
            request = HouseRequest("distributor", energyProduce, 1, 0, "production", "battery")
            schedule.append(request)
        
        print("=============================================")
        return schedule

    async def run(self):

        #print("         EnergySchedueling_behav: Running")
        # Receive the energy produced by the energy sources
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata('performative')
            if(performative == "inform_production"):
                body =  msg.body
                body : Energy = jsonpickle.decode(body)
                energyProduce = body.get_energy()
                time = body.get_validTime()
                print("         Scheduler: Message Received \n Energy Produced: {} kWh, Valid Time: {}h".format(energyProduce, time))
                
                orders = await self.__request_needed_houses(time)
                print("         Scheduler: Orders received: {}".format(orders))

                schedule = await self.set_schedule(energyProduce, orders)
                print("         Scheduler: Schedule set: {}".format(schedule))

                

                await self.__send_energy(schedule)
                print("         Scheduler: schedule sent to distributor")
                print("                     Scheduler: scheduling done")
            elif(performative == "subscribe"):
                print("         Scheduler: House {} subscribed".format(msg.sender)) 
                house = str(msg.sender)
                if house not in self.agent.housesSubscribed:
                    self.agent.housesSubscribed.append(house)
                    msg = msg.make_reply()
                    msg.set_metadata("performative", "ack_start")
                    await self.send(msg)
            elif(performative == "unsubscribe"):
                print("         Scheduler: House {} unsubscribed".format(msg.sender))
                self.agent.housesSubscribed.remove(str(msg.sender))
                msg = msg.make_reply()
                msg.set_metadata("performative", "ack_stop")
                await self.send(msg)
            else:
                print("         Scheduler: incorrect message received")

        