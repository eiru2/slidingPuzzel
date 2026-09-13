import pygame as pg
import random
from PIL import Image
import time
import numpy as np

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400

### initialisation
pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Gradient Rect")


class ColorPicker:
    def __init__(self, imageFile):
        self.image = Image.open(imageFile)
        self.colorThreshold = 100

        self.color = []
        self.index = []
        self.p = []
        self.count_colors_2()


    def count_colors_2(self) -> list:  # no need to give colors
        start_time = time.time()
        colors_count_list = self.image.getcolors(maxcolors = 1000000000)
        print(self.image.getcolors(maxcolors = 100000))
        print('count_colors_2 time elapsed: {:.10f}s'.format(time.time() - start_time))

        sumOfPixel = 0
        for count, c_bgr in colors_count_list:
            if count > self.colorThreshold:
                sumOfPixel +=count

                print('\tcolor {} appeared {} times'.format(c_bgr, count))
        i = 0
        for count, c_bgr in colors_count_list:
            if count > self.colorThreshold:
                self.color.append(c_bgr)
                self.index.append(i)
                self.p.append((count/sumOfPixel))
                i+=1
        return colors_count_list

    def randomColor(self):
        return  self.color[np.random.choice(self.index,p=self.p)]




clock = pg.time.Clock()
test = ColorPicker("picture.png")
finished = False
color = (0, 0, 0)
while not finished:

    # Handle user-input
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            finished = True

        if event.type == pg.MOUSEBUTTONDOWN:
            color = test.randomColor()
            print(color)

    # Update the window
    window.fill(color)
    # pygame.draw.polygon(window,(0,0,0),((100,100) , (200,100), (200,200)))

    # Clamp FPS
    clock.tick()
    pg.display.flip()



pg.quit()
