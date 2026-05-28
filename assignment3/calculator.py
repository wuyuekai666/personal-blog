"""A small calculator module used for Assignment 3 IDE integration."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b


def factorial(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("Please enter an integer.")
    if n < 0:
        raise ValueError("Negative numbers do not have factorials.")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def is_palindrome(text: str) -> bool:
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]
