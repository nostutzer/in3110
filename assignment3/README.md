# `Instapy`
---

## Summary of the Package
---

The `instapy` package is an image manipulation tool. It can be used both in scripts, but also has an easy to use command line interface. There are two image filters currently supported by `instapy`; a color-to-grayscale filter (`colot2gray`) and a color-to-sepia filter (`color2sepia`). As the names suggest the former converts a color image (in RGB) to a grayscale image, while the latter takes a color image and warms up its color tones using a sepia filter. Furthermore there are four implementation of each of the two filters;

 * `python`: An implementation of the filters which only used native `python`. NOTE that `numpy` is used in this case, but **only** to store the image matrix, but not for any computations.
 * `numpy`: An implementation which utilizes as `numpy`'s fast and convenient vectorized operations.
 * `numba`: An implementation which in it self looks very much like the native `python` version of the filters, but uses a just-in-time compilation provided by `numba` to speed up the filter operation.
 * `Cython`: An implementation which is written in the `Cython` `C/python` hybrid language, hence utilizing the speed advantages of typed and compiled `C` and at the same time the fast development speed of `python`'s comparatively east syntax.

---
## Installation
---

### Creating a `conda` environment
---

In order to generate a `conda` environment to install `instapy` in type 

```
$ conda create --name <your environment name> python=3.10
```

in a terminal. Then to activate the newly created environment run

```
$ conda activate <your environment name>
```

Once inside the conda environment we can continue with the installation of `instapy`.

---

### Installing `instapy` with `pip`
---

The first step in installing `instapy` is cloning the source code from GitHub by running 

```
$ mkdir your_preferred_directory
$ git clone https://github.uio.no/IN3110/IN3110-nilsoles.git your_preferred_directory
```
Thereafter, go into the correct directory inside the repository by running 

```
$ cd your_preferred_directory/assignment3
```
Now in the `assignment3` directory we can continue installing instapy by running 

```
$ python3 -m pip install .
```
If required, the `instapy` package can be installed in an editable mode by also providing the flags; `-e` or `--editable`. This is useful if you are interested in continuing to develope the package.

Because `ìnstapy` has a `cython` implementation of the image filters we also need to compile the cython libraries. This is easily done by running

```
$ python3 setup.py build_ext --inplace
```

The `instapy` package should now be ready for use!

---
### Requirements and Dependencies
---

To install the `instapy` package the following requirements and dependencies should be kept in mind;

 * `python >= 3.7`
 * `setuptools`
 * `numpy 1.23.3`
 * `numba 0.56.2`
 * `cython 0.29.32`
 * `pillow 9.2.0`
 * `line-profiler 3.5.1`

**NOTE:** These dependencies and requirements are also specified in the `pyproject.toml` file provided in the cloned repository. Thus if you create a  `conda` environment and use pip to install the package as specified all needed dependencies should automatically also be installed.

---
## Usage
---

The `instapy` package can be used both as a command line tool and as importable functions inside a `python` script. In the following each of these two use cases are elaborated.

---
### As a command line tool
---

In the following we will show you how to use `instapy` as a command line tool. 

To use `instapy` as a command line tool there are two options, either run

```
$ python3 -m instapy <arguments>
```
or
```
$ instapy <arguments>
```

In the above the `<arguments>` can take the following arguments and flags;

