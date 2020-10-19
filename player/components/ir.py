from . import Component

class Ir(Component):

    def __init__(self, ser):
        self.ser = ser

    def handleMessage(self, message):
        print("Ir.handleMessage")
        if "code" in message:
            if(message["code"] == "simulation"):
                cmd = "Tp" + "\r"
                self.ser.write(cmd.encode())
        else:
            self.poll()

    def poll(self):
        cmd = "Tr" + "\r"
        self.ser.write(cmd.encode())