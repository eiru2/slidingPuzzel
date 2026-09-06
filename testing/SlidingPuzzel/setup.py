from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Define the C++ extension module
ext_modules = [
    Pybind11Extension(
        "fast_noise",             # The name of the module you'll import in Python
        ["test.cpp"],    # Your C++ source file
    ),
]

setup(
    name="fast_noise",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}, # Automates compiler flags like -O3 and includes
)