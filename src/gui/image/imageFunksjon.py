import pygame as pg

def imageFram(image, border):
    imageX,imageY = image.get_size()
    imageOut = pg.Surface((imageX,imageY), pg.SRCALPHA)
    imageOut.blit(image, (0, 0))
    imageOut.fill((0, 0, 0, 0), (border, border, imageX - border * 2, imageY - border * 2))
    return  imageOut

def imageBorderCut(image, border):
    imageX, imageY = image.get_size()
    imageInner = pg.Surface((imageX - border * 2, imageY - border * 2))
    imageInner.blit(image, (-border, -border))
    return imageInner