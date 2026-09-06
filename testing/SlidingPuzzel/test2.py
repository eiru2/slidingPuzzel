import fast_noise
import random

# Keep size reasonable for vanilla Python lists (e.g. 16x16x16)
SIZE = 100
grid = [[[random.random() for _ in range(SIZE)] for _ in range(SIZE)] for _ in range(SIZE)]

print("Grid created successfully. Testing 1 sample lookup...")

# Test a single coordinate lookup to see if it immediately returns
try:
    result = fast_noise.trilinear_interpolation(grid, 5.25, 2.5, 9.75)
    print(f"Success! Output value: {result}")
except Exception as e:
    print(f"Error caught: {e}")
