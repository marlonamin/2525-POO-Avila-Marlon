class RegistroClima:
    def __init__(self):
        self.__temperaturas = []

    def ingresar_temperaturas(self):
        for i in range(4):
            temp = float(input(f"Ingrese la temperatura del día {i+1}: "))
            self.__temperaturas.append(temp)

    def calcular_promedio(self):
        if not self.__temperaturas:
            return 0
        return sum(self.__temperaturas) / len(self.__temperaturas)

    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        print(f"Promedio semanal de temperatura: {promedio:.2f}°C")


# Subclase que hereda de RegistroClima
class RegistroClimaExtremo(RegistroClima):
    def __init__(self):
        super().__init__()

    # Polimorfismo: sobreescribimos mostrar_resultado
    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        if promedio > 35:
            print(f"¡Alerta! Semana extremadamente calurosa: {promedio:.2f}°C")
        elif promedio < 10:
            print(f"¡Precaución! Semana muy fría: {promedio:.2f}°C")
        else:
            print(f"Promedio semanal de temperatura: {promedio:.2f}°C (Temperatura normal)")

# === EJECUCIÓN ===

if __name__ == "__main__":
    print("== Promedio semanal del clima con detección de extremos (POO avanzada) ==")
    clima = RegistroClimaExtremo()
    clima.ingresar_temperaturas()
    clima.mostrar_resultado()
