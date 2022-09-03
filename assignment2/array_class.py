"""
Array class for assignment 2
"""

class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check if the values are of valid types

        # Check that the amount of values corresponds to the shape

        # Set class-variables
        self.num_values = 1
        for dim in shape:
            self.num_values *= dim 

        if self.num_values != len(values):
            raise ValueError("Number of elements and provided elements are not equal.")
        

        if not isinstance(shape, tuple):
            raise TypeError("Input shape must be of type tuple.")

        for value in values:
            if not isinstance(value, (float, int, bool)):
                message = f"Array value {value} if of type {type(value)}. Only integers, floats or boolean values are permitted."
                raise TypeError(message)

        if len(values) > 1:                 # We only need to assertt homogeneity if there is more than one elements in the array.
            self.datatype = type(values[0]) # Defining the datatype of the Array values from the first element of the provided values.
            for value in values[1:]:
                if not type(value) == self.datatype:
                    message = f"The array elements must be of the same datatype. Currently both {self.datatype} and {type(value)} are contained in array."
                    raise ValueError(message)

        self.shape = shape
        self.values_flat = list(values)

        self.values = []

        if len(shape) > 1:
            for i in range(shape[0]):
                self.values.append(list(values[i * shape[1] : (i + 1) * shape[1]]))
        else:
            self.values = list(values)
        
    def __getitem__(self, idx):
        """Returns Array element at given index

        Args:
            idx (int): Index at which Array element is to be returned.
        """
        return self.values[idx]


    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """

        return str(self.values)

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        if not isinstance(other, Array):
            return NotImplemented
        elif self.shape != other.shape:
            return NotImplemented
        elif self.datatype == bool or other.datatype == bool:
            return NotImplemented
        else:
            new_values = []
            for i in range(self.num_values):
                new_values.append(self.values_flat[i] + other.values_flat[i])
            return Array(self.shape, *new_values)

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if not isinstance(other, Array):    
            
            new_values = []
            if isinstance(other, (int, float)):
                for value in self.values_flat:
                    new_values.append(other + value)
            
            if isinstance(other, (bool)):
                return NotImplemented
        else:
            if self.shape != other.shape:
                # TODO: implement addition for two Array classes with different shapes?
                return NotImplemented

        return Array(self.shape, *new_values)


    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if not isinstance(other, Array):
            return NotImplemented
        elif self.shape != other.shape:
            return NotImplemented
        elif self.datatype == bool or other.datatype == bool:
            return NotImplemented
        else:
            new_values = []
            for i in range(self.num_values):
                new_values.append(self.values_flat[i] - other.values_flat[i])
            return Array(self.shape, *new_values)


    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        if not isinstance(other, Array):    
            
            new_values = []

            if isinstance(other, (int, float)):
                for value in self.values_flat:
                    new_values.append(other - value)

            if isinstance(other, (bool)):
                return NotImplemented
        else:
            if self.shape != other.shape:
                # TODO: implement subtraction for two Array classes with different shapes, i.e. broadcasting?
                return NotImplemented

        return Array(self.shape, *new_values)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if not isinstance(other, Array):
            return NotImplemented
        elif self.shape != other.shape:
            return NotImplemented
        elif self.datatype == bool or other.datatype == bool:
            return NotImplemented
        else:
            new_values = []
            for i in range(self.num_values):
                new_values.append(self.values_flat[i] * other.values_flat[i])
            return Array(self.shape, *new_values)


    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        # return self.__mul__(other)

        if not isinstance(other, Array):    
    
            new_values = []

            if isinstance(other, (int, float)):
                for value in self.values_flat:
                    new_values.append(other * value)

            if isinstance(other, (bool)):
                return NotImplemented
        else:
            if self.shape != other.shape:
                # TODO: implement subtraction for two Array classes with different shapes, i.e. broadcasting?
                return NotImplemented

        return Array(self.shape, *new_values)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, (Array, float, int, bool)):
            return False
        else:
            if isinstance(other, Array):
                if self.datatype != other.datatype:
                    return False 
                elif self.shape != other.shape:
                    return False
            
            bools = self.is_equal(other)
            if False in bools:
                return False
            else: 
                return True


    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if not isinstance(other, (Array, float, int, bool)):
            raise TypeError(f"Cannot compare Array with object of type {type(other)}.")
        else:
            new_values = []
            if isinstance(other, Array):
                if self.shape != other.shape:
                    raise ValueError("To compare two objects of type Array their shapes must match.")
                
                for i in range(self.num_values):
                    new_values.append(self.values_flat[i] == other.values_flat[i])

            if isinstance(other, (float, int, bool)):
                for i in range(self.num_values):
                    new_values.append(self.values_flat[i] == other)

            return Array(self.shape, *new_values)

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        if self.datatype == bool:
            raise TypeError("Can only find minimum of array if it is of datatype integer of float.")

        min_elem = self.values_flat[0] # Initializing minimum value with first array element

        for value in self.values_flat[1:]:
            if value < min_elem:
                min_elem = value

        return min_elem


    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """

        if self.datatype == bool:
                raise TypeError("Can only find mean of array if it is of datatype integer of float.")

        mean = 0
        for value in self.values_flat:
            mean += value           # Cumulative sum of array elements

        N = 1
        for dim in self.shape:
            N *= dim                # Total number of elements in array along all dimensions
        
        return mean / N 

    

