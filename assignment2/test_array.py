"""
Tests for our array class
"""

from array_class import Array

# 1D tests (Task 4)


def test_str_1d():
    my_array = Array((4,), 3, 2, 1, 0)
    expected = "[3, 2, 1, 0]"
    assert str(my_array) == expected


def test_add_1d():
    # Testing two integer arrays (__add__)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 5, 1, 2, -3)
    expected = [8, 3, 3, -3]
    assert my_array + another_array == expected

    # Testing two float arrays (__add__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 5.0, 1.0, 2.0, -3.0)
    expected = [8.0, 3.0, 3.0, -3.0]
    assert my_array + another_array == expected
        
    # Testing one float array and a scalar (__radd__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    some_scalar = -3.0
    expected = [0, -1.0, -2.0, -3.0]
    assert some_scalar + my_array == expected
        
    # Testing one integer array and a scalar (__radd__)
    my_array = Array((4,), 3, 2, 1, 0)
    some_scalar = -3.0
    expected = [0, -1.0, -2.0, -3.0]
    assert some_scalar + my_array == expected

def test_sub_1d():
    # Testing two integer arrays (__sub__)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 5, 1, 2, -3)
    expected = [-2, 1, -1, 3]
    assert my_array - another_array == expected

    # Testing two float arrays (__sub__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 5.0, 1.0, 2.0, -3.0)
    expected = [-2.0, 1.0, -1.0, 3.0]
    assert my_array - another_array == expected
        
    # Testing one float array and a scalar (__rsub__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    some_scalar = -3.0
    expected = [-6.0, -5.0, -4.0, -3.0]
    assert some_scalar - my_array == expected
        
    # Testing one integer array and a scalar (__rsub__)
    my_array = Array((4,), 3, 2, 1, 0)
    some_scalar = -3.0
    expected = [-6.0, -5.0, -4.0, -3.0]
    assert some_scalar - my_array == expected

def test_mul_1d():
    # Testing two integer arrays (__mul__)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 5, 1, 2, -3)
    expected = [15, 2, 2, 0]
    assert my_array * another_array == expected

    # Testing two float arrays (__mul__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 5.0, 1.0, 2.0, -3.0)
    expected = [15.0, 2.0, 2.0, 0.0]
    assert my_array * another_array == expected
        
    # Testing one float array and a scalar (__rmul__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    some_scalar = -3.0
    expected = [-9.0, -6.0, -3.0, 0.0]
    assert some_scalar * my_array == expected
        
    # Testing one integer array and a scalar (__rmul__)
    my_array = Array((4,), 3, 2, 1, 0)
    some_scalar = -3.0
    expected = [-9.0, -6.0, -3.0, 0.0]
    assert some_scalar * my_array == expected

def test_eq_1d():
    # Testing two integer arrays (__eq__)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 3, 2, 1, 0)
    expected = True
    result = (my_array == another_array)
    assert result == expected

    # Testing two integer arrays (__eq__)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 3, -5, 1, 0)
    expected = False
    result = (my_array == another_array)
    assert result == expected

    # Testing two float arrays (__eq__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 3.0, -5.0, 1.0, 0.0)
    expected = False
    result = (my_array == another_array)
    assert result == expected

    # Testing two float arrays (__eq__)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    expected = True
    result = (my_array == another_array)
    assert result == expected

    # Testing two bool arrays (__eq__)
    my_array = Array((4,), False, False, True, False)
    another_array = Array((4,), False, False, True, False)
    expected = True
    result = (my_array == another_array)
    assert result == expected
    
    # Testing two bool arrays (__eq__)
    my_array = Array((4,), False, True, True, False)
    another_array = Array((4,), False, False, True, False)
    expected = False
    result = (my_array == another_array)
    assert result == expected
    

    # Testing one bool arrays and a bool scalar (__eq__)
    my_array = Array((4,), False, True, True, False)
    scalar = True
    expected = False
    result = (my_array == scalar)
    assert result == expected

    # Testing one float arrays and one float scalar (__eq__)
    my_array = Array((4,), 3.0, 3.0, 3.0, 3.0)
    scalar = 3.0
    expected = True
    result = (my_array == scalar)
    assert result == expected

    # Testing one int arrays and strange datatype scalar (__eq__)
    my_array = Array((4,), 3, 3, 3, 3)
    scalar = "3.0"
    expected = False
    result = (my_array == scalar)
    assert result == expected

def test_same_1d():
    # Testing two integer arrays (is_equal)
    my_array = Array((4,), 3, 2, 1, 0)
    another_array = Array((4,), 3, 2, -1, 0)
    expected = [True, True, False, True]
    result = (my_array.is_equal(another_array))
    assert result == expected

    # Testing two float arrays (is_equal)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    another_array = Array((4,), 3.0, 2.0, -1.0, 4.0)
    expected = [True, True, False, False]
    result = (my_array.is_equal(another_array))
    assert result == expected

    # Testing two bool arrays (is_equal)
    my_array = Array((4,), True, False, False, True)
    another_array = Array((4,), False, False, False, True)
    expected = [False, True, True, True]
    result = (my_array.is_equal(another_array))
    assert result == expected

    # Testing one float array and one scalar (is_equal)
    my_array = Array((4,), 3.0, 2.0, 1.0, 0.0)
    scalar = 2.0
    expected = [False, True, False, False]
    result = (my_array.is_equal(scalar))
    assert result == expected

def test_smallest_1d():
    # Testing one float array(min_element)
    my_array = Array((4,), 3.0, -2.0, 1.0, 0.0)
    expected = -2.0
    result = (my_array.min_element())
    assert result == expected

    # Testing one float array(min_element)
    my_array = Array((4,), 3, 2, -1, 0)
    expected = -1
    result = (my_array.min_element())
    assert result == expected

def test_mean_1d():
    # Testing one float array(mean_element)
    my_array = Array((4,), 3.0, -2.0, 1.0, 0.0)
    expected = (3.0 - 2.0 + 1.0 + 0.0) / 4
    result = (my_array.mean_element())
    assert result == expected

    # Testing one float array(mean_element)
    my_array = Array((4,), 3, 2, -1, 0)
    expected = (3 + 2 - 1 + 0) / 4
    result = (my_array.mean_element())
    assert result == expected



# 2D tests (Task 6)


def test_add_2d():
    pass


def test_mult_2d():
    pass


def test_same_2d():
    pass


def test_mean_2d():
    pass


if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
