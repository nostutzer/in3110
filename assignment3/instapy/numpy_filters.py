"""numpy implementation of image filters"""

from typing import Optional
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale using numpy

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    weights = np.array(
        [
            0.21,
            0.72,
            0.07,
        ]
    )  # Red, Green and Blue (RGB) weights for converting color to grayscale

    weights = (
        np.ones((3, 3)) * weights[:, None]
    )  # Broadcasting weight copies to output RGB rows
    # to construct transformation matrix operator
    gray_image = image.dot(weights)  # Performing color-to-grayscale operation

    return gray_image.astype("uint8")


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia using numpy

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ]
    )

    tuning_matrix_diagonal = (
        np.ones(3) - sepia_matrix.diagonal()
    )  # Modifying sepia matrix for tunable filter
    tuning_matrix_diagonal *= -(1 - k)
    tuning_matrix = sepia_matrix * (1 - k)
    np.fill_diagonal(tuning_matrix, tuning_matrix_diagonal)
    sepia_matrix -= tuning_matrix

    # Apply the matrix filter
    sepia_image = image.dot(
        sepia_matrix.T
    )  # Performing matrix product between image and sepia matrix

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image = np.minimum(
        sepia_image, 255
    )  # Clipping max value of sepia image to 255.

    return sepia_image.astype("uint8")
