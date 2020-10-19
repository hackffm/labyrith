from . import Component

class Light(Component):

    def handleMessage(self, message):
        print("Light.handleMessage")
    
        if(message["type"] == "white"):
            cmd = "Tw" + str(message["intensity"]) + "\r"
            print("white: " + cmd)
            self.ser.write(cmd.encode())
        elif(message["type"] == "uv"):
            cmd = "Tu" + str(message["intensity"]) + "\r"
            print("uv: " + cmd)
            self.ser.write(cmd.encode())
        elif(message["type"] == "color"):
            cmd = "Tc"+str(message["hex"]) + "\r"
            print("color: " + cmd)
            self.ser.write(cmd.encode())
        elif(message["type"] == "laser"):
            cmd = "Tl" + str(message["intensity"]) + "\r"
            print("laser: " + cmd)
            self.ser.write(cmd.encode())