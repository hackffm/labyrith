import json
import tornado.websocket
from things.car import Car

# Is a connection endpoint of a websocket
# With on_message() you receive and with write_message() you can send messages
# Things that open a ws: player website, fpv-car
# If a message with the attribute 'init' is received, the handler gets assigned a thing instance
class WsHandler(tornado.websocket.WebSocketHandler):

    labyrinth = None;
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        print("A client connected from " + self.request.remote_ip)
        WsHandler.connections.add(self)

    def on_close(self):
        print("A client disconnected")
        WsHandler.connections.remove(self)

    def on_message(self, msg):
        print("WsHandler: msg: {}".format(msg))
        m = json.loads(msg)
        if 'init' in m:
            if m['tid'] == 'car':
                print("type car")
                cars = WsHandler.labyrinth.get_things("Car")
                for car in cars: 
                    print(car.tid)
                    if car.wshandler == None:
                        car.wshandler = self
                        car.hostname = m['hostname']
                        car.name = m['name']
                        return
            else:
                thing = WsHandler.labyrinth.get_thing(m['tid'])
                thing.wshandler = self
        else:
            WsHandler.labyrinth.handle_message(msg, m, None)
