from . import Component
import os
import subprocess
import signal
from subprocess import check_output

class Cam(Component):

    def __init__(self, ser):
        self.sprocess = None
        self.pid = 0;

    def handleMessage(self, message):
        print("Cam.handleMessage")
        
        if "action" in message:
            if(message["action"] == "start"):
                print(message["action"])
                subprocess.call(['/home/pi/git/FPVCar/webserver_tornado/mjpg-streamer/cam.sh'], shell=True)

            if(message["action"] == "stop"):
                print(message["action"])
                pid = subprocess.check_output("ps -ef | grep [m]jpg | awk '{print $2}'", shell=True)
                print("pid: "+str(pid))
                os.kill(int(pid), signal.SIGTERM)
