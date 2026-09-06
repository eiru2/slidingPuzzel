from dis import print_instructions

import numpy as np
import matplotlib.pyplot as plt
import random
#kilde https://www.youtube.com/watch?v=5ojp-KPDsLk&t=11s

def smoothstep(t):
    """
    Smoothstep function for interpolation.

    Parameters:
    - t (float): Interpolation value between 0.0 and 1.0.

    Returns:
    - result (float): Smoothstep interpolated value.
    """
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    """
    Linear interpolation between two values.

    Parameters:
    - a (float): Start value.
    - b (float): End value.
    - t (float): Interpolation factor between 0.0 and 1.0.

    Returns:
    - result (float): Interpolated value between a and b.
    """
    return a + t * (b - a)




def perlin_noise(width,height,scale):
    """
    Generate Perlin noise using the given parameters.

    Parameters:
    - width (int): Width of the noise array.
    - height (int): Height of the noise array.
    - scale (int): Scale factor for generating the noise.

    Returns:
    - noise (n-dimensional array): Perlin noise array of shape (height, width).
    """
    noise = np.zeros((width,height))

    # Generate random gradient vectors
    gradients = np.random.randn(height // scale + 2, width // scale + 2, 2)
    print(gradients)

    for x in range(width):
        for y in range(height):
            # Calculate the grid cell coordinates for the current pixel
            cell_x = x // scale
            cell_y = y // scale

            # Calculate the position within the cell as fractional offsets
            cell_offset_x = x / scale - cell_x
            cell_offset_y = y / scale - cell_y

            # Calculate the dot products between gradients and offsets
            dot_product_tl = np.dot([cell_offset_x, cell_offset_y], gradients[cell_y, cell_x])
            dot_product_tr = np.dot([cell_offset_x - 1, cell_offset_y], gradients[cell_y, cell_x + 1])
            dot_product_bl = np.dot([cell_offset_x, cell_offset_y - 1], gradients[cell_y + 1, cell_x])
            dot_product_br = np.dot([cell_offset_x - 1, cell_offset_y - 1], gradients[cell_y + 1, cell_x + 1])

            # Interpolate the dot products using smoothstep function
            weight_x = smoothstep(cell_offset_x)
            weight_y = smoothstep(cell_offset_y)
            interpolated_top = lerp(dot_product_tl, dot_product_tr, weight_x)
            interpolated_bottom = lerp(dot_product_bl, dot_product_br, weight_x)
            interpolated_value = lerp(interpolated_top, interpolated_bottom, weight_y)

            # Store the interpolated value in the noise array
            noise[y,x] = interpolated_value

    # Normalize the noise values within the range of 0 to 1
    #noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))

    return noise


def perlin_noise_3d(shape, res):
    def f(t):
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

    delta = (res[0] / shape[0], res[1] / shape[1], res[2] / shape[2])
    d = (shape[0] // res[0], shape[1] // res[1], shape[2] // res[2])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1], 0:res[2]:delta[2]]
    grid = grid.transpose(1, 2, 3, 0) % 1

    # Gradients
    theta = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1, res[2] + 1)
    phi = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1, res[2] + 1)
    gradients = np.stack((np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)), axis=3)

    # === THE LOOPING FIX: Copy all boundary gradients to form a periodic grid ===
    gradients[-1, :, :] = gradients[0, :, :]
    gradients[:, -1, :] = gradients[:, 0, :]
    gradients[:, :, -1] = gradients[:, :, 0]
    # ============================================================================

    g000 = gradients[0:-1, 0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g100 = gradients[1:, 0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g010 = gradients[0:-1, 1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g110 = gradients[1:, 1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g001 = gradients[0:-1, 0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g101 = gradients[1:, 0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g011 = gradients[0:-1, 1:, 1:].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)
    g111 = gradients[1:, 1:, 1:].repeat(d[0], 0).repeat(d[1], 1).repeat(d[2], 2)

    # Ramps
    n000 = np.sum(np.stack((grid[:, :, :, 0], grid[:, :, :, 1], grid[:, :, :, 2]), axis=3) * g000, 3)
    n100 = np.sum(np.stack((grid[:, :, :, 0] - 1, grid[:, :, :, 1], grid[:, :, :, 2]), axis=3) * g100, 3)
    n010 = np.sum(np.stack((grid[:, :, :, 0], grid[:, :, :, 1] - 1, grid[:, :, :, 2]), axis=3) * g010, 3)
    n110 = np.sum(np.stack((grid[:, :, :, 0] - 1, grid[:, :, :, 1] - 1, grid[:, :, :, 2]), axis=3) * g110, 3)
    n001 = np.sum(np.stack((grid[:, :, :, 0], grid[:, :, :, 1], grid[:, :, :, 2] - 1), axis=3) * g001, 3)
    n101 = np.sum(np.stack((grid[:, :, :, 0] - 1, grid[:, :, :, 1], grid[:, :, :, 2] - 1), axis=3) * g101, 3)
    n011 = np.sum(np.stack((grid[:, :, :, 0], grid[:, :, :, 1] - 1, grid[:, :, :, 2] - 1), axis=3) * g011, 3)
    n111 = np.sum(np.stack((grid[:, :, :, 0] - 1, grid[:, :, :, 1] - 1, grid[:, :, :, 2] - 1), axis=3) * g111, 3)

    # Interpolation
    t = f(grid)
    n00 = n000 * (1 - t[:, :, :, 0]) + t[:, :, :, 0] * n100
    n10 = n010 * (1 - t[:, :, :, 0]) + t[:, :, :, 0] * n110
    n01 = n001 * (1 - t[:, :, :, 0]) + t[:, :, :, 0] * n101
    n11 = n011 * (1 - t[:, :, :, 0]) + t[:, :, :, 0] * n111
    n0 = (1 - t[:, :, :, 1]) * n00 + t[:, :, :, 1] * n10
    n1 = (1 - t[:, :, :, 1]) * n01 + t[:, :, :, 1] * n11
    return ((1 - t[:, :, :, 2]) * n0 + t[:, :, :, 2] * n1)


rng = np.random.default_rng()

def smoothing(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

def perlin3d_mine(size,scale):
    # First make vectores
    noise = np.zeros((size[0],size[1],size[2]))
    print(noise)
    gridLen = [size[0]//scale,size[1]//scale,size[2]//scale]
    grid = np.zeros((gridLen[0],gridLen[1],gridLen[2],3))
    print("---------")
    grid[0][0][0] = rng.uniform(-1, 1,3)
    for x in range(size[0]//scale):
        for y in range(size[1]//scale):
            for z in range(size[2]//scale):
                grid[x][y][z] = rng.uniform(-1, 1,3)
    # 2 dot prukukt
    print(grid)
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                #print("------")
                #print(x,y,z)
                #print(x//scale,y//scale,z//scale)
                #print((x//scale)%gridLen[0],(y//scale)%gridLen[1],(z//scale)%gridLen[2])

                # 1. Calculate base grid coordinates once
                X0 = (x // scale) % gridLen[0]
                Y0 = (y // scale) % gridLen[1]
                Z0 = (z // scale) % gridLen[2]

                # 2. Calculate neighbor coordinates with wrapping
                X1 = (X0 + 1) % gridLen[0]
                Y1 = (Y0 + 1) % gridLen[1]
                Z1 = (Z0 + 1) % gridLen[2]

                # 3. Retrieve the vectors
                vector000 = grid[X0][Y0][Z0]
                vector100 = grid[X1][Y0][Z0]
                vector010 = grid[X0][Y1][Z0]
                vector110 = grid[X1][Y1][Z0]

                vector001 = grid[X0][Y0][Z1]
                vector101 = grid[X1][Y0][Z1]
                vector011 = grid[X0][Y1][Z1]
                vector111 = grid[X1][Y1][Z1]

                cell_offset_x = (x % scale) / scale
                cell_offset_y = (y % scale) / scale
                cell_offset_z = (z % scale) / scale

                dot_product_tl0 = np.dot([cell_offset_x, cell_offset_y, cell_offset_z], vector000)
                dot_product_tr0 = np.dot([cell_offset_x - 1, cell_offset_y, cell_offset_z], vector100)
                dot_product_bl0 = np.dot([cell_offset_x, cell_offset_y - 1, cell_offset_z], vector010)
                dot_product_br0 = np.dot([cell_offset_x - 1, cell_offset_y - 1, cell_offset_z], vector110)

                dot_product_tl1 = np.dot([cell_offset_x, cell_offset_y, cell_offset_z-1], vector001)
                dot_product_tr1 = np.dot([cell_offset_x - 1, cell_offset_y, cell_offset_z-1], vector101)
                dot_product_bl1 = np.dot([cell_offset_x, cell_offset_y - 1, cell_offset_z-1], vector011)
                dot_product_br1 = np.dot([cell_offset_x - 1, cell_offset_y - 1, cell_offset_z-1], vector111)

                weight_x = smoothing(cell_offset_x)
                weight_y = smoothing(cell_offset_y)
                weight_z = smoothing(cell_offset_z)

                interpolated_top0 = lerp(dot_product_tl0, dot_product_tr0, weight_x)
                interpolated_bottom0 = lerp(dot_product_bl0, dot_product_br0, weight_x)
                interpolated_value0 = lerp(interpolated_top0, interpolated_bottom0, weight_y)

                interpolated_top1 = lerp(dot_product_tl1, dot_product_tr1, weight_x)
                interpolated_bottom1 = lerp(dot_product_bl1, dot_product_br1, weight_x)
                interpolated_value1 = lerp(interpolated_top1, interpolated_bottom1, weight_y)

                interpolated_value = lerp(interpolated_value0,interpolated_value1,weight_z)

                noise[x][y][z] = interpolated_value







    return noise
