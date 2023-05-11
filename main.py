"""
This script demonstrates how to convert an RGB image to grayscale using both CPU and GPU methods.

The grayscaleconversion is performed using the GrayscaleConverterGPU and GrayscaleConverterCPU classes from
grayscale_gpu.py and grayscale_cpu.py, respectively.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Samuel Hancak"
__email__ = "xhancaks@stuba.sk"
__license__ = "MIT"

from PIL import Image
import numpy as np
import time
from grayscale_gpu import GrayscaleConverterGPU
from grayscale_cpu import GrayscaleConverterCPU

IMAGE_PATH = 'image590x350.jpg'

if __name__ == '__main__':
    # Load the input image and resize it to the specified size
    image = Image.open(IMAGE_PATH)

    # Convert the input image to a NumPy array
    rgb_image = np.array(image)

    # Initialize the CPU and GPU grayscale converter objects
    converterGpu = GrayscaleConverterGPU((rgb_image.shape[0], rgb_image.shape[1]))
    converterCpu = GrayscaleConverterCPU((rgb_image.shape[0], rgb_image.shape[1]))

    # Convert the input image to grayscale using the GPU and measure the execution time
    start_gpu = time.time()
    gray_gpu = converterGpu.convert_to_grayscale(rgb_image)
    end_gpu = time.time()

    # Convert the input image to grayscale using the CPU and measure the execution time
    start_cpu = time.time()
    gray_cpu = converterCpu.convert_to_grayscale(rgb_image)
    end_cpu = time.time()

    # Save the resulting grayscale images to disk
    gray_gpu_image = Image.fromarray(gray_gpu, 'L')
    gray_gpu_image.save('image_gpu590x350.jpg')
    gray_cpu_image = Image.fromarray(gray_cpu, 'L')
    gray_cpu_image.save('image_cpu590x350.jpg')

    print(f"GPU executed task in time: {end_gpu - start_gpu}s")
    print(f"CPU executed task in time: {end_cpu - start_cpu}s")
