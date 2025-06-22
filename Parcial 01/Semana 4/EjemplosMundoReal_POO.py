# Clase que representa una habitación del hotel
class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero  # Número de habitación
        self.tipo = tipo      # Tipo: individual, doble, suite
        self.precio = precio  # Precio por noche
        self.disponible = True  # Estado de disponibilidad

    def reservar(self):
        if self.disponible:
            self.disponible = False
            print(f"Habitación {self.numero} reservada con éxito.")
        else:
            print(f"Habitación {self.numero} no está disponible.")

    def liberar(self):
        self.disponible = True
        print(f"Habitación {self.numero} ha sido liberada.")

# Clase que representa un cliente del hotel
class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def __str__(self):
        return f"{self.nombre} (ID: {self.cedula})"

# Clase principal que gestiona el hotel y las reservas
class Hotel:
    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_disponibles(self):
        print("Habitaciones disponibles:")
        for hab in self.habitaciones:
            if hab.disponible:
                print(f"- Habitación {hab.numero} ({hab.tipo}) - ${hab.precio}")

    def reservar_habitacion(self, numero, cliente):
        for hab in self.habitaciones:
            if hab.numero == numero:
                if hab.disponible:
                    hab.reservar()
                    print(f"Reserva a nombre de {cliente}")
                else:
                    print("La habitación ya está ocupada.")
                return
        print("Habitación no encontrada.")

# Programa de prueba
if __name__ == "__main__":
    # Crear hotel
    mi_hotel = Hotel("Hotel Paraíso")

    # Agregar habitaciones
    mi_hotel.agregar_habitacion(Habitacion(101, "Individual", 50))
    mi_hotel.agregar_habitacion(Habitacion(102, "Doble", 80))
    mi_hotel.agregar_habitacion(Habitacion(201, "Suite", 150))

    # Crear un cliente
    cliente1 = Cliente("Marlon Avila", "0932065048")

    # Mostrar habitaciones disponibles
    mi_hotel.mostrar_disponibles()

    # Reservar una habitación
    mi_hotel.reservar_habitacion(102, cliente1)

    # Mostrar habitaciones después de la reserva
    mi_hotel.mostrar_disponibles()