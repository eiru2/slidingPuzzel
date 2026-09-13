import pygame as pg
import numpy as np
import config as cf
from logic import perlin_noise_3d
from PIL import Image




def gradianRect(left_colour,middel_colour ,right_colour, points):
    colour_rect = pg.Surface( ( 3, 1 ) ,pg.SRCALPHA)                                   # tiny! 2x2 bitmap
    colour_rect.set_at((0, 0), left_colour)
    colour_rect.set_at((1, 0), middel_colour)# right colour line
    colour_rect.set_at((2, 0), right_colour)
    miny = min(points, key=lambda x: x[1])[1]
    maxy = max(points, key=lambda x: x[1])[1]
    return pg.transform.smoothscale(colour_rect, (cf.WIDTH*2, int(maxy - miny + 20))), miny  # stretch!

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
    r1 = coror1[0]*weight + coror2[0]*(1-weight)
    g1 = coror1[1]*weight + coror2[1]*(1-weight)
    b1 = coror1[2]*weight + coror2[2]*(1-weight)

    r2 = coror2[0]*weight + coror1[0]*(1-weight)
    g2 = coror2[1]*weight + coror1[1]*(1-weight)
    b2 = coror2[2]*weight + coror1[2]*(1-weight)
    return (r1,g1,b1), (r2,g2,b2)

def blend_colors(initial_color, final_color, amount):
    # Calc how much to add or subtract from start color
    r_diff = (final_color.r - initial_color.r) * amount
    g_diff = (final_color.g - initial_color.g) * amount
    b_diff = (final_color.b - initial_color.b) * amount

    # Create and return new color
    return pg.Color((int)(round(initial_color.r + r_diff)),
                        (int)(round(initial_color.g + g_diff)),
                        (int)(round(initial_color.b + b_diff)))

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

        for x in range(0,(cf.WIDTH)+self.xStep,self.xStep):
            self.points.append(self.point(x, self.counter))
        self.counter += 1

    def point(self,x,frame):
        if int(frame*self.velocity) > len(self.noise[0]):
            self.counter = 0

        #noise = bilinear_interpolation(self.noise,x*self.xFreq,frame*self.velocity,int(self.height*self.yFreq))
        #noise = self.noise[int( x * self.xFreq)][int(self.height * self.yFreq)][int(frame * self.velocity)%100]
        noise = trilinear_interpolation(self.noise, x * self.xFreq, self.height * self.yFreq, frame * self.velocity)
        #print(type(noise),type(self.amplitude))
        y = self.height + noise*self.amplitude

        return x,y

class ColorPicker:
    def __init__(self, imageFile):
        self.image = Image.open(imageFile)
        self.colorThreshold = 100

        self.color = []
        self.index = []
        self.p = []
        self.count_colors_2()


    def count_colors_2(self) -> list:  # no need to give colors
        colors_count_list = self.image.getcolors(maxcolors = 1000000000)
        #print(self.image.getcolors(maxcolors = 100000))
        sumOfPixel = 0
        for count, c_bgr in colors_count_list:
            if count > self.colorThreshold:
                sumOfPixel +=count

                #print('\tcolor {} appeared {} times'.format(c_bgr, count))
        i = 0
        for count, c_bgr in colors_count_list:
            if count > self.colorThreshold:
                self.color.append(c_bgr)
                self.index.append(i)
                self.p.append((count/sumOfPixel))
                i+=1
        return colors_count_list

    def randomColor(self,size):
        if size == 1:
            return  self.color[np.random.choice(self.index,p=self.p)]
        else:
            index = np.random.choice(self.index,p=self.p,size=size)
            list = []
            for i in range(size):
                list.append( self.color[index[i]])

            return  list





class BackGround:
    def __init__(self,imagePath):
        self.noise = perlin_noise_3d((150,150,150),(10,10,10))
        #print(self.noise)

        self.xStep = 20
        self.xFreq = 0.05
        self.yFreq = 0.5
        self.amplitude = 200
        self.velocity = 0.01
        self.waveCount = 5

        self.tempSurface = pg.Surface((cf.WIDTH, cf.HEIGHT),  pg.SRCALPHA)

        self.doPointsUpdate = True
        self.colorRect = []
        self.points = []
        self.x = 0

        self.colorPicker = ColorPicker(imagePath)

        self.rgb_color_trios = []
        for wave in range(self.waveCount):
            self.rgb_color_trios.append(self.colorPicker.randomColor(3))



        y = (cf.HEIGHT)/(self.waveCount-1)
        self.waves = []
        for wave in range(self.waveCount):
            self.waves.append(Wave(self.noise, self.xStep, self.xFreq,self.yFreq, self.amplitude, self.velocity, y*(wave-1)+y/3))

    def update(self):
        if self.doPointsUpdate:
            for wave in self.waves:
                wave.update()
            self.x-=1
            if self.x <= -cf.WIDTH:
                self.x = 0
                for image in range(len(self.waves)):
                    self.rgb_color_trios[image][0], self.rgb_color_trios[image][1] = self.rgb_color_trios[image][1],self.rgb_color_trios[image][2]
                    self.rgb_color_trios[image][2] = self.colorPicker.randomColor(1)
                    #self.waves[image].xOffset +=800

            self.colorRect = []
            i=0
            self.points = self.findPoints()
            for point in self.points:

                self.colorRect.append(gradianRect(self.rgb_color_trios[i][0],self.rgb_color_trios[i][1],self.rgb_color_trios[i][2], point))
                i+=1
            self.doPointsUpdate = False

    def findPoints(self):
        listOfpoint = []
        for wave in range(len(self.waves)):
            point = self.waves[wave].points
            if wave == len(self.waves) - 1:
                point.append((cf.WIDTH, cf.HEIGHT))
                point.append((0, cf.HEIGHT))

            else:
                point = point + list(reversed(self.waves[wave + 1].points))
            listOfpoint.append(point)
        return listOfpoint

    def gradientWaves(self,surface, colour_rect, points):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """

        pg.draw.polygon(self.tempSurface, (255, 255, 255, 255), points)
        colour_rect[0].blit(self.tempSurface, (-self.x, -colour_rect[1]), special_flags=pg.BLEND_RGBA_MIN)

        surface.blit(colour_rect[0], (self.x, colour_rect[1]))

    def drawGradian(self,surface):

        if not self.doPointsUpdate:
            i=0
            for point in self.points:
                #print(f"----------------{i}-------------------")
                #print(point)
                self.gradientWaves(surface, self.colorRect[i], point)
                i+=1
                self.tempSurface.fill((0,0,0,0))
            self.doPointsUpdate = not  self.doPointsUpdate