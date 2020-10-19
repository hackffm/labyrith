from things.thing import Thing

class RfidThing(Thing):

    def __init__(self, labyrinth, tid, rfid):
        super().__init__(labyrinth, tid)
        self.rfid = rfid
