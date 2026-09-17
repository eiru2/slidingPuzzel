from os.path import split

from state import State


from gui import Button, InputboxInt, Text
import config as cf
from os import listdir, PathLike
import pygame as pg
import random

class Menu(State):
    def __init__(self, app):
        super().__init__(app)
        buttonSize = (200,100)
        x_kordinatt_Knapp = cf.WIDTH/2 - buttonSize[0]/2
        self.buttonsMenu = [
            Button((x_kordinatt_Knapp,100),"Tilfeldig Spill", buttonsize=buttonSize, returnValue="tilfeldig"),
            Button((x_kordinatt_Knapp,250),"Level", buttonsize=buttonSize, returnValue="level"),
            Button((x_kordinatt_Knapp,400),"Instilinger", buttonsize=buttonSize, returnValue="instilinger"),
            Button((x_kordinatt_Knapp,550),"Avslutt", buttonsize=buttonSize, returnValue="avslutt")
        ]

        self.buttonsChoseSize = [
            Button((x_kordinatt_Knapp, 100), "3x3", buttonsize=buttonSize, returnValue=[3,3]),
            Button((x_kordinatt_Knapp, 250), "4x4", buttonsize=buttonSize, returnValue=[4,4]),
            Button((x_kordinatt_Knapp, 400), "5x5", buttonsize=buttonSize, returnValue=[5,5]),
            Button((x_kordinatt_Knapp, 550), "Custume", buttonsize=buttonSize, returnValue="custumSize"),
            Button((x_kordinatt_Knapp, 700), "Back", buttonsize=buttonSize, returnValue="back")
        ]

        self.buttonsCustomChoser = [
            Button((x_kordinatt_Knapp+110, 250), "Start", buttonsize=buttonSize, returnValue="startGame"),
            Button((x_kordinatt_Knapp-110, 250), "back", buttonsize=buttonSize, returnValue="back"),
        ]
        inputBoxSize = (100,100)
        self.inputBox = [
            InputboxInt((x_kordinatt_Knapp-50, 100), inputBoxSize, coler=(255, 255, 255), text="num x"),
            InputboxInt((x_kordinatt_Knapp+100, 100), inputBoxSize, coler=(255, 255, 255), text="num y")
        ]
        self.waringTextChooseSize = Text((x_kordinatt_Knapp,400), "wrong input", fontColor=(255,0,0), showText=False)

    def update(self, action, actioHold):
        if action["left_click"]:
            pos = pg.mouse.get_pos()
            for button in self.buttonsMenu:
                match button.click(pos):
                    case "tilfeldig":
                        paths = listdir(cf.imagePath)
                        new_state = self.app.state_dict["chooseGrideSize"](self.app, random.choice(paths))
                        new_state.enter_state()
                        self.app.rest_keys()
                    case "level":
                        print("level")
                    case "instilinger":
                        print("instilinger")
                    case "avslutt":
                        self.app.run = False


    def render(self, surface):
        for button in self.buttonsMenu:
            button.draw(surface)




