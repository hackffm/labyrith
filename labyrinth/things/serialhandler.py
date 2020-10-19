from things.thing import Thing
import serial
from serial.tools.list_ports import comports
from time import sleep
from tornado import gen
import logging

_logger = logging.getLogger(__name__)

class SerialHandler(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.serials = {}

    def handle_message(self, msg, m):
        print("SerialHandler: " + msg)

    def write(self, ser, command):
        command = str(command) + '\r'
        ser.write(command.encode())

    def serial_read(self, ser):
        data = b''
        wait_bytes = ser.inWaiting()
        if wait_bytes == 0:
            return False
        #print(str(wait_bytes) + ' bytes waiting in serial port')
        _logger.debug(str(wait_bytes) + ' bytes waiting in serial port')
        for i in range(ser.inWaiting()):
            b = ser.read(1)
            if b != b'\r':
                if b == b'\n':
                    return data
                else:
                    data += b
        return False

    def find_my_things(self):
        ports = comports()
        if len(ports) == 0:
            print('no used ports found')
        for p in ports:
            if p.description == 'ttyAMA0':
                return
            print('write to ' + p.description + ' on port ' + p.device)
            ser = serial.Serial(p.device, 38400, )
            #self.serials.append(ser)
            self.write(ser, '0?')
            sleep(0.3)
            sr = self.serial_read(ser)
            if sr is False:
                break
            result = str(sr.decode())
            print('Serial result was ' + result)
            tids = result.split(";")
            mcuThing = self.labyrinth.get_thing(tids[0])
            mcuThing.setSerial(0, ser)
            self.serials[tids[0]] = mcuThing

            for i in range(1, len(tids)):
                tid = tids[i]
                print(tid)
                thing = self.labyrinth.get_thing(tid)
                if thing is not None:
                    thing.setSerial(i, ser)
                    mcuThing.addThing(i, thing)
                else:
                    print('SerialHandler: couldnt find ' + tid)
        self.loop()

    @gen.coroutine
    def loop(self):
        while True:
            yield gen.sleep(1)
            data = b''
            for tid in self.serials:
                data = self.serial_read(self.serials[tid].ser)
                if data is not False:
                    print(tid + " " + str(data))
                    thing = self.labyrinth.get_thing(tid)
                    thing.handleSerialMessage(data)
