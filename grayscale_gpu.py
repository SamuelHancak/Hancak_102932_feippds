"""
A module for converting RGB images to grayscale using GPU-based computation.
"""

__author__ = "Samuel Hancak"
__email__ = "xhancaks@stuba.sk"
__license__ = "MIT"

import numpy as np
from numba import cuda


class GrayscaleConverterGPU:
    """
    A class for converting an RGB image to grayscale using CUDA on the GPU.

    Attributes:
    - image_size (tuple): The dimensions of the input image as a tuple of (height, width).
    - threads_per_block (tuple): The number of threads per block as a tuple of (height, width).
    - blocks_per_grid_x (int): The number of blocks per grid in the x dimension.
    - blocks_per_grid_y (int): The number of blocks per grid in the y dimension.
    - blocks_per_grid (tuple): The total number of blocks per grid as a tuple of (x, y).
    - rgb_image (numpy.ndarray): The input RGB image as a NumPy array.
    - gray_image (numpy.ndarray): The resulting grayscale image as a NumPy array.
    """

    def __init__(self, image_size):
        """
        Constructs a new GrayscaleConverterGPU object.

        Parameters:
        - image_size (tuple): The dimensions of the input image as a tuple of (height, width).
        """
        self.image_size = image_size
        self.threads_per_block = (16, 16)
        self.blocks_per_grid_x = int(np.ceil(self.image_size[0] / self.threads_per_block[0]))
        self.blocks_per_grid_y = int(np.ceil(self.image_size[1] / self.threads_per_block[1]))
        self.blocks_per_grid = (self.blocks_per_grid_x, self.blocks_per_grid_y)
        self.rgb_image = None
        self.gray_image = None

    @cuda.jit
    def __grayscale_kernel(self):
        """
        The kernel function for converting an RGB image to grayscale using CUDA on the GPU.
        """
        # Get the x and y coordinates of the current thread
        x, y = cuda.grid(2)

        # Check if the current thread is within the bounds of the input image
        if x < self.rgb_image.shape[0] and y < self.rgb_image.shape[1]:
            # Get the R, G, and B values of the current pixel in the input image
            r, g, b = self.rgb_image[x, y]
            # Calculate the grayscale value of the current pixel using the specified formula
            self.gray_image[x, y] = 0.2989 * r + 0.5870 * g + 0.1140 * b

    def convert_to_grayscale(self, image):
        """
        Converts an RGB image to grayscale using CUDA on the GPU.

        Parameters:
        - image (ndarray): The input RGB image as a NumPy array.

        Returns:
        - gray_image (ndarray): The resulting grayscale image as a NumPy array.
        """
        # Create an empty grayscale image with the same size as the input image
        gray_image = np.empty(self.image_size, dtype=np.uint8)

        # Copy the input image from host memory to device memory
        self.rgb_image = cuda.to_device(image)

        # Copy the empty grayscale image from host memory to device memory
        self.gray_image = cuda.to_device(gray_image)

        # Execute the grayscale kernel function on the GPU using the specified number of blocks and threads per block
        self.__grayscale_kernel[self.blocks_per_grid, self.threads_per_block](self)

        # Copy the resulting grayscale image from device memory back to host memory
        self.gray_image.copy_to_host(gray_image)

        # Return the resulting grayscale image
        return gray_image
