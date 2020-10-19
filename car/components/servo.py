from . import Component

class Servo(Component):

    def handleMessage(self, message):
        print("Servo.handleMessage")
    
        if message["type"] == "v":
            cmd = "pv" + str(message["intensity"]) + "\r"
            print("vertical: " + cmd)
            self.ser.write(cmd.encode())
        elif message["type"] == "h":
            cmd = "ph" + str(message["intensity"]) + "\r"
            print("horizontal: " + cmd)
            self.ser.write(cmd.encode())