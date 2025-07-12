import os
import time

class GestorDeRecursos:
    """
    Clase de ejemplo para demostrar constructores y destructores.
    Simula la gestión de un recurso, inicializándolo y limpiándolo.
    """

    def __init__(self, id_recurso):
        """
        Constructor: Se ejecuta al crear un objeto.
        Inicializa atributos y prepara el recurso.
        """
        self.id = id_recurso
        self.estado = "inicializado"
        print(f"Constructor: Recurso '{self.id}' {self.estado}.")
        # Simula la asignación de un recurso (ej: abrir una conexión o archivo)
        self.recurso_abierto = True

    def operar(self):
        """
        Método que simula una operación con el recurso.
        """
        if self.recurso_abierto:
            print(f"Operando con el recurso '{self.id}'.")
        else:
            print(f"Error: Recurso '{self.id}' no disponible para operar.")

    def __del__(self):
        """
        Destructor: Se ejecuta cuando el objeto es destruido (liberado de memoria).
        Realiza tareas de limpieza o cierre de recursos.
        """
        if self.recurso_abierto:
            print(f"Destructor: Cerrando recurso '{self.id}'.")
            # Simula la liberación del recurso (ej: cerrar conexión, archivo)
            self.recurso_abierto = False
        else:
            print(f"Destructor: Recurso '{self.id}' ya estaba cerrado o no inicializado.")
        print(f"Destructor: Objeto '{self.id}' eliminado de la memoria.")


# --- Código de prueba para demostrar el comportamiento ---

def main():
    print("--- Inicio del programa ---")

    # Crear una instancia, invoca __init__
    obj1 = GestorDeRecursos("Recurso_A")
    obj1.operar()

    print("\nCreando otro objeto...")
    # Crear otra instancia, invoca __init__
    obj2 = GestorDeRecursos("Recurso_B")
    obj2.operar()

    print("\nEliminando explícitamente obj1...")
    # 'del' elimina la referencia. __del__ se llamará cuando no haya más referencias.
    del obj1
    time.sleep(0.5) # Pequeña pausa para demostración

    print("\nFin de la función main. obj2 saldrá de alcance.")
    # Cuando main termina, obj2 (si no fue 'del'-eado) será destruido.

if __name__ == "__main__":
    main()
    print("\n--- Programa finalizado ---")