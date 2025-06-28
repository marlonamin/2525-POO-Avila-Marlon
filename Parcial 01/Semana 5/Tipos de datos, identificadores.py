# Programa para calcular el área de un círculo y verificar si supera un área mínima

import math

def calcular_area_circulo(radio):
    """
    Calcula el área de un círculo dado su radio.
    Parámetro:
        radio (float): Radio del círculo.
    Retorna:
        float: Área del círculo.
    """
    area = math.pi * radio ** 2
    return area

def area_mayor_que(area, umbral):
    """
    Verifica si el área es mayor que un valor umbral.
    Parámetros:
        area (float): Área calculada.
        umbral (float): Valor de comparación.
    Retorna:
        bool: True si área > umbral, False en caso contrario.
    """
    return area > umbral

# Entrada de datos
radio_circulo = float(input("Ingresa el radio del círculo: "))
umbral_area = float(input("Ingresa el área mínima para comparar: "))

# Cálculo del área
area_circulo = calcular_area_circulo(radio_circulo)

# Verificación
resultado = area_mayor_que(area_circulo, umbral_area)

# Mostrar resultados
print(f"El área del círculo es: {area_circulo:.2f}")
print(f"¿El área es mayor que {umbral_area}? {resultado}")