from .iridthing import IridThing

class KeyCard(IridThing):

    def handleMessage(self, msg, m):
        print("KeyCard: " + self.irid + "  " + msg)
        car = self.labyrinth.get_thing(m["car"])
        if m["type"] == "t":
            print("add")
            car.addItem(self)
        elif m["type"] == "rem":
            print("rem")
            car.removeItem(self)

