def ingresar_temperaturas():
    temperaturas = []
    for i in range(4):
        temp = float(input(f"Ingrese la temperatura del día {i+1}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    return sum(temperaturas) / len(temperaturas)

def main():
    print("== Promedio semanal del clima (Programación Tradicional) ==")
    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

if __name__ == "__main__":
    main()