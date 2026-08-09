import pygame as pg
import config as cf

class LeftClick:
    def __init__(self):
        pass
    
    def click(self, app):
        
        #  print(app.timer)
        
        if app.timer > cf.TresholdDubleClik and app.timer < cf.TrasholdHolde and app.clickCunter >= 2  :
            app.input["left_duble_click"] = True
            app.clickCunter = 0
            
        elif app.timer > cf.TresholdDubleClik and app.timer < cf.TrasholdHolde and app.clickCunter == 1 and not app.clicked :
            app.input["left_click"] = True
            app.clickCunter = 0

        if app.timer > cf.TrasholdHolde:
            app.inputHold["left_click"] = True
            
        if app.timer > cf.TresholdDubleClik and not app.clicked:
            app.timer = 0
            app.time = False
        # app.clickCunter = 0


