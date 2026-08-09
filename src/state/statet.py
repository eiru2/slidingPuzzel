class State:
    def __init__(self,app):
        """Konstruktvere for staten. 
        Her er atributer for staten

        Args:
            game (objekt): Helle spille objekte
        """
        self.app = app
        self.prev_state = None
        
    
    def update(self,action,actioHold):
        """for å updater game staten

        Args:
            action (dict): input for user

        """
        pass
    
    def render(self,surface):
        """Tegner staten

        Args:
            surface (pg.surface): Hvor state blir tegenr
        """
        
        pass
    
    def enter_state(self):
        """Gå in i en nye state
        """
        if len(self.app.state_stack) >= 1:
            self.prev_state = self.app.state_stack[-1]
        self.app.state_stack.append(self)

    def exit_state(self):
        """Går ut av en state
        """
        self.app.state_stack.pop()