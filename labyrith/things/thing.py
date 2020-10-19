class Thing:

    def __init__(self, labyrinth, tid):
        self.labyrinth = labyrinth
        self.tid = tid
        self.ser = None
        self.serid = None;

    def setSerial(self, serid, ser):
        self.serid = serid
        self.ser = ser

    def handleMessage(self, msg, m):
        print(msg)

    def handleSerialMessage(self, msg):
        print("handleSerialMessage: "+str(msg))