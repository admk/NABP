from nabp_utils import dec2bin

class FixedPoint(object):
    """
    A simple fixed point arithmetic utility for generating
    fixed point arithmetic verilog source code
    """
    def __init__(
            self, integer_width, fractional_width,
            signed=False, value=None):
        self.integer_width = integer_width
        self.fractional_width = fractional_width
        self.signed = signed
        if not value is None:
            self.value = value

    def width(self):
        sign_bit = 1 if self.signed else 0
        return int(sign_bit + self.integer_width + self.fractional_width)

    def bin_repr(self):
        return self.bin_repr_of_value(self.value)

    def range(self):
        """
        >>> FixedPoint(4, 4, True).range()
        (-16.0, 15.9375)
        >>> FixedPoint(4, 4, False).range()
        (0.0, 15.9375)
        """
        if self.signed:
            min_val = -2 ** (self.width() - 1)
            max_val = 2 ** (self.width() - 1) - 1
        else:
            min_val = 0
            max_val = 2 ** self.width() - 1
        min_val /= float(2 ** self.fractional_width)
        max_val /= float(2 ** self.fractional_width)
        return (min_val, max_val)

    def precision(self):
        """
        >>> x = FixedPoint(4, 4, True, value='110011100')
        >>> y = FixedPoint(4, 4, True, value='110011101')
        >>> p = x.precision()
        >>> p
        0.0625
        >>> y.value - x.value == p
        True
        """
        return 1 / float(2 ** self.fractional_width)

    def verilog_decl(self):
        """
        >>> FixedPoint(4, 4, True).verilog_decl()
        'signed [8:0]'
        """
        signed = 'signed' if self.signed else 'unsigned'
        return signed + ' [' + str(self.width() - 1) + ':0]'

    def verilog_repr(self):
        """
        >>> FixedPoint(4, 4, True, value='110011101').verilog_repr()
        "9'b110011101"
        >>> FixedPoint(4, 4, True, value=-6.37).verilog_repr()
        "9'b110011011"
        """
        return str(self.width()) + '\'b' + self.bin_repr()

    def bin_repr_of_value(self, value):
        """
        >>> FixedPoint(4, 4, True).bin_repr_of_value(-6.1875)
        '110011101'
        """
        value *= 2 ** self.fractional_width
        return dec2bin(int(value), self.width())

    def value_of_bin_repr(self, repr_str):
        """
        >>> FixedPoint(4, 4, True).value_of_bin_repr('000000000')
        0.0
        >>> FixedPoint(4, 4, True).value_of_bin_repr('000000001')
        0.0625
        >>> FixedPoint(4, 4, True).value_of_bin_repr('110011101')
        -6.1875
        """
        if self.width() != len(repr_str):
            raise ValueError(
                    'Length of repr_str (%d) and width (%d) mismatch.' %
                    (len(repr_str), self.width()))
        val = 0
        for idx in xrange(self.width()):
            acc = int(repr_str[idx]) * (2 ** (self.width() - idx - 1))
            if idx == 0 and self.signed:
                acc = -acc
            val += acc
        val /= float(2 ** self.fractional_width)
        return val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        >>> FixedPoint(4, 4, True, value=-6.37).value
        -6.3125
        """
        if type(value) is float or type(value) is int:
            value = self.value_of_bin_repr(
                    self.bin_repr_of_value(value))
        elif type(value) is str:
            value = self.value_of_bin_repr(value)
        else:
            raise TypeError(
                    'Expected a numer or a binary represenation.')
        if value < self.range()[0] or value > self.range()[1]:
            raise OverflowError(
                    'Value cannot be within the range of this representation.')
        self._value = value

    def __str__(self):
        return self.verilog_repr()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
