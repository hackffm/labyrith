from things.thing import Thing
from things.iridthing import IridThing

class Ir(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.things = {}

    def addThing(self, thing:IridThing):
        self.things[thing.irid] = thing

    def handleMessage(self, msg, m):
        print("Irid: " + msg)
        thing = self.things[m["irid"]]
        if thing is not None:
            m[thing] = thing.tid
            thing.handleMessage(msg.replace('irid', thing.tid), m)
