from spade import behaviour, message

class SubscribeHouse(behaviour.PeriodicBehaviour):

    async def run(self):
        scheduler_jid = self.agent.get("scheduler_jid")
        msg = message.Message(to=scheduler_jid)
        msg.set_metadata("performative", "subscribe")
        await self.send(msg)
        print(f"        Sent message to {scheduler_jid}")
        print("         House subscribed to the scheduler agent.")