from things.thing import Thing
from tornado import gen
import pygame
import json
import logging

_logger = logging.getLogger(__name__)

class Ps3Handler(Thing):

    def __init__(self, labyrinth, tid, tidCar):
        super().__init__(labyrinth, tid)
        self.car = self.labyrinth.get_thing(tidCar)
        pygame.init()
        pygame.joystick.init()
        
        _logger.debug(pygame.joystick.get_count())
        
        joystick = pygame.joystick.Joystick(1)
        joystick.init()

    @gen.coroutine
    def loop(self):
        done = False
        while not done:
            for event in pygame.event.get():  # User did something.
                if event.type == pygame.QUIT:  # If user clicked close.
                    done = True  # Flag that we are done so we exit this loop.
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.handleButtons()
                elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                elif event.type == pygame.JOYAXISMOTION:
                    self.handleJoystick()

            yield gen.sleep(0.3)

    def handleButtons(self):
        print("Joystick button pressed.")
        joystick = pygame.joystick.Joystick(1)
        joystick.init()

        m = {}
        btTmp = -1
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            b = joystick.get_button(i)
            if b > 0:
                btTmp = i

            m["bt"] = btTmp

        msg = json.dumps(m)
        print(msg)

    def handleJoystick(self):
        #print("Joystick axis motion")
        j = pygame.joystick.Joystick(1)
        j.init()
        xaxis = round(j.get_axis(2), 2)
        yaxis = round(j.get_axis(3), 2)
        #print("x: " + str(xaxis) + "   y: " + str(yaxis))
        if (xaxis > 0.01 or xaxis < - 0.01) or (yaxis > 0.01 or yaxis < 0.01):
            left = round(yaxis + xaxis, 2)
            right = round(yaxis - xaxis, 2)
            m = {}
            m["component"] = "base"
            m["left"] = left
            m["right"] = right
            msg = json.dumps(m)
            self.car.handleMessage(msg, m)
            #print(msg)