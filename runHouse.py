from spade import quit_spade
from Agents.House import HouseAgent
import time

XMPP_SERVER = 'host.docker.internal' #put your XMPP_SERVER
PASSWORD = "NOPASSWORD" #put your password

scheduling_jid = 'scheduling@' + XMPP_SERVER

house_jid = input("Enter the house jid: ")
house_jid = house_jid + '@' + XMPP_SERVER
house_agent = HouseAgent(house_jid, PASSWORD)
house_agent.set("scheduler_jid", scheduling_jid) 

res_house = house_agent.start()
res_house.result()

while house_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            house_agent.revisedStop()
            break
print('Agents finished')

quit_spade()