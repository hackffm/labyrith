from . import Component

class Base(Component):

    def handleMessage(self, message):
        print("Base.handleMessage")
        
        if "right" in message:
            self.moveRightLeft(message)
        elif "switchoff" in message:    
            cmd = "p!999" + "\r"
            self.ser.write(cmd.encode())
        else:
            print("no usefull command found")
    
    def moveRightLeft(self, message):
        cmd = "f" + str(message["right"]) + " " + str(message["left"]) + "\r"
        print("moveRightLeft: " + cmd)
        self.ser.write(cmd.encode())
