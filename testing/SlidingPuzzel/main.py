import pygame as pg
import sys
from noisePerlin import perlin_noise_3d
from Drawtext import Text_FPS
import fast_noise

import multiprocessing
from concurrent.futures import ThreadPoolExecutor

# Initialize Pygame
pg.init()

# Set up the display
WIDTH, HEIGHT =800, 600
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("My Pygame Window")

def gradientWaves( window, left_colour, right_colour, points, wave_y ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pg.Surface( ( 2, 2 ) ,pg.SRCALPHA)                                   # tiny! 2x2 bitmap
    pg.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pg.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    miny = min(points, key=lambda x: x[1])[1]
    maxy = max(points, key=lambda x: x[1])[1]
    colour_rect = pg.transform.smoothscale( colour_rect, ( WIDTH, int(maxy-miny+50)) )  # stretch!

    mask_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

# Define your polygon points (relative to the image size)
    pg.draw.polygon(mask_surface, (255, 255, 255, 255), points)
    
    colour_rect.blit(mask_surface, (0, -miny), special_flags=pg.BLEND_RGBA_MIN)
    
    window.blit( colour_rect, (0,miny) )

def trilinear_interpolation(noise,x,y,z):
    #https://www.geeksforgeeks.org/maths/what-is-bilinear-interpolation/
    len_noise = len(noise)

    x0 = int(x)%len_noise
    x1 = (x0 + 1)%len_noise
    y0 = int(y)%len_noise
    y1 = (y0 + 1)%len_noise
    z0 = int(z)%len_noise
    z1 = (z0 + 1)%len_noise



    noise_value000 = noise[x0][y0][z0]
    noise_value010 = noise[x0][y1][z0]
    noise_value100 = noise[x1][y0][z0]
    noise_value110 = noise[x1][y1][z0]

    noise_value001 = noise[x0][y0][z1]
    noise_value011 = noise[x0][y1][z1]
    noise_value101 = noise[x1][y0][z1]
    noise_value111 = noise[x1][y1][z1]
    #print((x2-x1),(y2-y1))
    xd = x % 1
    yd = y % 1
    zd = z % 1

    value = (
                noise_value000*(1 - xd)*(1 - yd)*(1 - zd) +
                noise_value100 * xd * (1 - yd) * (1 - zd) +
                noise_value010 * (1 - xd) * yd * (1 - zd) +
                noise_value110 * xd * yd * (1 - zd) +
                noise_value001 * (1 - xd) * (1 - yd) * zd +
                noise_value101 * xd * (1 - yd) * zd +
                noise_value011 * (1 - xd) * yd * zd +
                noise_value111 * xd * yd * zd
             )
    # change (x2-x1),(y2-y1) to 1 becasue alwasy 1
    return value

def bilinear_interpolation(noise,x,y,z):
    #https://www.geeksforgeeks.org/maths/what-is-bilinear-interpolation/

    x1 = int(x)
    x2 = x1+1
    y1 = int(y)
    y2 = y1 + 1
    z1 = int(z)
    z2 = z1 + 1

    len_noise = len(noise)


    noise_value110 = noise[x1%len_noise][y1%len_noise][z1%len_noise]
    noise_value120 = noise[x1%len_noise][y2%len_noise][z1%len_noise]
    noise_value210 = noise[x2%len_noise][y1%len_noise][z1%len_noise]
    noise_value220 = noise[x2%len_noise][y2%len_noise][z1%len_noise]
    #print((x2-x1),(y2-y1))
    value = (
            noise_value110*((x2-x) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value210*((x-x1) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value120*((x2-x) * (y-y1) / (x2-x1) * (y2-y1)) +
            noise_value220*((x-x1) * (y-y1) / (x2-x1) * (y2-y1))
             )
    # change (x2-x1),(y2-y1) to 1 becasue alwasy 1
    return value

def colorTransform(colors,weight):
    coror1 = colors[0]
    coror2 = colors[1]
    r = coror1[0]*weight + coror2[0]*(1-weight)
    g = coror1[1]*weight + coror2[1]*(1-weight)
    b = coror1[2]*weight + coror2[2]*(1-weight)
    return r,g,b

class Wave:
    def __init__(self,noise ,xStep,xFreq,yFreq,amplitude,velocity,height):
        self.xStep = xStep
        self.xFreq = xFreq
        self.yFreq = yFreq
        self.amplitude = amplitude
        self.velocity = velocity
        self.height = height

        self.points = []
        self.noise = noise
        self.counter = height

    def update(self):
        self.points = []
        args = []
        if int(self.counter*self.velocity) > len(self.noise[0]):
            self.counter = 0
            
        temp = []
        for x in range(0,(WIDTH)+self.xStep,self.xStep):
            self.points.append(self.point(x))
           # temp.append(x)
          #  if x%500 == 0:
           #    ¤ args.append(temp)

                
       # ¤args.append(temp)

        #with ThreadPoolExecutor() as executor:
         #   result = list(executor.map(self.point, args))
        #for r in result:
        #    self.points = self.points +r
        # with multiprocessing.Pool(10) as p:
        #     multiprocessing.freeze_support()
        #     p.map(self.point, args)
        self.counter += 1

    def point(self,x):

        #noise = bilinear_interpolation(self.noise,x*self.xFreq,frame*self.velocity,int(self.height*self.yFreq))
        #noise = self.noise[int( x * self.xFreq)][int(self.height * self.yFreq)][int(frame * self.velocity)%100]

        #noise = fast_noise.trilinear_interpolation(self.noise, x * self.xFreq, self.height * self.yFreq, self.counter * self.velocity)
        noise = trilinear_interpolation(self.noise, x * self.xFreq, self.height * self.yFreq,
                                                   self.counter * self.velocity)
        #print(type(noise),type(self.amplitude))
        y = self.height + noise*self.amplitude


        return x,y

rgb_color_pairs = [
    ((0, 0, 0), (255, 255, 255)),        # Black & White
    ((10, 25, 47), (100, 255, 218)),     # Dark Navy & Teal/Cyan
    ((26, 54, 93), (144, 205, 244)),     # Navy Blue & Light Blue
    ((45, 55, 72), (237, 242, 247)),     # Charcoal & Off-White
    ((74, 21, 75), (244, 237, 177)),     # Deep Plum & Soft Yellow
    ((13, 92, 58), (209, 231, 221)),     # Forest Green & Mint
    ((49, 20, 50), (232, 167, 161)),     # Dark Purple & Dusty Rose
    ((17, 24, 39), (243, 244, 246)),     # Dark Gray & Light Gray
    ((44, 22, 84), (181, 126, 220)),     # Violet & Lavender
    ((0, 75, 73), (255, 107, 107))       # Deep Teal & Coral
]


class BackGround:
    def __init__(self):
        self.noise = perlin_noise_3d((100,100,100),(10,10,10))
        #print(self.noise)

        self.xStep = 40
        self.xFreq = 0.01
        self.yFreq = 0.1
        self.amplitude = 70
        self.velocity = 0.01
        self.waveCount = 5



        y = (HEIGHT)/self.waveCount
        self.waves = []
        for wave in range(self.waveCount):
            self.waves.append(Wave(self.noise, self.xStep, self.xFreq,self.yFreq, self.amplitude, self.velocity, y*wave))

    def update(self):
        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     # Submit the target method for each class instance in the list
        #     futures = [executor.submit(obj.update) for obj in self.waves]
            
        # [future.result() for future in futures]
        #print(self.waves[0].points)
        for wave in self.waves:
            wave.update()

    def draw(self,surface):
        #for point in self.points:

            #try: pg.draw.circle(surface,(0,0,0),point,5)
            #except:
            #    print(point)
             #   exit()
        for wave in range (len(self.waves)):
            point = self.waves[wave].points

            if wave == len(self.waves)-1:
                point.append((WIDTH,HEIGHT))
                point.append((0, HEIGHT))

            else:
                point = point + list(reversed(self.waves[wave+1].points))
            #gfxdraw.aapolygon(surface, point, cf.farger[cf.fargerKey[wave]])
            #gfxdraw.filled_polygon(surface, point, cf.farger[cf.fargerKey[wave]])
            pg.draw.polygon(surface, farger[fargerKey[wave]], point)
            #pg.draw.lines(surface, (0,0,0),False, self.waves[wave].points, 6)
        pass

    def drawGradian(self,surface):
        # for wave in range(len(self.waves)):
        #     lenOfpoints = len(self.waves[wave].points)-1
        #     for point in range(lenOfpoints):
        #         points = 0
        #         if wave == len(self.waves) - 1:
        #             points = (self.waves[wave].points[point], self.waves[wave].points[point + 1],
        #                       (self.waves[wave].points[point+1][0],HEIGHT), (self.waves[wave].points[point][0],HEIGHT))
        #         else:
        #             points = (self.waves[wave].points[point], self.waves[wave].points[point+1], self.waves[wave+1].points[point+1], self.waves[wave+1].points[point])
        #         pg.draw.polygon(surface, colorTransform(rgb_color_pairs[wave],point/lenOfpoints), points)
        
        for wave in range (len(self.waves)):
            point = self.waves[wave].points

            if wave == len(self.waves)-1:
                point.append((WIDTH,HEIGHT))
                point.append((0, HEIGHT))
            
            else:
                point = point + list(reversed(self.waves[wave+1].points))
            gradientWaves(surface, rgb_color_pairs[wave][0],rgb_color_pairs[wave][1], point,self.waves[wave].height)

clock =  pg.time.Clock()
FPScounter = Text_FPS((0,0), (f"Fps: {str(round(clock.get_fps(),2))}"))

def showFPS(surface):
    FPScounter.update(clock.get_fps())
    FPScounter.draw(surface)
    
color1 = (255,0,0)
color2 = (255,0,0)
test = BackGround()
# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    test.update()
    # Fill the screen with a black background
    screen.fill((0, 0, 0))
    test.drawGradian(screen)
    showFPS(screen)

    # Update the display
    pg.display.flip()
    clock.tick(0)

pg.quit()
sys.exit()