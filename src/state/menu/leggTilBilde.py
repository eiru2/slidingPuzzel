from state import State
from PIL import Image
import json
import numpy as np
import pygame as pg
import os
import skimage
from scipy.spatial import cKDTree

from gui import Button, InputboxInt, Text
import config as cf
from enum import Enum

"""
Jsson:
MainColor

"""

Path = ("Data/testBilder/")

class ColorColtion:
    def __init__(self, colorLab, colorRGB, count):
        self.count = count
        self.colors = [colorLab]
        self.baseColor = colorRGB
        self.baseColorLab = colorLab
        #print(self.baseColorLab)
        self.treshold = 20

    def addColor(self,colorLab,count):
        self.colors.append(colorLab)
        self.count +=count


    def isColorSimilar(self,color):
        return ((color[0]-self.baseColorLab[0])**2 + (color[1]-self.baseColorLab[1])**2 +(color[2]-self.baseColorLab[2])**2 )**0.5
        # print(color)    # Convert tuples/lists to NumPy arrays for vectorized operations
        # c = np.array(color_lab, dtype=np.int16)
        # base = np.array(self.baseColor, dtype=np.int16)

        # Check if all channel differences are within the threshold
        # return np.all(((c[0]-base[0])**2 + (c[1]-base[1])**2 +(c[2]-base[2])**2 )**0.5 <= self.treshold)

    def returnColorAndCount(self):
        return self.baseColor, self.count


class ImageManger:
    def __init__(self, imageFile):
        self.imagePil = Image.open(imageFile)
        self.imagePil = self.imagePil.convert("RGB")
        self.imagePygame = pg.image.load(imageFile).convert()
        self.colorThreshold = 0.001 / 100

        self.color = []
        self.index = []
        self.p = []
        self.count_colors_2()


    def count_colors_2(self) -> list:  # no need to give colors
        #print(self.imagePil.getcolors(maxcolors = 100000))
        pixel_amount = self.imagePil.size[0]*self.imagePil.size[1]
        colors_count_list = self.imagePil.getcolors(maxcolors = pixel_amount)
        sumOfPixel = 0
        print("First", colors_count_list[0])
        i = []
        # lab = skimage.color.rgb2lab(colors_count_list[1])
        # print(lab[0])
        for count, c_bgr in colors_count_list:
            r = c_bgr[0]/255
            g = c_bgr[1] / 255
            b = c_bgr[2] / 255
            lab = skimage.color.rgb2lab((r,g,b))
            i.append((count,lab,c_bgr))
            # lab_coords.append(lab)
        print(i[0])
        colors_count_list = i

        print(len(colors_count_list))
        # colors_count_list.sort(key=lambda x: x[0], reverse=True)
        # print(colors_count_list)

        tree = None

        DISTANCE_THRESHOLD = 20
        arryOfColor = []
        lab_coords = []

        for count, c_Lab, c_rgb in colors_count_list:
            allReadyInList = False

            # If we have items in our tree, perform a fast spatial lookup
            if tree is not None:
                # Find the nearest color within your threshold distance
                # distance_upper_bound stops searching early if no color is close
                dist, index = tree.query(c_Lab, distance_upper_bound=DISTANCE_THRESHOLD)
                # print(dist)

                # dist will be infinity if no match is found within the threshold
                if dist < float('inf'):
                    arryOfColor[index].addColor(c_Lab, count)
                    allReadyInList = True

            if not allReadyInList:
                # Create your custom collection object
                new_collection = ColorColtion(c_Lab, c_rgb, count)
                arryOfColor.append(new_collection)
                lab_coords.append(c_Lab)
                tree = cKDTree(lab_coords)


                # Rebuild the tree with the new coordinate (fast operation for small-to-medium sets)


        # for count, c_Lab, c_rgb in colors_count_list:
        #     # if count > self.colorThreshold * pixel_amount:
        #         allReadyInList = False
        #         for color in arryOfColor:
        #             if color.isColorSimilar(c_Lab):
        #                 color.addColor(c_Lab, count)
        #                 allReadyInList = True
        #                 break
        #
        #         if not allReadyInList:
        #             arryOfColor.append(ColorColtion(c_Lab,c_rgb,count))
        print("secesf")
        newList = []
        for colorColtion in arryOfColor:
            if colorColtion.count >  self.colorThreshold * pixel_amount:
                sumOfPixel += colorColtion.count
                newList.append(colorColtion)

        print("third")
        i = 0
        for colorColtion in newList:
            color, count = colorColtion.returnColorAndCount()
            self.color.append(color)
            self.index.append(i)
            if sumOfPixel > 0:
                self.p.append(count / sumOfPixel)
            else:
                self.p.append(0.0)
            i+=1

        print(self.color)

            # if count > self.colorThreshold*pixel_amount:
            #     sumOfPixel +=count
            #     if count < leastColor:
            #         print(c_bgr, count)
            #         leastColor = count


                #print('\tcolor {} appeared {} times'.format(c_bgr, count))
        # i = 0
        # for count, c_bgr in colors_count_list:
        #     if count > self.colorThreshold:
        #         self.color.append(c_bgr)
        #         self.index.append(i)
        #         self.p.append((count/sumOfPixel))
        #         i+=1
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

    def saveImage(self, name):
        saveDict = {}

        self.count_colors_2()
        saveDict["Color"] = self.color
        saveDict["ColorProblty"] = self.p

        if not os.path.exists((Path + name)):
            os.makedirs(Path + name)

        with open(Path + name+"/ImageData.json", 'w') as f:
            json.dump(saveDict, f)
            f.close()

    def loadImage(self):
        pass

    def draw(self,surface):
        size = int(np.ceil(len(self.color)**0.5))
        # print(size,len(self.color),len(self.color)**0.5)
        img = pg.Surface((size,size),pg.SRCALPHA)
        i = 0

        for x in range(size):
            for y in range(size):
                if not i > len(self.color)-1:
                    # print(i)
                    img.set_at((x,y),self.color[i])
                    i +=1
        img = pg.transform.scale(img,surface.get_size())
        surface.blit(img,(0,0))



class SaveImage(State):
    def __init__(self, app):
        super().__init__(app)
        self.image = None
        self.imageRecived = False

    def update(self, action, actioHold):
        #print(self.app.dropFile)
        if self.app.dropImported:
            self.image = ImageManger(self.app.dropFile)
            self.app.dropImported = False
            self.imageRecived = True
        if action["left_click"] and self.image:
            self.image.saveImage("Test")

    def render(self, surface):
        if self.image:
            surface.blit(self.image.imagePygame, (0,0))
            self.image.draw(surface)
