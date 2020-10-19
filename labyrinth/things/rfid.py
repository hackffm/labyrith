from things.thing import Thing
from things.rfidthing import RfidThing

class Rfid(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.things = {}

    def addThing(self, thing:RfidThing):
        self.things[thing.rfid] = thing

    def handleMessage(self, msg, m):
        print("Rfid: " + msg)
        thing = self.things[m["id"]]
        if thing is not None:
            m[thing] = thing.tid
            thing.handleMessage(msg.replace('rfid', thing.tid), m)
