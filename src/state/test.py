import pygame as pg
import os 
import config as cf

from state.statet import State
import pygame as pg

class Shadow:
    def __init__(self,pos,image,shadowSize:int):
        """
        A class that add shadow to image
        Args:
             pos: postion to where the image is going be drawn (ignors shadows)
             image: The image that going get a shadow
             shadowSize(int): how long the shadows are in pixel values
        """
        self.pos = pos
        self.image = image
        self.shadowSize = shadowSize
        self.outliner = 5
        self.imageShadow = self.shadows()

    def shadows(self):
        """
        Create a shadow outliner plus a transpente sheet under the image
        """
        x,y = self.image.get_size()
        img = pg.Surface((x + self.shadowSize+self.outliner,
                               y + self.shadowSize+self.outliner), pg.SRCALPHA)
        img.fill((0,0,0,230),
                 (self.shadowSize,self.shadowSize,x+self.outliner,y+self.outliner))
        img.fill((0, 0, 0, 30),
                 (self.shadowSize,self.shadowSize, x,y))

        alph = 255//self.shadowSize
        for i in range(self.shadowSize):
            rectX = pg.Rect(self.shadowSize - i, 1, 1, y+self.shadowSize+self.outliner)
            recty = pg.Rect(1, self.shadowSize - i, x+self.shadowSize+self.outliner, 1)
            print(f"X: {rectX}, Y: {recty}  alpha: {255-(alph*i)}")
            img.fill((0, 0, 0, 255-(alph*i)), recty)
            img.fill((0,0,0,255-(alph*i)),rectX)

        img.blit(self.image,(self.shadowSize,self.shadowSize))
        return img

    def draw(self,surface):
        """
        Draw the image with outliner
        Args:
            surface: A pygame surface
        """
        surface.blit(self.imageShadow,(self.pos[0]-self.shadowSize,self.pos[1]-self.shadowSize))


class Test(State):
    def __init__(self, app):
        super().__init__(app)
        image = pg.image.load('./Data/picture/tree.jpeg').convert_alpha()
        self.imageRect = image.get_rect()
        self.index = 1

        imageX, imageY = image.get_size()
        border = 10
        pg.transform.chop(image, (100, 100, 10, 10))
        imageOut = pg.Surface((imageX,imageY), pg.SRCALPHA)
        imageOut.blit(image,(0,0))
        imageOut.fill((0,0,0,0),(border,border,imageX-border*2,imageY-border*2))
        #imageOut.set_colorkey((255,255,255))



        imageInner = pg.Surface((imageX-border*2,imageY-border*2))
        imageInner.blit(image,(-border,-border))

        self.images = [image,imageOut ,imageInner]
        self.imagePos = [(15,15),(15,15),(border+15,border+15)]

        self.renderImage = Shadow(self.imagePos[self.index],self.images[self.index],10)



        
    def update(self, action, actioHold):
        if action["arrow_left"]:
            self.index -=1
            self.renderImage = Shadow(self.imagePos[self.index], self.images[self.index], 10)

        if action["arrow_right"]:
            self.index +=1
            self.renderImage = Shadow(self.imagePos[self.index], self.images[self.index], 10)

    def render(self, surface):
        self.renderImage.draw(surface)
        #surface.blit(self.images[self.index], self.imagePos[self.index])


