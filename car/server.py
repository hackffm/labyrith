import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from tornado import gen
from tornado.ioloop import PeriodicCallback
import serial
import _thread
import pygame
import socket
import json
from components import *
import asyncio
from tornado.websocket import websocket_connect
import toml
import time
from serialtocar import SerialToCar
import logging

print("       .__                             ")
print("______ |  | _____  ___.__. ___________ ")
print("\____ \|  | \__  \<   |  |/ __ \_  __ \\")
print("|  |_> >  |__/ __ \\___  \  ___/|  | \/")
print("|   __/|____(____  / ____|\___  >__|   ")
print("|__|             \/\/         \/      ")
print("")

try:
    config = toml.load('config.toml')
except FileNotFoundError as e:
    print("Config file 'config.toml' not found.")
    print("Please make a copy of the 'config.template.toml' and name it config.toml.")
    exit(1)
    
logging.basicConfig(level=logging.DEBUG)
    
ser = serial.Serial('/dev/ttyS0', 38400)
hostname = socket.gethostname()
print("serial:   " + ser.name)
print("hostname: " + hostname)
print("")

pygame.mixer.init(44100, -16, 1, 1024)

components = {
    "base": Base(ser),
    "sound": Sound(ser),
    "cam": Cam(ser),
    "stats": Stats(ser),
    "light": Light(ser),
    "servo": Servo(ser),
    "ir": Ir(ser)
}
       
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)
        print('new connection was opened')
        pass

    def on_message(self, message):
        print ('from WebSocket: ', message)
        m = json.loads(message)
        component = components[m["component"]]
        component.handleMessage(m)

    def on_close(self):
        self.connections.remove(self)
        print('connection closed')
        pass

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_neu.html", hostname=hostname)
        
class CssPageHandler(tornado.web.RequestHandler):  
    def get(self):
        self.set_header("Content-Type", 'text/css')
        self.render("style.css", hostname=hostname)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/style.css', CssPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})
        ]
        settings = {
            'autoreload': True,
            'debug': True,
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.ws = None
        self.connectToLabyrinth()
        PeriodicCallback(self.poll_ir, 2000).start()
        
    def poll_ir(self):
        component = components["ir"]
        component.poll()
        
    @gen.coroutine
    def connectToLabyrinth(self):
        log = logging.getLogger("ws labyrith")
        url = "ws://"+config.get('labyrint_host_name')+":3000/ws"
        while True:
            log.info("trying to connect to labyrinth ("+url+")")
            try:
                self.ws = yield websocket_connect(url)
            except Exception:
                log.info("connection error")
            else:
                log.info("connected")
                self.ws.write_message('{ "tid": "car", "name": "schokomobil", "hostname":"'+hostname+'", "init":"true" }')
                break
            time.sleep(10)
            
        self.receiverLoop()

    @gen.coroutine
    def receiverLoop(self):
        log = logging.getLogger("ws labyrith receiver")
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                log.debug("verbindung abgebrochen")
                self.connectToLabyrinth()
                return
            log.debug(msg)
            try:
                m = json.loads(msg)
            except Exception:
                log.debug("no json")
            else: 
                component = components[m["component"]]
                component.handleMessage(m)
                if msg is None:
                    log.debug("connection to labyrinth closed")
                    self.ws = None
                    break

if __name__ == '__main__':
    ser.flushInput()
    ws_app = Application()

    #_thread.start_new_thread(serial.readSerial, ())
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9090)
    loop = tornado.ioloop.IOLoop.instance()
    serial = SerialToCar(ws_app, ser)
    serial.start()
    #serial_loop = tornado.ioloop.PeriodicCallback(serial.readSerial, 30)
    #serial_loop.start()    
    loop.start()
