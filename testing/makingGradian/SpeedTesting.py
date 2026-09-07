# Source - https://stackoverflow.com/a/62336993
# Posted by Kingsley, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-06, License - CC BY-SA 4.0

import pygame as pg
from src.gui.text.Drawtext import Text_FPS
import numpy as np
import time

# Window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400

### initialisation
pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Gradient Rect")


def gradientWaves(surface, left_colour, right_colour):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pg.Surface((2, 2), pg.SRCALPHA)  # tiny! 2x2 bitmap
    pg.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pg.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pg.transform.smoothscale(colour_rect, (WINDOW_WIDTH, 100)) # stretch!
    surface.blit(colour_rect, (0,150))

def r(surface, left_colour, right_colour):
    gradient_surf = pg.Surface((2, 1))
    gradient_surf.set_at((0, 0), left_colour)
    gradient_surf.set_at((1, 0), right_colour)

    colour_rect = pg.transform.smoothscale(gradient_surf, (WINDOW_WIDTH, 100)) # stretch!
    surface.blit(colour_rect, (0,150))

def colorInter(color1,color2, fraction):

    R = color1[0]*(1-fraction) + color2[0] *fraction
    G = color1[1]*(1-fraction) + color2[1] * fraction
    B = color1[2]*(1-fraction) + color2[2] * fraction
    return R,G,B

def rectGra(surface, left_colour, right_colour):
    surf = pg.Surface((WINDOW_WIDTH, 100))
    for x in range(WINDOW_WIDTH):
        color = colorInter(left_colour,right_colour,x/WINDOW_WIDTH)
        #print(color)
        pg.draw.line(surf, color ,(x,0),(x,100))
    surface.blit(surf,(0,150))


start = time.time()



### Main Loop
clock = pg.time.Clock()
FPScounter = Text_FPS((0,0), (f"Fps: {str(round(clock.get_fps(),2))}"))
fpsStore = []
finished = False
frameCounter = 0
start = time.time()
while not finished:

    # Handle user-input
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            finished = True

    # Update the window
    window.fill((0, 0, 0))
    gradientWaves(window,(255,0,0),(0,255,0))
    r(window,(255,0,0),(0,255,0))
    rectGra(window,(255,0,0),(0,255,0))
    # pygame.draw.polygon(window,(0,0,0),((100,100) , (200,100), (200,200)))

    # Clamp FPS
    clock.tick()
    fps = clock.get_fps()
    fpsStore.append(fps)
    FPScounter.update(fps)
    FPScounter.draw(window)
    frameCounter +=1
    if frameCounter%1000 == 0:
        print(frameCounter)
    if frameCounter >= 1:
        finished = True

    pg.display.flip()

end = time.time()
print(f"Total runtime of the program is {end - start} seconds")
print(f"FPS: {np.average(fpsStore)}")
pg.quit()
