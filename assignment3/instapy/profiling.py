"""
Profiling (IN4110 only)
"""

import pstats
import cProfile
import line_profiler

import numpy

import instapy
from . import io


def profile_with_cprofile(filter, image, ncalls=3):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """

    profiler = cProfile.Profile()

    profiler.enable()
    for _ in range(ncalls):  # Repeating measurement
        profiler.runcall(filter, image)
    profiler.disable()

    stats = pstats.Stats(profiler)

    stats.sort_stats("cumulative")
    stats.print_stats(10)


def profile_with_line_profiler(filter, image, ncalls=3):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    # create the LineProfiler
    profiler = line_profiler.LineProfiler()
    # tell it to measure the function we are given
    profiler.add_function(filter)

    # Measure filter(image)
    for _ in range(ncalls):  # Repeating measurement
        profiler.runcall(filter, image)
    # print statistics

    profiler.print_stats()


def run_profiles(profiler: str = "cprofile"):
    """Run profiles of every implementation

    Args:

        profiler (str): either 'line_profiler' or 'cprofile'
    """
    # Select which profile function to use
    if profiler == "line_profiler":
        profile_func = profile_with_line_profiler
    elif profiler.lower() == "cprofile":
        profile_func = profile_with_cprofile
    else:
        raise ValueError(f"{profiler=} must be 'line_profiler' or 'cprofile'")

    # construct a random 640x480 image
    image = io.random_image(640, 480)

    filter_names = ["color2gray", "color2sepia"]
    implementations = ["python", "numpy", "numba", "cython"]
    for filter_name in filter_names:
        for implementation in implementations:
            print(f"Profiling {implementation} {filter_name} with {profiler}:")
            filter = instapy.get_filter(filter_name, implementation)  #
            # call it once
            filter(image)
            profile_func(filter, image)


if __name__ == "__main__":
    print("Begin cProfile")
    run_profiles("cprofile")
    print("End cProfile")
    print("Begin line_profiler")
    run_profiles("line_profiler")
    print("End line_profiler")
