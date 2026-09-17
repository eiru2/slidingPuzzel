from state import State

from gui import Button, InputboxInt, Text
import config as cf
from enum import Enum
import pygame as pg

class MenuState(Enum):
    choseSize = 0
    customChoser =1

class ChoseGrideSize(State):
    def __init__(self, app,imagePath):
        super().__init__(app)
        buttonSize = (200, 100)
        x_kordinatt_Knapp = cf.WIDTH / 2 - buttonSize[0] / 2

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
        self.state = MenuState.choseSize

        self.imagePath = imagePath
        print(imagePath,"     dfg")

    def choseSizeUpdate(self,action, actioHold):
        if action["left_click"]:
            pos = pg.mouse.get_pos()
            for button in self.buttonsChoseSize:
                match button.click(pos):
                    case "back":
                        self.exit_state()
                        self.app.rest_keys()
                    case "custumSize":
                        self.state = MenuState.customChoser
                        self.app.rest_keys()

                    case list():
                        print(button.returnValue)
                        new_state = self.app.state_dict["game"](self.app, button.returnValue, self.imagePath)
                        new_state.enter_state()
                        self.app.rest_keys()


    def customChoserUpdate(self,action, actioHold):
        for inputBox in self.inputBox:
            inputBox.update(action["textInput"])
        if action["left_click"]:
            pos = pg.mouse.get_pos()
            for inputBox in self.inputBox:
                inputBox.click(pos)
            for button in self.buttonsCustomChoser:
                match button.click(pos):
                    case "back":
                        self.state = MenuState.choseSize
                        for inputBox in self.inputBox:
                            inputBox.rest()
                        self.app.rest_keys()
                    case "startGame":
                        x = self.inputBox[0].returnInput()
                        y = self.inputBox[1].returnInput()
                        print(x,y)
                        if not x:
                            self.waringTextChooseSize.showText()
                        elif not y:
                            self.waringTextChooseSize.showText()
                        else:
                            new_state = self.app.state_dict["game"](self.app,(x,y),self.imagePath)
                            new_state.enter_state()
                            self.app.rest_keys()

    def update(self, action, actioHold):
        if self.state == MenuState.choseSize:
            self.choseSizeUpdate(action, actioHold)
        elif self.state == MenuState.customChoser:
            self.customChoserUpdate(action, actioHold)

    def render(self, surface):
        if self.state == MenuState.choseSize:
            for button in self.buttonsChoseSize:
                button.draw(surface)

        elif self.state == MenuState.customChoser:
            self.waringTextChooseSize.draw(surface)
            for button in self.buttonsCustomChoser:
                button.draw(surface)
            for inputBox in self.inputBox:
                inputBox.draw(surface)