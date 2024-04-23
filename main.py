from spade import quit_spade
from Agents.EnergyManager import EnergyManagerAgent
from Agents.House import HouseAgent 
from Agents.Distributor import DistributorAgent
from Agents.Scheduling import SchedulingAgent
import time

XMPP_SERVER = 'host.docker.internal' #put your XMPP_SERVER
PASSWORD = "NOPASSWORD" #put your password

if __name__ == '__main__':

    energyManager_jid = 'energy_manager@' + XMPP_SERVER
    house_jid = 'house@' + XMPP_SERVER
    distributor_jid = 'distributor@' + XMPP_SERVER
    scheduling_jid = 'scheduling@' + XMPP_SERVER

    #Creating agents
    energyManager_agent = EnergyManagerAgent(energyManager_jid, PASSWORD)
    house_agent = HouseAgent(house_jid, PASSWORD)
    distributor_agent = DistributorAgent(distributor_jid, PASSWORD)
    scheduling_agent = SchedulingAgent(scheduling_jid, PASSWORD)

    #Adding the agents to the platform
    energyManager_agent.set("distributor_jid", distributor_jid)
    energyManager_agent.set("scheduler_jid", scheduling_jid)

    house_agent.set("scheduling_jid", scheduling_jid)

    scheduling_agent.set("distributor_jid", distributor_jid)
    scheduling_agent.set("house_jid", [house_jid])
    scheduling_agent.set("energy_manager_jid", energyManager_jid)
    

    # starting the agents
    house_agent.start() 
   # distributor_agent.start()
    res_scheduler = scheduling_agent.start()
    res_scheduler.result()
    energyManager_agent.start()

    while scheduling_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            house_agent.stop()
            distributor_agent.stop()
            energyManager_agent.stop()
            scheduling_agent.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()