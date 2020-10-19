from things.thing import Thing

class Mcu(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.things = {}

    def addThing(self, nbr, thing):
        self.things[nbr] = thing

    def handleSerialMessage(self, msg):
        id = int(int(msg[0]))-48
        if id in self.things:
            thing = self.things[id]
            print('handeled from ' + thing.tid)
        else:
            print('couldnt find thing for serial message')