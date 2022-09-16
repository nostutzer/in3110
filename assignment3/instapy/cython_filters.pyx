"""Cython implementation of filter functions"""

import numpy as np
cimport numpy as np

cpdef np.ndarray[np.uint8_t, ndim=3] cython_color2gray(np.ndarray[np.uint8_t, ndim=3] image):
    """Convert rgb pixel array to grayscale using typed cython code

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    cdef np.ndarray[np.uint8_t, ndim=3] gray_image 
    
    gray_image= np.zeros_like(
        image, dtype = np.uint8
    )  # Using zeros instead of empty to avoid empty containing uninitialized values.
    # iterate through the pixels, and apply the grayscale transform
    
    cdef int num_of_rows    # Defining variables to store length of image axes
    cdef int num_of_columns
    cdef int num_of_colors

    cdef int row            # Defining loop variables
    cdef int column
    cdef int in_color
    cdef int out_color

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
            for in_color in range(num_of_colors):
                weighted_colors = weights[in_color] * image[row, column, in_color]    # Weight input colors
                for out_color in range(num_of_colors):
                    gray_image[row, column, out_color] += int(weighted_colors)                 # Perform weighted color sum and assign values to output image

    return gray_image

cpdef np.ndarray[np.uint8_t, ndim=3] cython_color2sepia(np.ndarray[np.uint8_t, ndim=3] image):
    """Convert rgb pixel array to sepia using typed cython code

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    cdef np.ndarray[np.double_t, ndim=3] sepia_image    # Making sure to use double dtype to avoid overflow
                                                        # in intermediate sepia filter computations
    
    sepia_image= np.zeros_like(
        image, dtype = np.double
    )  

    cdef int num_of_rows    # Defining variables to store length of image axes
    cdef int num_of_columns
    cdef int num_of_colors 

    cdef int row            # Defining loop variables
    cdef int column
    cdef int out_color
    cdef int in_color

    cdef double weighted_colors # Defining variable to temporarily store weighted color value

    num_of_rows = image.shape[0]    # Assigning values to defined variables
    num_of_columns = image.shape[1]
    num_of_colors = image.shape[2]

    cdef np.ndarray[np.double_t, ndim = 2] sepia_matrix
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ], dtype = np.double
    )  # Sepia weight matrix

    
    for row in range(num_of_rows):  # Looping over input image
        for column in range(num_of_columns):
            for out_color in range(num_of_colors):
                weighted_colors = 0
                for in_color in range(num_of_colors):
                    weighted_colors += sepia_matrix[out_color, in_color] * image[row, column, in_color]    # Weight input colors
                sepia_image[row, column, out_color] = min(255, weighted_colors)
    
    return sepia_image.astype("uint8")