| Flag/argument           | Description                                                                                                                                                                                                                                                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<file>`                | (*Positional argument*) Full path to image file to perform filtering on. Must be an image format that Pillow can open.                                                                                                                                                           |
| `-h --help`             | This prints a **help** message describing the command line usage.                                                                                                                                                                                                                |
| `-o --out`              | the full path (including file ending) of the output file to save filtered image in.                                                                                                                                                                                              |
| `-g --gray`             | If this flag is supplied the grayscale filter is run                                                                                                                                                                                                                             |
| `-se --sepia`           | If this flag is supplied the sepia filter is run                                                                                                                                                                                                                                 |
| `-sc --scale`           | Rescaling factor to apply to image before filtering.                                                                                                                                                                                                                             |
| `-i` `--implementation` | Which implementation of the filter to use. Valid options are `python, numba, numpy` or `cython`                                                                                                                                                                                  |
| `-t --tune`             | With this we can tune the degree to which the sepia filter is applied to the image. The provided parameter takes values between 0 and 1, for respectively a not and fully sepia filtered image. **NOTE** that this feature is only available together with the `-i numpy` flag . |
| `-r --runtime`          | When providing this flag an average runtime of the filter (over three executions) will be printed.                                                                                                                                                                               |

To get some useful helper text we can run 
```
$ instapy -h
```
or 
```
$ instapy --help
```

Let us consider a case where we want to apply the grayscale filter to the `rain.jpg` image (provided in the `test` directory of the repository), with a python implementation of the filter, and save the result in a file called `my_grayscale_rain.jpg`. In that case we could run

```
$ instapy test/rain.jpg -i python -g -o my_grayscale_rain.jpg
```
If we want to do the same, but in addition scale down the image by a factor 2, we can add `-sc 2`
```
$ instapy test/rain.jpg -i python -g -sc 2 -o my_grayscale_rain.jpg 
```
We can also run the tool without specifying an output file (`-o`). In that case the filtered image will be displayed instead of being saved. 

Let us next run both the sepia and grayscale filters with the same call, and choose the `cython` implementation to filter the image;
```
$ instapy test/rain.jpg -i python -g -se -sc 3
```
which this time also scaled the image resolution down by a factor 3 and instead of saving the image we display it by leaving out the `-o <outfile>` flag.

Lastly, let us introduce the last two flags, `-t` or `--tune` and `-r` or `__runtime`, which respectively let you run a tunable sepia filter and print the average runtime of our filter;

```
$ instapy test/rain.jpg -i numpy -se -sc 3 -t 0.8 -r
```
which should produce an image that is 80% sepia filtered and it should print an average runtime of the filter.

---
### Inside a `python` script
---

The `instapy` filter functions can also be used inside a `python` script. To do so import the following modules

```
from instapy.<implementation>_filters import <implementation>_color2gray, <implementation>_color2sepia
from instapy import io
import instapy
import numpy as np
```
where `<implementation>` can be either `python, numba, numpy` or `cython`. For simplicity, let us use the `numpy` implementation in the next example. 

To load an image from file we can use;
```
image = io.read_image(filename)
```
and then to display the image we can run
```
io.display(image)
```
![input image](test/rain.jpg) 

Then if we want to apply the grayscale filter in the numpy implementation we can use 
```
gray_image = numpy_color2gray(image)
# Or we could use the build in function get_filter to construct a callable filter function 
filter_func = instapy.get_filter("color2gray", "numpy")
gray_image = filter_func(image)
io.display(gray_image)
```

![grayscale image](test/rain_reference_gray.png)

Lastly, if we want to run the sepia filter with, say a tuning of 100% we can do the following:
```
sepia_tuning = 1.0
sepia_image = numpy_color2sepia(image, sepia_tuning)
# Or we could again we can use the get_filter function
filter_func = instapy.get_filter("color2sepia", "numpy")
sepia_image = filter_func(image)
io.display(sepia_image)
```
![sepia image](test/rain_reference_sepia.png)

---
## Tests
In order to run the unit tests on `instapy` we need to use `pytest`. 

To check if our installation of the package was successfully we can run:

    ```
