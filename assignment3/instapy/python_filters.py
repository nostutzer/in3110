"""pure Python implementation of image filters"""

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

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
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    ...

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
