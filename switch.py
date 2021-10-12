from .client import *


class switch(client):

    def __init__(self, name: str = None, controller_type=None, methods: list = None,state:int = 0):
        self.state: int = state
        super().__init__(name, "switch", methods,state)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)