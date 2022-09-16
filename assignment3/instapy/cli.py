"""Command-line (script) interface to instapy"""

import argparse
import sys

import numpy as np
from PIL import Image

import instapy
from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = io.read_image(file)
    # print("raw", image)
    if scale != 1:
        # print(image.shape)
        resized_image = Image.fromarray(
            image
        )  # Defining temporary Pillow Image to downscale
        resized_image = resized_image.resize(
            (resized_image.width // scale, resized_image.height // scale)
        )  # Downscaling image
        # io.display(image)
        image = np.asarray(
            resized_image
        )  # Re-defining image to be the downscaled version
        # print(image.shape)
        # io.display(image)

    # Apply the filter
    filter_func = instapy.get_filter(filter, implementation)  # Defining filter function
    filtered = filter_func(image)
    # print("filtered", filtered)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", type=str, help="The filename to apply filter to")
    parser.add_argument(
        "-o", "--out", type=str, help="The output filename", default=None
    )

    # Add required arguments
    parser.add_argument(
        "-i",
        "--implementation",
        help="Implementation of filter function, e.g. python, cython etc.",
        default="python",
        choices=["python", "numba", "numpy", "cython"],
        type=str,
    )

    parser.add_argument(
        "-g",
        "--gray",
        help="Apply grayscale filter to input image.",
        action="store_true",
    )

    parser.add_argument(
        "-se", "--sepia", help="Apply sepia filter to input image.", action="store_true"
    )

    parser.add_argument(
        "-sc",
        "--scale",
        help="Downscaling to apply to height/width of image. If set to 1 the original image is used.",
        default=1,
        type=int,
    )

    # parse arguments and call run_filter
    args = parser.parse_args()  # Getting commandline arguments from parser object
    filename = args.file  # Input image filename
    out_file = args.out  # Output filename
    implementation = args.implementation  # Which filter implementation to use
    use_gray = args.gray  # Filter to apply to input image
    use_sepia = args.sepia  # Filter to apply to input image
    scaleing = args.scale  # Scaling to apply to image height/width

    if not use_gray and not use_sepia:
        raise ValueError("At least one filter must be provided.")

    arguments = []
    if use_gray:
        filter = "color2gray"
        if out_file:
            out_name = out_file.split(".")
            out_file = out_name[0] + "_gray." + out_name[1]
        arguments.append((filename, out_file, implementation, filter, scaleing))

    if use_sepia:
        filter = "color2sepia"
        if out_file:
            out_name = out_file.split(".")
            out_file = out_name[0] + "_sepia." + out_name[1]
        arguments.append((filename, out_file, implementation, filter, scaleing))

    for args in arguments:
        run_filter(*args)  # Applying filter to specified command line arguments
