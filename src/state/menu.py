from state import State

from gui.buttons.Button import Button
import config as cf

import pygame as pg

class Menu(State):
    def __init__(self, app):
        super().__init__(app)
        buttonSize = (200,100)
        x_kordinatt_Knapp = cf.WIDTH/2 - buttonSize[0]/2
        self.buttons = [
            Button((x_kordinatt_Knapp,100),"Tilfeldig Spill", buttonsize=buttonSize, returnValue="tilfeldig"),
            Button((x_kordinatt_Knapp,250),"Level", buttonsize=buttonSize, returnValue="level"),
            Button((x_kordinatt_Knapp,400),"Instilinger", buttonsize=buttonSize, returnValue="instilinger"),
            Button((x_kordinatt_Knapp,550),"Avslutt", buttonsize=buttonSize, returnValue="avslutt")
        ]

    def update(self, action, actioHold):
        if action["left_click"]:
            pos = pg.mouse.get_pos()
            for button in self.buttons:
                match button.click(pos):
                    case "tilfeldig":
                        print("tilfeldig")
                        new_state = self.app.state_dict["game"](self.app)
                        new_state.enter_state()
                        self.app.rest_keys()
                        

                    case "level":
                        print("level")
                    case "instilinger":
                        print("instilinger") 
                    case "avslutt":
                        self.app.run = False
                    
                    
                

    
    def render(self, surface):
        for button in self. buttons:
            button.draw(surface)