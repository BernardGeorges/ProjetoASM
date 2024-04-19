from spade import quit_spade
from Agents.energyManager import EnergyManagerAgent
from Agents.House import HouseAgent 
import time

XMPP_SERVER = 'desktop-vi70507.lan' #put your XMPP_SERVER
PASSWORD = "NOPASSWORD" #put your password

if __name__ == '__main__':

    energyManager_jid = 'energy_manager@' + XMPP_SERVER

    # Create agents Seller and Buyer instances
    energyManager_agent = EnergyManagerAgent(energyManager_jid, PASSWORD)
    house_agent = HouseAgent('house@' + XMPP_SERVER, PASSWORD)

    # place them into the start status
    house_agent.start() 
    res_energyManager = energyManager_agent.start()  # Execute Seller_agent
    res_energyManager.result()  # Verify if Seller_agent is active
    energyManager_agent.web.start(hostname="127.0.0.1", port=10000)

    while energyManager_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            energyManager_agent.stop()
            house_agent.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()