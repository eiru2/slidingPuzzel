#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>

double trilinear_interpolation(const std::vector<std::vector<std::vector<double>>>& noise, double x, double y, double z) {
    int len_noise = noise.size();
    if (len_noise == 0) return 0.0;

    auto python_mod = [len_noise](int val) {
        int mod = val % len_noise;
        return mod < 0 ? mod + len_noise : mod;
    };

    int x0 = python_mod(static_cast<int>(x));
    int x1 = python_mod(x0 + 1);
    int y0 = python_mod(static_cast<int>(y));
    int y1 = python_mod(y0 + 1);
    int z0 = python_mod(static_cast<int>(z));
    int z1 = python_mod(z0 + 1);

    double noise_value000 = noise[x0][y0][z0];
    double noise_value010 = noise[x0][y1][z0];
    double noise_value100 = noise[x1][y0][z0];
    double noise_value110 = noise[x1][y1][z0];

    double noise_value001 = noise[x0][y0][z1];
    double noise_value011 = noise[x0][y1][z1];
    double noise_value101 = noise[x1][y0][z1];
    double noise_value111 = noise[x1][y1][z1];

    double xd = x - std::floor(x);
    double yd = y - std::floor(y);
    double zd = z - std::floor(z);

    return (
        noise_value000 * (1 - xd) * (1 - yd) * (1 - zd) +
        noise_value100 * xd * (1 - yd) * (1 - zd) +
        noise_value010 * (1 - xd) * yd * (1 - zd) +
        noise_value110 * xd * yd * (1 - zd) +
        noise_value001 * (1 - xd) * (1 - yd) * zd +
        noise_value101 * xd * (1 - yd) * zd +
        noise_value011 * (1 - xd) * yd * zd +
        noise_value111 * xd * yd * zd
    );
}

int main() {
    int size = 32;
    // Initialize 32x32x32 noise grid
    std::vector<std::vector<std::vector<double>>> noise(size, std::vector<std::vector<double>>(size, std::vector<double>(size, 0.5)));
    
    int iterations = 100000000;
    double total = 0;

    std::cout << "Running " << iterations << " iterations in C++..." << std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < iterations; ++i) {
        // Pseudo-random walking floating-point coordinates
        total += trilinear_interpolation(noise, i * 0.123, i * 0.456, i * 0.789);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> duration = end - start;
    
    std::cout << "C++ Execution Time: " << duration.count() << " ms" << std::endl;
    std::cout << "Verification Checksum: " << total << std::endl;
    return 0;
}