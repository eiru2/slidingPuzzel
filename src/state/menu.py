from state import State


import config as cf

import pygame as pg

class Menu(State):
    def __init__(self, app):
        super().__init__(app)
        self.buttons = []

    def update(self, action, actioHold):
        print(f"{action}")
                

    
    def render(self, surface):
        self.menu.draw(surface)
        for button in self. buttons:
            button.draw(surface)