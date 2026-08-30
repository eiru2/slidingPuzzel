import pygame as pg
import os 
import config as cf

from state.statet import State
import pygame as pg
import numpy as np
from sys import exit
import config as cf
from logic import perlin_noise


#https://openprocessing.org/@u315300/1776463#page-10

test_gride = [
    [1,0],
    [0,1]
]



def bilinear_interpolation(noise,x,y):
    #https://www.geeksforgeeks.org/maths/what-is-bilinear-interpolation/

    x1 = int(x)
    x2 = x1+1
    y1 = int(y)
    y2 = y1 + 1


    # edge case
    if x2 >= len(noise):
        x2 = 0
    if y2 >= len(noise[0]):
        y2 = 0

    noise_value11 = noise[x1][y1]
    noise_value12 = noise[x1][y2]
    noise_value21 = noise[x2][y1]
    noise_value22 = noise[x2][y2]
    value = (
            noise_value11*((x2-x) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value21*((x-x1) * (y2-y) / (x2-x1) * (y2-y1)) +
            noise_value12*((x2-x) * (y-y1) / (x2-x1) * (y2-y1)) +
            noise_value22*((x-x1) * (y-y1) / (x2-x1) * (y2-y1))
             )

    return value




class BackGround:
    def __init__(self):
        self.noise = perlin_noise(600,600,10)

        self.xStep = 10
        self.xFreq = 0.09
        self.yFreq = 0.005
        self.amplitude = 400
        self.velocity = 0.01
        self.waveCount = 20
        self.counter = 0

        self.points = []
        for x in range(0,cf.WIDTH,self.xStep):
            self.points.append(self.point(x, self.counter))

    def update(self):
        self.points = []

        for x in range(0,cf.WIDTH,self.xStep):
            self.points.append(self.point(x, self.counter))

        self.counter +=1





    def point(self,x,frame):
        if int(frame*self.velocity) > len(self.noise[0]):
            self.counter = 0

        noise = bilinear_interpolation(self.noise,x*self.xFreq,frame*self.velocity)*self.amplitude
        y = cf.HEIGHT/ 2+noise

        return x,y

    def draw(self,surface):
        #for point in self.points:

            #try: pg.draw.circle(surface,(0,0,0),point,5)
            #except:
            #    print(point)
             #   exit()

        pg.draw.polygon(surface,(0,0,0),self.points)
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