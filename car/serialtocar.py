import tornado.ioloop
from tornado.ioloop import PeriodicCallback

class SerialToCar():

    def __init__(self, app, ser):
        self.app = app
        self.ser = ser
        self.data = b''
        
    def start(self):
        serial_loop = tornado.ioloop.PeriodicCallback(self.readSerial, 30)
        serial_loop.start()

    def readSerial(self):
        #global data
        try:
            self.data
        except:
            self.data = b''
        for i in range(self.ser.inWaiting()):
            b = self.ser.read(1)
            if(b != b'\r'): 
                if(b == b'\n'):
                    if self.data:
                        print('msg from arduino: ', self.data)
                    #[con.write_message(data.decode("utf-8")) for con in WebSocketHandler.connections]
                    self.sendDataToLabyrinth(self.data)
                    self.data = b''
                else:
                    self.data += b

    def sendDataToLabyrinth(self, data):
        str = data.decode("utf-8") 
        tokens = str.split(';')
        if not tokens:
            print(tokens)
        for token in tokens:
            if token == '':
                return None
            print(token)
            if token.startswith('t'):
                self.app.ws.write_message('{ "tid":"ir", "car":"car1", "type":"t", "irid":"'+token[1:]+'"}')
            elif token.startswith('x'):
                self.app.ws.write_message('{ "tid":"ir", "car":"car1", "type":"x", "irid":"'+token[1:]+'"}')
