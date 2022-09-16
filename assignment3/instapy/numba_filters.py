"""numba-optimized filters"""
from numba import jit
import numpy as np


@jit(nopython=True, cache=True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale using just-in-time compiled python code

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.zeros_like(
        image
    )  # Using zeros instead of empty to avoid empty containing uninitialized values.

    num_of_rows, num_of_columns, num_of_colors = image.shape

    weights = [
        0.21,
        0.72,
        0.07,
    ]  # Red, Green and Blue (RGB) weights for converting color to grayscale

    for row in range(num_of_rows):  # Looping over input image
        for column in range(num_of_columns):
            for in_color in range(num_of_colors):
                weighted_colors = (
                    weights[in_color] * image[row, column, in_color]
                )  # Weight input colors
                for out_color in range(num_of_colors):
                    gray_image[row, column, out_color] += int(
                        weighted_colors
                    )  # Perform weighted color sum and assign values to output image

    return gray_image


@jit(nopython=True, cache=True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia using just-in-time compiled python code

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.zeros(
        image.shape, dtype=float
    )  # Making sure dtype of initial zeros image is float
    # to avoid overflow in intermediate calculations

    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]

    num_of_rows, num_of_columns, num_of_colors = image.shape

    for row in range(num_of_rows):  # Looping over input image
        for column in range(num_of_columns):
            for out_color in range(num_of_colors):
                for in_color in range(num_of_colors):
                    weighted_colors = (
                        sepia_matrix[out_color][in_color] * image[row, column, in_color]
                    )  # Computing weighted color matrix product
                    sepia_image[
                        row, column, out_color
                    ] += weighted_colors  # Summing weighted color values

                sepia_image[row, column, out_color] = min(
                    255, sepia_image[row, column, out_color]
                )  # Cliping max value to max allowed value 255

    return sepia_image.astype("uint8")  # Converting to correct dtype
