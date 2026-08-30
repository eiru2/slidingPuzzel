from noisePerlin import perlin_noise
from noiseRandom import random_noise
import matplotlib.pyplot as plt

def plot_noise(noise):
    plt.imshow(noise,cmap="gray", interpolation="nearest")
    plt.title("gat")
    plt.show()

plot_noise(perlin_noise(5000,5000,10))