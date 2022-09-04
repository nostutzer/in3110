# IN3110-nilsoles

The codes in this repo are ordered according to the weeks in which the corresponding exercises were given. E.g. the directory `assignment2` for week 2 etc.

The directory `assignment1` only contains `.txt`files used to test git functionality.

The following codes are contained in this repo:
1.  `assignment2/`
        - `array_class.py` --- Containes a class implementation for a homogenous array of floats, integers of booleans. Supported mathematical operations on two instance of type `Array` are elementwise addition (`__add__`), subtraction (`__sub__`) and multiplication (`__mul__`). There is also support addition, subtraction and multiplication between a scalar and an instance of the `Array` class (calling the `__radd__`, `__rsub__` or `__rmul__` methods). One can also perform an element wise check of whether two instances of the `Array` class are equal, or where the elements of an instance of `Array` is equal to a scalar (`is_equal`). Similarly, there is also support for checking whether two instances of array are identical (`__eq__`). Finally, one can call the `min_element` and `mean_element` methods to respectively get the arrays minimum and mean elements. 

        The `Array` class can simply be imported though a regular import call in Python.

        Code example:

            ```
            from array_class import Array

            shape = (2, 2,)
            >>> my_array = Array(shape, 3, 2, 1, 0)
            >>> another_array = Array(shape, 5, 1, 2, -3)

            >>> my_array + another_array
            [[8, 3], [3, -3]]

            >>> my_array - another_array
            [[-2, 1], [-1, 3]]
            
            >>> my_array * another_array
            [[15, 2], [2, 0]]
            
            >>> -3.0 + my_array
            [[0, -1.0], [-2.0, -3.0]]

            >>> print(my_array)
            [[3, 2], [1, 0]]

            >>> print(another[1, 0])
            2

            >>> print(my_array.mean_element())
            1.5

            >>> print(another_array.min_element())
            -3

            >>> my_array = Array(shape, True, False, False, True)
            >>> another_array = Array(shape, False, False, False, True)
            >>> print(my_array.is_equal(another_array)
            [[False, True], [True, True]]

            >>> my_array = Array((4,), 3, 2, 1, 0)
            >>> another_array = Array((4,), 3, 2, 1, 0)
            >>> my_array == another_array
            True
            ```

        NOTE: There is support for N-D arrays.

        - `test_array.py` --- Contains unit test for a number of operations evaluating the correctness of the `Array`class methods in `array_class.py`. Both 1D and 2D cases are tested for a variety of inputs types. To run the unit tests either run

        1. `python test_array.py`
        
        2. `pytest test_array.py`

            ```
            ============================================ test session starts ============================================
            platform darwin -- Python 3.8.9, pytest-7.1.3, pluggy-1.0.0
            rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment2
            collected 12 items

            test_array.py ............                                                                            [100%]

            ============================================ 12 passed in 0.01s =============================================
            ```
