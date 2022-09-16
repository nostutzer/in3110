# Profiling report

## Questions

A few questions below to help understand the kind of information we can get from profiling outputs.
 We are not asking for lots of detail, just 1-2 sentences each.

### Question 1

> Which profiler produced the most useful output, and why?

The `line_profiler` seems preferable as it specifically tells you about the bottle necks inside the function called, how many times each line is run and what percentage of the total runtime that line causes, whereas `cProfiler` only seems to tell us about the performance of function calls. This enables us to specifically target the lines that pose the largest bottleneck in our function. However, it might still be usefull to know about the function call overhead from different function calls which `cProfiler` tells us about.

### Question 2

> Pick one profiler output (e.g. `cprofile numpy_color2sepia`).
  Based on this profile, where should we focus effort on improving performance?

> **Hint:** two things to consider when picking an optimization:

> - how much time is spent in the step? (reducing a step that takes 1% of the time all the way to 0 can only improve performance by 1%)
> - are there other ways to do it? (simple steps may already be optimal. Complex steps often have many implementations with different performance)

selected profile: `line_profiler numpy_color2sepia`

According to the `line_profiler` report of `numpy_color2sepia` the lines that take the most time are (in decreasing order) line 73, 6.5 and 82 with respectively 89.4%, 6.5% and 3.8% of the runtime. On first glance therefore we would like to find faster ways of implementing these three lines. However, taking a closer look, it seems that the two first of these, i.e. the matrix operation between image and sepia matrix and the cliping of the image values to 255 are calls to vectorized numpy functions. This is good though; we want the most runtime to be spent on the fastest modules like numpy, that way we know that if numpy calls need the most runtime we have likely implemented everything else quite efficiently. However, perhaps it is possible to find some more smart way of handelig the correct datatypes so that we can avoid the `.astype("uint8")` call that causes 3.8% of the runtime.

## Profile output

Paste the outputs of `python3 -m instapy.profiling` below:

<details>
<summary>cProfile output</summary>

```
Profiling python color2gray with cprofile:
         8294441 function calls (8294435 primitive calls) in 7.539 seconds

   Ordered by: cumulative time
   List reduced from 14 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    4.316    1.439    7.539    2.513 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/python_filters.py:6(python_color2gray)
  8294400    3.223    0.000    3.223    0.000 {method 'astype' of 'numpy.generic' objects}
        1    0.000    0.000    2.494    2.494 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(zeros_like)
      9/3    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:76(zeros_like)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(copyto)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.zeros}
        3    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numpy color2gray with cprofile:
         32 function calls in 0.028 seconds

   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.000    0.000    0.028    0.009 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numpy_filters.py:7(numpy_color2gray)
        3    0.027    0.009    0.027    0.009 {method 'dot' of 'numpy.ndarray' objects}
        1    0.000    0.000    0.010    0.010 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.001    0.000    0.001    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:149(ones)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(copyto)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 {built-in method numpy.array}
        3    0.000    0.000    0.000    0.000 {built-in method numpy.empty}
        3    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numba color2gray with cprofile:
         11 function calls in 0.008 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.008    0.003    0.008    0.003 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numba_filters.py:6(numba_color2gray)
        1    0.000    0.000    0.003    0.003 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numba/core/serialize.py:29(_numba_unpickle)
        1    0.000    0.000    0.000    0.000 {method 'enable' of '_lsprof.Profiler' objects}
        3    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling cython color2gray with cprofile:
         44 function calls (35 primitive calls) in 0.041 seconds

   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      6/3    0.041    0.007    0.041    0.014 instapy/cython_filters.pyx:6(cython_color2gray)
        1    0.000    0.000    0.014    0.014 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(zeros_like)
      9/3    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:76(zeros_like)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(copyto)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.zeros}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/multiarray.py:80(empty_like)
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/multiarray.py:1071(copyto)


Profiling python color2sepia with cprofile:
         2764844 function calls (2764838 primitive calls) in 8.671 seconds

   Ordered by: cumulative time
   List reduced from 15 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    8.478    2.826    8.671    2.890 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/python_filters.py:40(python_color2sepia)
        1    0.000    0.000    2.918    2.918 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
  2764800    0.190    0.000    0.190    0.000 {built-in method builtins.min}
        3    0.000    0.000    0.002    0.001 <__array_function__ internals>:177(zeros_like)
      9/3    0.002    0.000    0.002    0.001 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.002    0.001 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:76(zeros_like)
        3    0.000    0.000    0.002    0.001 <__array_function__ internals>:177(copyto)
        3    0.001    0.000    0.001    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.zeros}


Profiling numpy color2sepia with cprofile:
         47 function calls in 0.028 seconds

   Ordered by: cumulative time
   List reduced from 16 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.002    0.001    0.028    0.009 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numpy_filters.py:33(numpy_color2sepia)
        3    0.025    0.008    0.025    0.008 {method 'dot' of 'numpy.ndarray' objects}
        1    0.000    0.000    0.010    0.010 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.001    0.000    0.001    0.000 {method 'astype' of 'numpy.ndarray' objects}
        6    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:149(ones)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(fill_diagonal)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(copyto)
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/lib/index_tricks.py:779(fill_diagonal)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.array}


Profiling numba color2sepia with cprofile:
         11 function calls in 0.031 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.031    0.010    0.031    0.010 /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numba_filters.py:41(numba_color2sepia)
        1    0.000    0.000    0.010    0.010 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numba/core/serialize.py:29(_numba_unpickle)
        3    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {method 'enable' of '_lsprof.Profiler' objects}


Profiling cython color2sepia with cprofile:
         44 function calls (35 primitive calls) in 0.040 seconds

   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      6/3    0.039    0.006    0.040    0.013 instapy/cython_filters.pyx:54(cython_color2sepia)
        1    0.000    0.000    0.013    0.013 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/cProfile.py:106(runcall)
        3    0.000    0.000    0.001    0.000 <__array_function__ internals>:177(zeros_like)
      9/3    0.001    0.000    0.001    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.001    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/numeric.py:76(zeros_like)
        3    0.000    0.000    0.001    0.000 <__array_function__ internals>:177(copyto)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 {built-in method numpy.zeros}
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/multiarray.py:1071(copyto)
        3    0.000    0.000    0.000    0.000 /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/numpy/core/multiarray.py:80(empty_like)
```

