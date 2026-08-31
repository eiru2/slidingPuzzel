import numpy as np
from matplotlib import scale


def random_noise(width,heigh):
    rng = np.random.default_rng()
    noise = rng.uniform(-1,1,(width,width))
    #print(noise)
    return noise
