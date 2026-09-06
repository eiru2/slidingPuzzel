#include <pybind11/pybind11.h>
#include <pybind11/numpy.h> // Required for direct NumPy array streaming
#include <cmath>

namespace py = pybind11;

double trilinear_interpolation(py::array_t<double> noise, double x, double y, double z) {
    // Request a buffer descriptor from the NumPy array
    py::buffer_info buf = noise.request();

    // Safety checks: ensure the array is 3D
    if (buf.ndim != 3) {
        throw std::runtime_error("Input noise grid must be a 3-dimensional NumPy array");
    }

    // Get grid dimension sizes
    int size_x = buf.shape[0];
    int size_y = buf.shape[1];
    int size_z = buf.shape[2];

    if (size_x <= 0 || size_y <= 0 || size_z <= 0) return 0.0;
    if (!std::isfinite(x) || !std::isfinite(y) || !std::isfinite(z)) return 0.0;

    // Helper lambda to replicate Python's modulo behavior safely
    auto python_mod = [](int val, int limit) {
        int mod = val % limit;
        return (mod < 0) ? (mod + limit) : mod;
    };

    // Calculate grid wrap-arounds using proper dimension size
    int x0 = python_mod(static_cast<int>(std::floor(x)), size_x);
    int x1 = python_mod(x0 + 1, size_x);
    
    int y0 = python_mod(static_cast<int>(std::floor(y)), size_y);
    int y1 = python_mod(y0 + 1, size_y);
    
    int z0 = python_mod(static_cast<int>(std::floor(z)), size_z);
    int z1 = python_mod(z0 + 1, size_z);

    // Get raw data pointer and strides for lightning-fast memory offsets
    double* ptr = static_cast<double*>(buf.ptr);
    auto stride_x = buf.strides[0] / sizeof(double);
    auto stride_y = buf.strides[1] / sizeof(double);
    auto stride_z = buf.strides[2] / sizeof(double);

    // Fast pointer calculations for the 8 surrounding grid coordinates
    double noise_value000 = ptr[x0 * stride_x + y0 * stride_y + z0 * stride_z];
    double noise_value010 = ptr[x0 * stride_x + y1 * stride_y + z0 * stride_z];
    double noise_value100 = ptr[x1 * stride_x + y0 * stride_y + z0 * stride_z];
    double noise_value110 = ptr[x1 * stride_x + y1 * stride_y + z0 * stride_z];

    double noise_value001 = ptr[x0 * stride_x + y0 * stride_y + z1 * stride_z];
    double noise_value011 = ptr[x0 * stride_x + y1 * stride_y + z1 * stride_z];
    double noise_value101 = ptr[x1 * stride_x + y0 * stride_y + z1 * stride_z];
    double noise_value111 = ptr[x1 * stride_x + y1 * stride_y + z1 * stride_z];

    // Get fractional steps
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

PYBIND11_MODULE(fast_noise, m) {
    m.doc() = "Zero-copy NumPy optimized trilinear interpolation module";
    m.def("trilinear_interpolation", &trilinear_interpolation, "Calculates trilinear interpolation on a NumPy array");
}