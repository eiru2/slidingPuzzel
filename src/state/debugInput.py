from state import State


import config as cf

import pygame as pg

class InputDebuger(State):
    def __init__(self, app):
        super().__init__(app)
        self.test = False
        self.frame = 0
        self.preList = None

    def update(self, action, actioHold):
        # the action to test
        # if action["left_duble_click"]:
        #     self.test = not self.test
        
        if action["left_click"]:
            self.test = not self.test
        if self.frame >= 160 or not self.preList == action :
            print(f"input: {action}, input Hold: {actioHold} Test; {self.test} game {self.app.clickCunter} timer: {self.app.timer}")
            # print(self.preList == action)
            self.frame = 0
        self.preList = action.copy()
        self.frame +=1

        
        
        
                
    def render(self, surface):
        pass