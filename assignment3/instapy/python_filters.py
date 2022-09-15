"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale using pure python code

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.zeros_like(
        image[..., 0]
    )  # Only need one color channel for grayscale. Using zeros instead of empty to avoid empty containing uninitialized values.
    # iterate through the pixels, and apply the grayscale transform
    num_of_rows, num_of_columns, num_of_colors = image.shape

    weights = [
        0.21,
        0.72,
        0.07,
    ]  # Red, Green and Blue (RGB) weights for converting color to grayscale

    for row in range(num_of_rows):  # Looping over input image
        for column in range(num_of_columns):
            for color in range(num_of_colors):
                weighted_colors = (
                    weights[color] * image[row, column, color]
                )  # Weight input colors
                gray_image[row, column] += weighted_colors.astype(
                    "uint8"
                )  # Perform weighted color sum and assign values to output image

    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia using pure python code

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.zeros_like(image, dtype=float)
    # Iterate through the pixels
    # applying the sepia matrix

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
