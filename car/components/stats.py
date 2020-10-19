from . import Component

class Stats(Component):

    def __init__(self, ser):
        self.ser = ser

    def handleMessage(self, message):
        print("Stats.handleMessage")
        cmd = "V\r"
        print("fetch: " + cmd)
        self.ser.write(cmd.encode())
        cmd = "v\r"
        print("fetch: " + cmd)
        self.ser.write(cmd.encode())
