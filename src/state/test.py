import pygame as pg
import os 
import config as cf

from state.statet import State
import pygame as pg
import numpy as np
from sys import exit
import config as cf
from logic import perlin_noise, perlin_noise_3d
from pygame import gfxdraw
import noise


#https://openprocessing.org/@u315300/1776463#page-10

test_gride = [
    [1,0],
    [0,1]
]



def bilinear_interpolation(noise,x,y,z):
    #https://www.geeksforgeeks.org/maths/what-is-bilinear-interpolation/

    x1 = int(x)
    x2 = x1+1
    y1 = int(y)
    y2 = y1 + 1

    len_noise = len(noise)


    noise_value11 = noise[x1%len_noise][y1%len_noise][z]
    noise_value12 = noise[x1%len_noise][y2%len_noise][z]
    noise_value21 = noise[x2%len_noise][y1%len_noise][z]
    noise_value22 = noise[x2%len_noise][y2%len_noise][z]
    #print((x2-x1),(y2-y1))
    value = (
            noise_value11*((x2-x) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value21*((x-x1) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value12*((x2-x) * (y-y1) / (x2-x1) * (y2-y1)) +
            noise_value22*((x-x1) * (y-y1) / (x2-x1) * (y2-y1))
             )
    # change (x2-x1),(y2-y1) to 1 becasue alwasy 1
    return value


class Wave:
    def __init__(self,noise ,xStep,xFreq,yFreq,amplitude,velocity,height):
        self.xStep = xStep
        self.xFreq = xFreq
        self.yFreq = yFreq
        self.amplitude = 300
        self.velocity = velocity
        self.height = height

        self.points = []
        self.noise = noise
        self.counter = height

    def update(self):
        self.points = []

        for x in range(0,cf.WIDTH+self.xStep,self.xStep):
            self.points.append(self.point(x, self.counter))
        self.counter += 1

    def point(self,x,frame):
        if int(frame*self.velocity) > len(self.noise[0]):
            self.counter = 0

        noise = bilinear_interpolation(self.noise,x*self.xFreq,frame*self.velocity,int(self.height*self.yFreq))
        #print(type(noise),type(self.amplitude))
        y = self.height + noise*self.amplitude

        return x,y



class BackGround:
    def __init__(self):
        self.noise = perlin_noise_3d((100,100,100),(10,10,10))
        #print(self.noise)

        self.xStep = 10
        self.xFreq = 0.01
        self.yFreq = 0.05
        self.amplitude = 40,50
        self.velocity = 0.05
        self.waveCount = 6

        y = cf.HEIGHT/self.waveCount
        self.waves = []
        for wave in range(self.waveCount):
            self.waves.append(Wave(self.noise, self.xStep, self.xFreq,self.yFreq, self.amplitude, self.velocity, y*wave))

    def update(self):
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
                point.append((cf.WIDTH,cf.HEIGHT))
                point.append((0, cf.HEIGHT))
            else:
                point = point + list(reversed(self.waves[wave+1].points))
            gfxdraw.aapolygon(surface, point, cf.farger[cf.fargerKey[wave]])
            gfxdraw.filled_polygon(surface, point, cf.farger[cf.fargerKey[wave]])
            pg.draw.polygon(surface, cf.farger[cf.fargerKey[wave]], point)
            #pg.draw.lines(surface, (0,0,0),False, self.waves[wave].points, 6)
        pass

class Test(State):
    def __init__(self, app):
        super().__init__(app)
        self.back = BackGround()



        
    def update(self, action, actioHold):
        #print(action,actioHold)
        self.back.update()
        if action["left_duble_click"]:
            print("2")
        if action["left_click"]:
            print(1)
        if actioHold["left_click"]:
            print(3)


    def render(self, surface):
        self.back.draw(surface)
        #pg.draw.polygon(surface,(0,0,0),((100,100),(300,300),(100,50)))
        pass



"""
// Based on original sketch by Takawo(https: // openprocessing.org / sketch / 1615214)

let
simplex;
let
palette;

let
xStep = 10;
let
xFreq = 0.003;
let
yFreq = 0.005;
let
amplitude = 100;
let
velocity = 0.0001;
let
waveCount = 20;

function
setup()
{
    createCanvas(600, 600);
simplex = new
SimplexNoise();
palette = palettesList[floor(random(Object.keys(palettesList).length))];
noStroke();
}

function
draw()
{
    randomSeed(0);

let
c = shuffle(palette);
background(c[0]);

let
yStep = height / waveCount;

for (let y = 0; y <= height; y += yStep)
{
    push();
translate(0, y);
c = shuffle(palette);

let
gradient = drawingContext.createLinearGradient(0, height / 2, width, height / 2);
gradient.addColorStop(0, c[0]);
gradient.addColorStop(1, c[1]);
drawingContext.fillStyle = gradient;

beginShape();
for (let x = 0; x <= width; x += xStep)
{
    let
noise = simplex.noise3D(x * xFreq, y * yFreq, frameCount * velocity) * amplitude;
vertex(x, noise);
}
vertex(width, height);
vertex(0, height);
endShape(CLOSE);
pop();
}
}
"""