from things.thing import Thing

class IridThing(Thing):

    def __init__(self, labyrinth, tid, irid):
        super().__init__(labyrinth, tid)
        self.irid = irid
