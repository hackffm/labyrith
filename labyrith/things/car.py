from things.thing import Thing

class Car(Thing):

    def __init__(self, labyrinth, tid):
        super().__init__(labyrinth, tid)
        self.wshandler = None
        self.items = {}
        self.ctrl = None
        self.hostname = None
        self.name = None

    def handleMessage(self, msg, m):
        print(str(self.tid) + ": " + msg)
        if self.wshandler is not None:
            self.wshandler.write_message(msg)

    def addItem(self, item):
        print("Car.addItem: " + item.tid)
        if item.tid in self.items:
            return
        self.items[item.tid] = item
        self.ctrl.handleMessage('{ "component": "items", "action":"add", "item": "'+item.tid+'"}', None)

    def removeItem(self, item):
        if self.items.pop(item.tid, None) is not None:
            self.ctrl.handleMessage('{ "component": "items", "action":"rem", "item": "'+item.tid+'"}', None)

    def useItem(self, item):
        print("car: useItem: " + item.tid)
        #self.ctrl.handleMessage('{ "component": "items", "action":"use", "item": "'+item.tid+'"}', None)
        if item.tid in self.items:
            return True
        return False
