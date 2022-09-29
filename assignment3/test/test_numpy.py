from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

import numpy.testing as nt
import numpy as np


def test_color2gray(image, reference_gray):
    # run color2gray
    gray_result = numpy_color2gray(image)
    # check that the result has the right shape, type

    assert gray_result.shape[-1] == 3  # Assert if we have three color channels
    assert gray_result.dtype == np.uint8  # Assert correct data type
    assert gray_result.shape == image.shape  # Assert if input shape equals output shape
    # assert uniform r,g,b values
    assert np.all(
        gray_result == gray_result[:, :, 0][:, :, None]
    )  # Assert if all color channels are equal in grayscale
    assert not np.all(
        image == image[:, :, 0][:, :, None]
    )  # Assert if input colors are different in color image

    np.random.seed(1)  # Ensure always the same random pixels are drawn
    selected_pixels = np.random.randint(
        (0, 0), (image.shape[0], image.shape[1]), (10, 2)
    )  # Select 10 random pixels

    for row, column in selected_pixels:
        in_pixel = image[row, column, :]
        expected_value = 0.21 * in_pixel[0] + 0.72 * in_pixel[1] + 0.07 * in_pixel[2]
        expected_value = expected_value.astype(
            np.int32
        )  # Transform to np.int32 to avoid cyclic over/underflow in difference
        out_pixel = gray_result[row, column, 0].astype(
            np.int32
        )  # Transform to np.int32 to avoid cyclic over/underflow in difference
        assert (
            np.abs(out_pixel - expected_value) <= 2
        )  # Check if input and output are within value 2 of each other.
        # Amouts to <= 2 / 255 = 0.8 % error with repsect to maximum color value 255.

    nt.assert_allclose(
        reference_gray, gray_result, atol=2
    )  # Assert if numpy grayscale result
    # and saved pure-python reference are similar to within 2 in pixel value


def test_color2sepia(image, reference_sepia):
    # run color2sepia
    sepia_result = numpy_color2sepia(image)

    # check that the result has the right shape, type
    # check that the result has the right shape, type
    assert sepia_result.shape[-1] == 3  # Assert if we have three color channels
    assert sepia_result.dtype == np.uint8  # Assert correct data type
    assert (
        sepia_result.shape == image.shape
    )  # Assert if input shape equals output shape

    # verify some individual pixel samples
    # according to the sepia matrix

    np.random.seed(1)  # Ensure always the same random pixels are drawn
    selected_pixels = np.random.randint(
        (0, 0), (image.shape[0], image.shape[1]), (10, 2)
    )  # Select 10 random pixels

    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ]
    )
    for row, column in selected_pixels:
        in_pixel = image[row, column, :]
        expected_value = np.minimum(255, in_pixel.dot(sepia_matrix.T))
        expected_value = expected_value.astype(
            np.int32
        )  # Transform to np.int32 to avoid cyclic over/underflow in difference
        out_pixel = sepia_result[row, column, :].astype(
            np.int32
        )  # Transform to np.int32 to avoid cyclic over/underflow in difference
        assert np.allclose(
            out_pixel, expected_value, atol=1
        )  # Check if input and output are within value 1 of each other.
        # Amouts to <= 1 / 255 = 0.4 % error with repsect to maximum color value 255.

    nt.assert_allclose(
        reference_sepia, sepia_result, atol=1
    )  # Assert if numpy sepia result and saved
    # pure-python reference are similar to within 1 pixel
