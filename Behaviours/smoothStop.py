from spade import behaviour
from spade.message import Message

class smoothStop(behaviour.OneShotBehaviour):
    async def run(self):
        while self.agent.housesSubscribed:
            for house in self.agent.housesSubscribed:
                msg = Message(to=house)
                msg.set_metadata("performative", "inform_stop")
                await self.send(msg)

        print("Agent stopping...")
        self.agent.revisedStop()
        print("Agent stopped")
        self.kill()