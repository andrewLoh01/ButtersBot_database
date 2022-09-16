import json
from json import JSONEncoder

class switchEncoder(JSONEncoder):
    def default(self, object):
        return object.__dict__
        
class switch:
    def __init__(self, switchType):
        self.switchType = switchType
        self.links = {}
        
    def get_switchType(self):
        return self.switchType
    
    def set_swithType(self, switchType):
        self.switchType = switchType
        return f"Set to {switchType} switches"
        
    def get_allLinks(self):
        return self.link
    


            

        

    


