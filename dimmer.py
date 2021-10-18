from .client import *


class dimmer(client):

    def __init__(self, name: str = None, controller_type=None, methods: list = None,state:float = 0):
        self.state: int = state
        super().__init__(name, "dimmer", methods,state)
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def change_state(self,state):
        if state not in range(0,100):
            state = 0
        self.state = state