# IN3110-nilsoles

The codes in this repo are ordered according to the weeks in which the corresponding exercises were given. E.g. the directory `assignment2` for week 2 etc.

The directory `assignment1` only contains `.txt`files used to test git functionality.

The following codes are contained in this repo:
1. `assignment2/`

	- `array_class.py` --- Containes a class implementation for a homogenous array of floats, integers of booleans. Supported mathematical operations on two instance of type `Array` are elementwise addition (`__add__`), subtraction (`__sub__`) and multiplication (`__mul__`). There is also support addition, subtraction and multiplication between a scalar and an instance of the `Array` class (calling the `__radd__`, `__rsub__` or `__rmul__` methods). One can also perform an element wise check of whether two instances of the `Array` class are equal, or where the elements of an instance of `Array` is equal to a scalar (`is_equal`). Similarly, there is also support for checking whether two instances of array are identical (`__eq__`). Finally, one can call the `min_element` and `mean_element` methods to respectively get the arrays minimum and mean elements. 

	The `Array` class can simply be imported though a regular import call in Python.

	NOTE: There is support for N-D arrays.

	- `test_array.py` --- Contains unit test for a number of operations evaluating the correctness of the `Array`class methods in `array_class.py`. Both 1D and 2D cases are tested for a variety of inputs types. To run the unit tests either run