$ python3 -m pytest -v test/test_package.py
    ============================================= test session starts ==============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 12 items

    test/test_package.py::test_import PASSED                                                                 [  8%]
    test/test_package.py::test_install_metadata PASSED                                                       [ 16%]
    test/test_package.py::test_dependencies[numpy] PASSED                                                    [ 25%]
    test/test_package.py::test_dependencies[pillow] PASSED                                                   [ 33%]
    test/test_package.py::test_dependencies[numba] PASSED                                                    [ 41%]
    test/test_package.py::test_get_filter[python-color2gray] PASSED                                          [ 50%]
    test/test_package.py::test_get_filter[python-color2sepia] PASSED                                         [ 58%]
    test/test_package.py::test_get_filter[numpy-color2gray] PASSED                                           [ 66%]
    test/test_package.py::test_get_filter[numpy-color2sepia] PASSED                                          [ 75%]
    test/test_package.py::test_get_filter[numba-color2gray] PASSED                                           [ 83%]
    test/test_package.py::test_get_filter[numba-color2sepia] PASSED                                          [ 91%]
    test/test_package.py::test_io PASSED                                                                     [100%]

    ============================================== 12 passed in 0.18s ==============================================
    ```

When testing the four different filter implementations, i.e. `python, numpy, numba` or `cython`, we can also use pytest in the following ways

* `python` -- `$ python3 -m pytest -v test/test_python.py`
    ```
    ============================================= test session starts ==============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 2 items

    test/test_python.py::test_color2gray PASSED                                                              [ 50%]
    test/test_python.py::test_color2sepia PASSED                                                             [100%]

    ============================================== 2 passed in 0.71s ===============================================
    ```

* `numpy` -- `python3 -m pytest -v test/test_numpy.py`
    ```
    ============================================= test session starts ==============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 2 items

    test/test_numpy.py::test_color2gray PASSED                                                               [ 50%]
    test/test_numpy.py::test_color2sepia PASSED                                                              [100%]

    ============================================== 2 passed in 0.71s ===============================================
    ```

* `numba` -- `python3 -m pytest -v test/test_numba.py`
    ```
    ============================================= test session starts ==============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 2 items

    test/test_numba.py::test_color2gray PASSED                                                               [ 50%]
    test/test_numba.py::test_color2sepia PASSED                                                              [100%]

    ============================================== 2 passed in 1.02s ===============================================
    ```

* `cython` -- `python3 -m pytest -v test/test_cython.py`
    ```
    ============================================= test session starts ==============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 2 items

    test/test_cython.py::test_color2gray PASSED                                                              [ 50%]
    test/test_cython.py::test_color2sepia PASSED                                                             [100%]

    ============================================== 2 passed in 0.73s ===============================================
    ```


Alternatively, one can also run all unit test in one single call;

`$  python3 -m pytest -v test/*.p`
    ```
    =============================================== test session starts ===============================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment3
    collected 20 items

    test/test_cython.py::test_color2gray PASSED                                                                 [  5%]
    test/test_cython.py::test_color2sepia PASSED                                                                [ 10%]
    test/test_numba.py::test_color2gray PASSED                                                                  [ 15%]
    test/test_numba.py::test_color2sepia PASSED                                                                 [ 20%]
    test/test_numpy.py::test_color2gray PASSED                                                                  [ 25%]
    test/test_numpy.py::test_color2sepia PASSED                                                                 [ 30%]
    test/test_package.py::test_import PASSED                                                                    [ 35%]
    test/test_package.py::test_install_metadata PASSED                                                          [ 40%]
    test/test_package.py::test_dependencies[numpy] PASSED                                                       [ 45%]
    test/test_package.py::test_dependencies[pillow] PASSED                                                      [ 50%]
    test/test_package.py::test_dependencies[numba] PASSED                                                       [ 55%]
    test/test_package.py::test_get_filter[python-color2gray] PASSED                                             [ 60%]
    test/test_package.py::test_get_filter[python-color2sepia] PASSED                                            [ 65%]
    test/test_package.py::test_get_filter[numpy-color2gray] PASSED                                              [ 70%]
    test/test_package.py::test_get_filter[numpy-color2sepia] PASSED                                             [ 75%]
    test/test_package.py::test_get_filter[numba-color2gray] PASSED                                              [ 80%]
    test/test_package.py::test_get_filter[numba-color2sepia] PASSED                                             [ 85%]
    test/test_package.py::test_io PASSED                                                                        [ 90%]
    test/test_python.py::test_color2gray PASSED                                                                 [ 95%]
    test/test_python.py::test_color2sepia PASSED                                                                [100%]

    =============================================== 20 passed in 1.56s ================================================
    ```