from spade import behaviour
from spade.message import Message

class smoothStop(behaviour.OneShotBehaviour):
    async def run(self):
        print("Agent informing stoppage...")
        print(self.agent.housesSubscribed)
        for house in self.agent.housesSubscribed:
            print("         Scheduler: sending scheduler stop")
            msg = Message(to=house)
            msg.set_metadata("performative", "inform_stop")
            await self.send(msg)

        