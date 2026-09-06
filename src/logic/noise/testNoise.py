from noisePerlin import perlin_noise,perlin3d_mine
from noiseRandom import random_noise
import matplotlib.pyplot as plt

def plot_noise(noise, titel):
    plt.imshow(noise,cmap="gray", interpolation="nearest")
    plt.title(titel)
    plt.show()


plot_noise(perlin3d_mine((100,100,100),10)[4],"3d")
#plot_noise(perlin_noise(500,500,30), "perlin")
#print(perlin_noise(50,50,10))
#plot_noise(random_noise(500,500), "random")