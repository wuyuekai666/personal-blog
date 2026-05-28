"""Unit tests for calculator.py.

Run with:

    python -m pytest test_calculator.py -v
"""

import pytest

from calculator import add, subtract, multiply, divide, factorial, is_palindrome


class TestAdd:
    def test_add_positive(self):
        assert add(1, 2) == 3

    def test_add_negative(self):
        assert add(-1, -1) == -2

    def test_add_float(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)


class TestSubtract:
    def test_subtract_positive(self):
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        assert subtract(2, 5) == -3


class TestMultiply:
    def test_multiply_positive(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(999, 0) == 0


class TestDivide:
    def test_divide_exact(self):
        assert divide(10, 2) == 5.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError):
            divide(10, 0)


class TestFactorial:
    def test_factorial_zero(self):
        assert factorial(0) == 1

    def test_factorial_positive(self):
        assert factorial(5) == 120

    def test_factorial_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_factorial_non_integer_raises(self):
        with pytest.raises(TypeError):
            factorial(3.5)


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_with_spaces(self):
        assert is_palindrome("a man a plan a canal panama") is True
