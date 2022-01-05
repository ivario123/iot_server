import json
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
import datetime


def encode(list):
    if type(list) is dict:
        print(list)
        js = "{"
        for key in list.keys():
            print(key)
            js = js +f"\"{key}\" : "+json.dumps(list[key],default=lambda o:o.toJSON())+",\n"
        js = js[:len(js)-2]+"}"
        return js
    return json.dumps(list,default=lambda o:o.toJSON())

class client():
    def __init__(self, name: str = None, controller_type=None,
                 methods: list = None,state=None, owner = None):
        self.name = name
        self.owner = owner
        self.type = controller_type
        self.active = True
        self.last_checkin = datetime.datetime.now().__str__()
        if methods == None:
            self.methods = ["toggle"]
        else:
            self.methods = methods
        self.state = state
    def correct_owner(self, owner):
        return self.owner == owner
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __repr__(self):
        return f"{self.name} : {self.type}  : {self.state}"

    def inactivate(self):
        self.active = False
    def change_state(self,state):
        self.state = state
class dimmer(client):

    def __init__(self, name: str = None, controller_type=None, methods: list = None,state:float = 0,
    owner:str = None):
        self.state: int = state
        super().__init__(name, "dimmer", methods,state,owner = owner)
    def change_state(self,state):
        if state not in range(0,100):
            state = 0
        self.state = state

class moisture_sensor(client):

    def __init__(self, name: str = None, controller_type=None, methods: list = None,state:float = 0,
    owner:str = None):
        self.state: int = state
        super().__init__(name, "moisture_sensor", methods,state,owner = owner)
    def change_state(self,state):
        if state not in range(0,100):
            state = 0
        self.state = state
    def __repr__(self):
      return f"Soil moisture = {self.state}"

class switch(client):

    def __init__(self, name: str = None, controller_type=None, methods: list = None,state:int = 0,
    owner:str = None):
        self.state: int = state
        super().__init__(name, "switch", methods,state,owner = owner)
    def change_state(self,state):
        if state is not 1:
            state = 0
        self.state = state



device_types = {
    "switch":  switch,    # The switch class,
    "dimmer":  dimmer,    # The dimmer class,
    "moisture_sensor": moisture_sensor, #The moisture sensor class
    "client": client,     # The base class for clients
    "": client            # ...
}