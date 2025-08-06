import pytest

from func import es_primo
# Happy paths - casos donde la función debería funcionar correctamente
def test_es_primo():
    assert es_primo(2) == True
    assert es_primo(3) == True
    assert es_primo(4) == False
    assert es_primo(5) == True
    assert es_primo(29) == True
    assert es_primo(15) == False

# Edge cases - casos límite y especiales
def test_es_primo_edge_cases():
    assert es_primo(1) == False
    assert es_primo(0) == False
    assert es_primo(-5) == False
    assert es_primo(-3) == False
    assert es_primo(2.5) == False
    assert es_primo(1.5) == False
    assert es_primo(100) == False  # Compuesto grande
    assert es_primo(97) == True  # Primo grande
    assert es_primo(101) == True  # Primo grande
    assert es_primo(1000) == False  # Compuesto grande
    assert es_primo(999983) == True  # Primo grande
    assert es_primo(999984) == False  # Compuesto grande
    assert es_primo(999999) == False  # Compuesto grande
    assert es_primo(999991) == True  # Primo grande
    assert es_primo(999997) == True  # Primo grande
    assert es_primo(999999999999999999) == False  # Muy grande, compuesto
    assert es_primo(999999999999999991) == True  # Muy grande, primo
    assert es_primo(999999999999999993) == False  # Muy grande, compuesto
    assert es_primo(999999999999999997) == True  # Muy grande, primo
    assert es_primo(999999999999999998) == False  # Muy grande, compuesto


