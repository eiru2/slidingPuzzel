"""
continer
"""

class Div:
    def __init__(self, size:list, name:str, pos:list = [0,0]):
        self.pos = pos
        self.size = size
        
        self.name = name
        
        self.conten = {}
        
        # Flages
        self.resizing = False
    
    def resize(self, mousepos):
        pass
    
    def scale(self):
        """Make it evething in the div bigger
        """
        pass
    
    def addGuiElement(self, element):
        pass
    
    def removeGuiElemnet(self, element):
        pass
    
    def save(self):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        if self.resizing:
            pass