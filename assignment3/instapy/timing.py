"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
from . import io
from typing import Callable
import numpy as np


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        average_runtime (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    average_runtime = 0

    for i in range(calls):
        initial_time = time.perf_counter()  # Start time in seconds
        filter_function(*arguments)
        final_time = time.perf_counter()  # Final time in secods
        average_runtime += final_time - initial_time  # Cumulative sum of runtimes

    average_runtime /= calls  # Converting cumulative runtime sum to average time

    return average_runtime


def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    with open("timing-report.txt", "w") as report_file:  # Making timing report file
        # load the image
        image = io.read_image(filename)
        image_shape = image.shape
        # print the image name, width, height
        message = (
            f"Timing performed using {filename}: {image_shape[0]}x{image_shape[1]}"
        )
        print(message)
        report_file.write(message + "\n")
        # iterate through the filters
        filter_names = ["color2gray", "color2sepia"]
        for filter_name in filter_names:
            # get the reference filter function
            reference_filter = filter_name
            reference_implementation = "python"
            # time the reference implementation

            reference_filter_func = instapy.get_filter(
                reference_filter, reference_implementation
            )  # Hardcoding "python" as reference implementation
            reference_time = time_one(reference_filter_func, image, calls=calls)

            message = f"Reference (pure Python) filter time {reference_filter}: {reference_time:.3}s ({calls=})"
            print(message)
            report_file.write(message + "\n")

            # iterate through the implementations
            implementations = ["numpy", "numba", "cython"]
            for implementation in implementations:
                filter = instapy.get_filter(filter_name, implementation)
                # time the filter
                filter_time = time_one(filter, image, calls=calls)
                # compare the reference time to the optimized time
                speedup = reference_time / filter_time

                message = f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
                print(message)
                report_file.write(message + "\n")


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports(calls=10)
