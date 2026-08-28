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