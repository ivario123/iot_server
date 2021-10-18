import json
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder

class client_encoder(JSONEncoder):
    def default(self, o):
            return o.__dict__

class client():
    def __init__(self, name: str = None, controller_type=None,
                 methods: list = None,state=None):
        self.name = name
        self.type = controller_type
        self.active = True
        if methods == None:
            self.methods = ["toggle"]
        else:
            self.methods = methods
        self.state = state
    def __repr__(self):
        return f"{self.name} : {self.type} : {self.ip} : {self.methods}"

    def inactivate(self):
        self.active = False
    def change_state(self,state):
        self.state = state