</details>

<details>
<summary>line_profiler output</summary>

```
Profiling python color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 16.9352 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/python_filters.py
Function: python_color2gray at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           def python_color2gray(image: np.array) -> np.array:
     7                                               """Convert rgb pixel array to grayscale using pure python code
     8                                           
     9                                               Args:
    10                                                   image (np.array)
    11                                               Returns:
    12                                                   np.array: gray_image
    13                                               """
    14         6        122.0     20.3      0.0      gray_image = np.zeros_like(
    15         3          0.0      0.0      0.0          image
    16                                               )  # Using zeros instead of empty to avoid empty containing uninitialized values.
    17                                               # iterate through the pixels, and apply the grayscale transform
    18         3          3.0      1.0      0.0      num_of_rows, num_of_columns, num_of_colors = image.shape
    19                                           
    20         3          2.0      0.7      0.0      weights = [
    21                                                   0.21,
    22                                                   0.72,
    23                                                   0.07,
    24                                               ]  # Red, Green and Blue (RGB) weights for converting color to grayscale
    25                                           
    26      1443        273.0      0.2      0.0      for row in range(num_of_rows):  # Looping over input image
    27    923040     185570.0      0.2      1.1          for column in range(num_of_columns):
    28   3686400     838706.0      0.2      5.0              for in_color in range(num_of_colors):
    29   2764800     556813.0      0.2      3.3                  weighted_colors = (
    30   2764800    2801575.0      1.0     16.5                      weights[in_color] * image[row, column, in_color]
    31                                                           )  # Weight input colors
    32  11059200    2603969.0      0.2     15.4                  for out_color in range(num_of_colors):
    33  16588800    8355803.0      0.5     49.3                      gray_image[row, column, out_color] += weighted_colors.astype(
    34   8294400    1592337.0      0.2      9.4                          "uint8"
    35                                                               )  # Perform weighted color sum and assign values to output image
    36                                           
    37         3          3.0      1.0      0.0      return gray_image

Profiling numpy color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 0.027542 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numpy_filters.py
Function: numpy_color2gray at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           def numpy_color2gray(image: np.array) -> np.array:
     8                                               """Convert rgb pixel array to grayscale using numpy
     9                                           
    10                                               Args:
    11                                                   image (np.array)
    12                                               Returns:
    13                                                   np.array: gray_image
    14                                               """
    15                                           
    16         6         13.0      2.2      0.0      weights = np.array(
    17         3          2.0      0.7      0.0          [
    18                                                       0.21,
    19                                                       0.72,
    20                                                       0.07,
    21                                                   ]
    22                                               )  # Red, Green and Blue (RGB) weights for converting color to grayscale
    23                                           
    24         3          0.0      0.0      0.0      weights = (
    25         3         60.0     20.0      0.2          np.ones((3, 3)) * weights[:, None]
    26                                               )  # Broadcasting weight copies to output RGB rows
    27                                               # to construct transformation matrix operator
    28         3      26397.0   8799.0     95.8      gray_image = image.dot(weights)  # Performing color-to-grayscale operation
    29                                           
    30         3       1070.0    356.7      3.9      return gray_image.astype("uint8")

Profiling numba color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 0 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numba_filters.py
Function: numba_color2gray at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           @jit(nopython=True, cache=True)
     7                                           def numba_color2gray(image: np.array) -> np.array:
     8                                               """Convert rgb pixel array to grayscale using just-in-time compiled python code
     9                                           
    10                                               Args:
    11                                                   image (np.array)
    12                                               Returns:
    13                                                   np.array: gray_image
    14                                               """
    15                                               gray_image = np.zeros_like(
    16                                                   image
    17                                               )  # Using zeros instead of empty to avoid empty containing uninitialized values.
    18                                           
    19                                               num_of_rows, num_of_columns, num_of_colors = image.shape
    20                                           
    21                                               weights = [
    22                                                   0.21,
    23                                                   0.72,
    24                                                   0.07,
    25                                               ]  # Red, Green and Blue (RGB) weights for converting color to grayscale
    26                                           
    27                                               for row in range(num_of_rows):  # Looping over input image
    28                                                   for column in range(num_of_columns):
    29                                                       for in_color in range(num_of_colors):
    30                                                           weighted_colors = (
    31                                                               weights[in_color] * image[row, column, in_color]
    32                                                           )  # Weight input colors
    33                                                           for out_color in range(num_of_colors):
    34                                                               gray_image[row, column, out_color] += int(
    35                                                                   weighted_colors
    36                                                               )  # Perform weighted color sum and assign values to output image
    37                                           
    38                                               return gray_image

Profiling cython color2gray with line_profiler:
Timer unit: 1e-06 s

Total time: 1.32812 s
File: instapy/cython_filters.pyx
Function: cython_color2gray at line 6

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     6                                           cpdef np.ndarray[np.uint8_t, ndim=3] cython_color2gray(np.ndarray[np.uint8_t, ndim=3] image):

Profiling python color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 34.596 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/python_filters.py
Function: python_color2sepia at line 40

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    40                                           def python_color2sepia(image: np.array) -> np.array:
    41                                               """Convert rgb pixel array to sepia using pure python code
    42                                           
    43                                               Args:
    44                                                   image (np.array)
    45                                               Returns:
    46                                                   np.array: sepia_image
    47                                               """
    48         3       2276.0    758.7      0.0      sepia_image = np.zeros_like(image, dtype=float)
    49                                               # Iterate through the pixels
    50                                               # applying the sepia matrix
    51                                           
    52         3          1.0      0.3      0.0      sepia_matrix = [
    53         3          3.0      1.0      0.0          [0.393, 0.769, 0.189],
    54         3          1.0      0.3      0.0          [0.349, 0.686, 0.168],
    55         3          3.0      1.0      0.0          [0.272, 0.534, 0.131],
    56                                               ]
    57                                           
    58         3          5.0      1.7      0.0      num_of_rows, num_of_columns, num_of_colors = image.shape
    59                                           
    60      1443        503.0      0.3      0.0      for row in range(num_of_rows):  # Looping over input image
    61    923040     284379.0      0.3      0.8          for column in range(num_of_columns):
    62   3686400    1285318.0      0.3      3.7              for out_color in range(num_of_colors):
    63  11059200    3649425.0      0.3     10.5                  for in_color in range(num_of_colors):
    64   8294400    2532342.0      0.3      7.3                      weighted_colors = (
    65   8294400    9110599.0      1.1     26.3                          sepia_matrix[out_color][in_color] * image[row, column, in_color]
    66                                                               )  # Computing weighted color matrix product
    67  24883200    9066353.0      0.4     26.2                      sepia_image[
    68   8294400    2640983.0      0.3      7.6                          row, column, out_color
    69   8294400    2615489.0      0.3      7.6                      ] += weighted_colors  # Summing weighted color values
    70                                           
    71   5529600    2312329.0      0.4      6.7                  sepia_image[row, column, out_color] = min(
    72   2764800    1094753.0      0.4      3.2                      255, sepia_image[row, column, out_color]
    73                                                           )  # Cliping max value to max allowed value 255
    74                                           
    75         3       1235.0    411.7      0.0      return sepia_image.astype("uint8")  # Converting to correct dtype

Profiling numpy color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 0.027653 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numpy_filters.py
Function: numpy_color2sepia at line 33

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    33                                           def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    34                                               """Convert rgb pixel array to sepia using numpy
    35                                           
    36                                               Args:
    37                                                   image (np.array)
    38                                                   k (float): amount of sepia filter to apply (optional)
    39                                           
    40                                               The amount of sepia is given as a fraction, k=0 yields no sepia while
    41                                               k=1 yields full sepia.
    42                                           
    43                                               (note: implementing 'k' is a bonus task,
    44                                               you may ignore it for Task 9)
    45                                           
    46                                               Returns:
    47                                                   np.array: sepia_image
    48                                               """
    49                                           
    50         3          3.0      1.0      0.0      if not 0 <= k <= 1:
    51                                                   # validate k (optional)
    52                                                   raise ValueError(f"k must be between [0-1], got {k=}")
    53                                           
    54                                               # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    55         6         13.0      2.2      0.0      sepia_matrix = np.array(
    56         3          2.0      0.7      0.0          [
    57         3          3.0      1.0      0.0              [0.393, 0.769, 0.189],
    58         3          1.0      0.3      0.0              [0.349, 0.686, 0.168],
    59         3          1.0      0.3      0.0              [0.272, 0.534, 0.131],
    60                                                   ]
    61                                               )
    62                                           
    63         3          0.0      0.0      0.0      if k > 0:
    64         3          1.0      0.3      0.0          tuning_matrix_diagonal = (
    65         3         25.0      8.3      0.1              np.ones(3) - sepia_matrix.diagonal()
    66                                                   )  # Modifying sepia matrix for tunable filter
    67         3          8.0      2.7      0.0          tuning_matrix_diagonal *= -(1 - k)
    68         3          3.0      1.0      0.0          tuning_matrix = sepia_matrix * (1 - k)
    69         3         20.0      6.7      0.1          np.fill_diagonal(tuning_matrix, tuning_matrix_diagonal)
    70         3          2.0      0.7      0.0          sepia_matrix -= tuning_matrix
    71                                           
    72                                               # Apply the matrix filter
    73         6      24734.0   4122.3     89.4      sepia_image = image.dot(
    74         3          2.0      0.7      0.0          sepia_matrix.T
    75                                               )  # Performing matrix product between image and sepia matrix
    76                                           
    77                                               # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    78         6       1796.0    299.3      6.5      sepia_image = np.minimum(
    79         3          2.0      0.7      0.0          sepia_image, 255
    80                                               )  # Clipping max value of sepia image to 255.
    81                                           
    82         3       1037.0    345.7      3.8      return sepia_image.astype("uint8")

Profiling numba color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 0 s
File: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3/instapy/numba_filters.py
Function: numba_color2sepia at line 41

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    41                                           @jit(nopython=True, cache=True)
    42                                           def numba_color2sepia(image: np.array) -> np.array:
    43                                               """Convert rgb pixel array to sepia using just-in-time compiled python code
    44                                           
    45                                               Args:
    46                                                   image (np.array)
    47                                               Returns:
    48                                                   np.array: sepia_image
    49                                               """
    50                                               sepia_image = np.zeros(
    51                                                   image.shape, dtype=float
    52                                               )  # Making sure dtype of initial zeros image is float
    53                                               # to avoid overflow in intermediate calculations
    54                                           
    55                                               sepia_matrix = [
    56                                                   [0.393, 0.769, 0.189],
    57                                                   [0.349, 0.686, 0.168],
    58                                                   [0.272, 0.534, 0.131],
    59                                               ]
    60                                           
    61                                               num_of_rows, num_of_columns, num_of_colors = image.shape
    62                                           
    63                                               for row in range(num_of_rows):  # Looping over input image
    64                                                   for column in range(num_of_columns):
    65                                                       for out_color in range(num_of_colors):
    66                                                           for in_color in range(num_of_colors):
    67                                                               weighted_colors = (
    68                                                                   sepia_matrix[out_color][in_color] * image[row, column, in_color]
    69                                                               )  # Computing weighted color matrix product
    70                                                               sepia_image[
    71                                                                   row, column, out_color
    72                                                               ] += weighted_colors  # Summing weighted color values
    73                                           
    74                                                           sepia_image[row, column, out_color] = min(
    75                                                               255, sepia_image[row, column, out_color]
    76                                                           )  # Cliping max value to max allowed value 255
    77                                           
    78                                               return sepia_image.astype("uint8")  # Converting to correct dtype

Profiling cython color2sepia with line_profiler:
Timer unit: 1e-06 s

Total time: 1.5715 s
File: instapy/cython_filters.pyx
Function: cython_color2sepia at line 54

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    54                                           cpdef np.ndarray[np.uint8_t, ndim=3] cython_color2sepia(np.ndarray[np.uint8_t, ndim=3] image):
```

</details>
