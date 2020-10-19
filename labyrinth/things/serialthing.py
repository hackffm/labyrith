from .thing import Thing


class SerialThing(Thing):

    def __init__(self, labyrinth, tid):
        self.labyrinth = labyrinth
        self.tid = tid
        self.ser = None

    def setSerial(self, ser):
        self.ser = ser


