from noisePerlin import perlin_noise
from noiseRandom import random_noise
import matplotlib.pyplot as plt

def plot_noise(noise, titel):
    plt.imshow(noise,cmap="gray", interpolation="nearest")
    plt.title(titel)
    plt.show()

plot_noise(perlin_noise(500,500,10), "perlin")
print(perlin_noise(50,50,10))
plot_noise(random_noise(500,500), "random")