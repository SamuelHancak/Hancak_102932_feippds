"""
A module for converting RGB images to grayscale using CPU-based computation.
"""

__author__ = "Samuel Hancak"
__email__ = "xhancaks@stuba.sk"
__license__ = "MIT"

import numpy as np


class GrayscaleConverterCPU:
    """
    A class for converting RGB images to grayscale using CPU-based computation.

    Attributes:
    - image_size (tuple): The dimensions of the input image as a tuple of (height, width).
    """

    def __init__(self, image_size):
        """
        Initialize the GrayscaleConverterCPU object.

        Parameters:
        - image_size (tuple): The size of the input image as a (height, width) tuple.
        """
        self.image_size = image_size

    def convert_to_grayscale(self, image):
        """
        Convert the input RGB image to grayscale using the formula:
        gray = 0.2989 * red + 0.5870 * green + 0.1140 * blue

        Parameters:
        - image (ndarray): The input RGB image as a NumPy array.

        Returns:
        - gray_image (ndarray): The resulting grayscale image as a NumPy array.
        """
        # Extract the RGB channels from the input image
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

        # Calculate the corresponding grayscale values for each pixel
        gray_values = 0.2989 * r + 0.5870 * g + 0.1140 * b

        # Create a new grayscale image from the calculated grayscale values
        gray_image = np.array(gray_values, dtype=np.uint8)

        # Return the resulting grayscale image
        return gray_image
