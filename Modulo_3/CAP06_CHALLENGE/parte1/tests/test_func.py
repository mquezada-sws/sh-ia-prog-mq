import pytest

from parte1.func import es_primo

def test_prime_number_returns_true():
    """Function correctly identifies a prime number input."""
    assert es_primo(7) == True

def test_non_prime_number_returns_false():
    """Function correctly identifies a non-prime number input."""
    assert es_primo(8) == False

def test_smallest_prime_number():
    """Function returns expected result for the smallest prime number."""
    assert es_primo(2) == True

def test_zero_input():
    """Function handles input of 0 correctly."""
    assert es_primo(0) == False

def test_one_input():
    """Function handles input of 1 correctly."""
    assert es_primo(1) == False

def test_negative_number_input():
    """Function handles negative number input gracefully."""
    assert es_primo(-7) == False