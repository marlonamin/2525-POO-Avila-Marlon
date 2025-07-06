# Clase base
class Animal:
    def __init__(self, nombre, edad):
        self.nombre = nombre           # Atributo público
        self.__edad = edad            # Atributo encapsulado (privado)

    def hacer_sonido(self):
        return "El animal hace un sonido genérico"

    def get_edad(self):
        return self.__edad

    def set_edad(self, nueva_edad):
        if nueva_edad > 0:
            self.__edad = nueva_edad
        else:
            print("La edad debe ser positiva.")

    def info(self):
        return f"Nombre: {self.nombre}, Edad: {self.__edad}"


# Clase derivada que hereda de Animal
class Perro(Animal):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)  # Llamada al constructor de la clase base
        self.raza = raza

    # Polimorfismo: sobrescribimos el metodo hacer_sonido
    def hacer_sonido(self):
        return "¡Guau!"

    # Polimorfismo: metodo con diferentes comportamientos
    def jugar(self, juguete=None):
        if juguete:
            return f"{self.nombre} está jugando con un {juguete}."
        else:
            return f"{self.nombre} está corriendo feliz."

    def info(self):
        return f"{super().info()}, Raza: {self.raza}"


# Clase derivada adicional para mostrar más polimorfismo
class Gato(Animal):
    def hacer_sonido(self):
        return "¡Miau!"


if __name__ == "__main__":
    # Crear objetos (instancias) de las clases
    animal_generico = Animal("Animalito", 5)
    perro1 = Perro("Max", 3, "Labrador")
    gato1 = Gato("Michi", 2)

    # Mostrar sonidos (polimorfismo)
    print(animal_generico.hacer_sonido())  # Salida: sonido genérico
    print(perro1.hacer_sonido())           # Salida: Guau
    print(gato1.hacer_sonido())            # Salida: Miau

    # Mostrar información
    print(perro1.info())

    # Acceder a edad con encapsulación
    print("Edad del perro:", perro1.get_edad())
    perro1.set_edad(4)
    print("Nueva edad del perro:", perro1.get_edad())

    # Demostración de metodo con polimorfismo por argumentos
    print(perro1.jugar())
    print(perro1.jugar("pelota"))
