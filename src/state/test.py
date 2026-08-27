import pygame as pg
import os 
import config as cf

from state.statet import State
import pygame as pg




class Test(State):
    def __init__(self, app):
        super().__init__(app)
        image = pg.image.load('./Data/picture/tree.jpeg').convert_alpha()
        self.imageRect = image.get_rect()
        self.index = 0

        imageX, imageY = image.get_size()
        border = 10
        pg.transform.chop(image, (100, 100, 10, 10))
        imageOut = pg.Surface((imageX,imageY))
        imageOut.blit(image,(0,0))
        imageOut.fill((0,0,0),(border,border,imageX-border*2,imageY-border*2))
        imageOut.set_colorkey((0,0,0))



        imageInner = pg.Surface((imageX-border*2,imageY-border*2))
        imageInner.blit(image,(-border,-border))

        self.images = [image,imageOut ,imageInner]
        self.imagePos = [(0,0),(0,0),(border,border)]



        
    def update(self, action, actioHold):
        if action["arrow_left"]:
            self.index -=1

        if action["arrow_right"]:
            self.index +=1

    def render(self, surface):
        surface.blit(self.images[self.index], self.imagePos[self.index])
        pass

