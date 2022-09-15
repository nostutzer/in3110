"""Cython implementation of filter functions"""

import numpy as np
cimport numpy as np

cpdef np.ndarray[np.uint8_t, ndim=3] cython_color2gray(np.ndarray[np.uint8_t, ndim=3] image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    cdef np.ndarray[np.uint8_t, ndim=2] gray_image 
    
    gray_image= np.zeros_like(
        image[..., 0], dtype = np.uint8
    )  # Only need one color channel for grayscale. Using zeros instead of empty to avoid empty containing uninitialized values.
    # iterate through the pixels, and apply the grayscale transform
    
    cdef int num_of_rows    # Defining variables to store length of image axes
    cdef int num_of_columns
    cdef int num_of_colors

    cdef int row            # Defining loop variables
    cdef int column
    cdef int color

    cdef double weighted_colors # Defining variable to temporarily store weighted color value

    num_of_rows = image.shape[0]    # Assigning values to defined variables
    num_of_columns = image.shape[1]
    num_of_colors = image.shape[2]

    cdef np.ndarray[np.double_t, ndim = 1] weights
    weights = np.array([
        0.21,
        0.72,
        0.07,
    ], dtype = np.double
    )  # Red, Green and Blue (RGB) weights for converting color to grayscale

    
    for row in range(num_of_rows):  # Looping over input image
        for column in range(num_of_columns):
            for color in range(num_of_colors):
                weighted_colors = weights[color] * image[row, column, color]    # Weight input colors
                gray_image[row, column] += int(weighted_colors)                 # Perform weighted color sum and assign values to output image

    return gray_image

def cython_color2sepia(image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    ...
