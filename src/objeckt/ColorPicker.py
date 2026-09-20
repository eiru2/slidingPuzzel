from PIL import Image
import numpy as np

class ColorPicker:
    def __init__(self, imageFile):
        self.image = Image.open(imageFile)
        self.colorThreshold = 100

        self.color = []
        self.index = []
        self.p = []
        self.count_colors_2()


    def count_colors_2(self) -> list:  # no need to give colors
        colors_count_list = self.image.getcolors(maxcolors = 10000000)
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
