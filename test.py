import numpy as np
import matplotlib.pyplot as plt
import random
#kilde https://www.youtube.com/watch?v=5ojp-KPDsLk&t=11s



array = [1,2,3,4,5,6]


for a in array:
    if a%2 == 0:
        array.remove(a)

print(array)