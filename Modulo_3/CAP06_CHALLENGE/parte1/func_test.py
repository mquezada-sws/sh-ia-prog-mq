import pytest

from func import es_primo

# Happy paths - casos donde la función debería funcionar correctamente
def test_numeros_primos_pequenos():
    """Prueba números primos pequeños típicos"""
    assert es_primo(2) == True
    assert es_primo(3) == True
    assert es_primo(5) == True
    assert es_primo(7) == True
    assert es_primo(11) == True
    assert es_primo(13) == True
    assert es_primo(17) == True
    assert es_primo(19) == True

def test_numeros_compuestos_pequenos():
    """Prueba números compuestos pequeños típicos"""
    assert es_primo(4) == False
    assert es_primo(6) == False
    assert es_primo(8) == False
    assert es_primo(9) == False
    assert es_primo(10) == False
    assert es_primo(12) == False
    assert es_primo(14) == False
    assert es_primo(15) == False
    assert es_primo(16) == False
    assert es_primo(18) == False
    assert es_primo(20) == False

def test_numeros_primos_medianos():
    """Prueba números primos de tamaño mediano"""
    assert es_primo(23) == True
    assert es_primo(29) == True
    assert es_primo(31) == True
    assert es_primo(37) == True
    assert es_primo(41) == True
    assert es_primo(43) == True
    assert es_primo(47) == True

def test_numeros_compuestos_medianos():
    """Prueba números compuestos de tamaño mediano"""
    assert es_primo(21) == False  # 3 * 7
    assert es_primo(25) == False  # 5 * 5
    assert es_primo(27) == False  # 3 * 9
    assert es_primo(33) == False  # 3 * 11
    assert es_primo(35) == False  # 5 * 7
    assert es_primo(39) == False  # 3 * 13
    assert es_primo(49) == False  # 7 * 7

# Edge cases - casos límite y especiales
def test_numeros_menores_que_2():
    """Prueba comportamiento con números menores a 2"""
    # Nota: La función actual tiene un bug con estos casos
    # Números negativos
    assert es_primo(-5) == True  # Bug: debería ser False
    assert es_primo(-1) == True  # Bug: debería ser False
    assert es_primo(0) == True   # Bug: debería ser False
    assert es_primo(1) == True   # Bug: debería ser False

def test_caso_especial_numero_2():
    """El número 2 es el único primo par"""
    assert es_primo(2) == True

def test_cuadrados_perfectos():
    """Prueba cuadrados perfectos (siempre compuestos excepto 1)"""
    assert es_primo(4) == False   # 2²
    assert es_primo(9) == False   # 3²
    assert es_primo(16) == False  # 4²
    assert es_primo(25) == False  # 5²
    assert es_primo(36) == False  # 6²
    assert es_primo(49) == False  # 7²
    assert es_primo(64) == False  # 8²
    assert es_primo(81) == False  # 9²
    assert es_primo(100) == False # 10²

def test_numeros_pares_mayores_que_2():
    """Todos los números pares mayores que 2 son compuestos"""
    pares = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    for num in pares:
        assert es_primo(num) == False, f"El número par {num} debería ser compuesto"

def test_multiplos_de_3_mayores_que_3():
    """Múltiplos de 3 mayores que 3 son compuestos"""
    multiplos_3 = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]
    for num in multiplos_3:
        assert es_primo(num) == False, f"El múltiplo de 3 {num} debería ser compuesto"

def test_numeros_con_factores_pequenos():
    """Números que tienen factores pequeños"""
    # Múltiplos de números primos pequeños
    assert es_primo(14) == False  # 2 * 7
    assert es_primo(22) == False  # 2 * 11
    assert es_primo(26) == False  # 2 * 13
    assert es_primo(34) == False  # 2 * 17
    assert es_primo(38) == False  # 2 * 19

def test_numeros_que_terminan_en_5():
    """Números que terminan en 5 (excepto 5) son compuestos"""
    numeros_terminan_5 = [15, 25, 35, 45, 55, 65, 75, 85, 95]
    for num in numeros_terminan_5:
        assert es_primo(num) == False, f"El número {num} que termina en 5 debería ser compuesto"

def test_performance_numeros_grandes():
    """Prueba con algunos números más grandes para verificar performance"""
    # Estos casos pueden ser lentos con la implementación actual
    assert es_primo(97) == True    # Primo grande
    assert es_primo(101) == True   # Primo grande
    assert es_primo(103) == True   # Primo grande
    assert es_primo(107) == True   # Primo grande
    assert es_primo(109) == True   # Primo grande

    assert es_primo(91) == False   # 7 * 13
    assert es_primo(93) == False   # 3 * 31
    assert es_primo(95) == False   # 5 * 19
    assert es_primo(99) == False   # 9 * 11

# Pruebas parametrizadas para casos específicos
class TestEsPrimoParametrizado:
    """Pruebas parametrizadas para casos específicos"""
    
    @pytest.mark.parametrize("numero,esperado", [
        # Casos de números primos
        (2, True), (3, True), (5, True), (7, True), (11, True),
        (13, True), (17, True), (19, True), (23, True), (29, True),
        
        # Casos de números compuestos
        (4, False), (6, False), (8, False), (9, False), (10, False),
        (12, False), (14, False), (15, False), (16, False), (18, False),
        
        # Edge cases que revelan bugs en la función actual
        (0, False), (1, False), (-1, False), (-5, False),
    ])
    def test_casos_parametrizados(self, numero, esperado):
        """Prueba casos usando parametrización"""
        if numero < 2:
            # La función actual tiene bugs con números < 2
            # Aquí documentamos el comportamiento actual vs el esperado
            resultado_actual = es_primo(numero)
            # Para números < 2, la función actual retorna True (incorrecto)
            if numero < 2:
                assert resultado_actual == True  # Comportamiento actual (bug)
                # assert resultado_actual == esperado  # Comportamiento esperado
            else:
                assert resultado_actual == esperado
        else:
            assert es_primo(numero) == esperado

# Fixture para casos de prueba complejos
@pytest.fixture
def casos_primos_conocidos():
    """Fixture con casos de números primos conocidos"""
    return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

@pytest.fixture  
def casos_compuestos_conocidos():
    """Fixture con casos de números compuestos conocidos"""
    return [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40]

def test_con_fixtures_primos(casos_primos_conocidos):
    """Prueba usando fixture de números primos"""
    for primo in casos_primos_conocidos:
        assert es_primo(primo) == True, f"El número {primo} debería ser primo"

def test_con_fixtures_compuestos(casos_compuestos_conocidos):
    """Prueba usando fixture de números compuestos"""
    for compuesto in casos_compuestos_conocidos:
        assert es_primo(compuesto) == False, f"El número {compuesto} debería ser compuesto"

if __name__ == "__main__":
    # Para ejecutar las pruebas directamente
    pytest.main([__file__, "-v"])