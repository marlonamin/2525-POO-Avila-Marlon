# inventario.py
# Sistema de Gestión de Inventarios (POO) en un solo archivo, con menú de consola.
# Autor: Tú :)
# Requisitos cubiertos:
# - Clase Producto (id único, nombre, cantidad, precio) con getters/setters y validaciones.
# - Clase Inventario (lista de productos) con métodos: agregar, eliminar, actualizar, buscar, listar.
# - Menú interactivo en consola para manejar todas las operaciones.

from typing import Any, List, Optional


class Producto:
    """Representa un producto del inventario."""

    def __init__(self, pid: str, nombre: str, cantidad: int, precio: float) -> None:
        self.id = pid
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # --- id ---
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El ID no puede estar vacío.")
        self._id = value.strip()

    # --- nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = value.strip()

    # --- cantidad ---
    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("La cantidad debe ser un número entero.")
        if value < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = value

    # --- precio ---
    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float) -> None:
        try:
            value = float(value)
        except Exception as e:
            raise TypeError("El precio debe ser numérico.") from e
        if value < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = value

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "nombre": self.nombre, "cantidad": self.cantidad, "precio": self.precio}

    def __repr__(self) -> str:
        return f"Producto(id={self.id!r}, nombre={self.nombre!r}, cantidad={self.cantidad}, precio={self.precio:.2f})"


class Inventario:
    """Estructura de datos personalizada: lista interna de productos + operaciones CRUD."""

    def __init__(self) -> None:
        self._productos: List[Producto] = []

    def _buscar_idx_por_id(self, pid: str) -> Optional[int]:
        """Devuelve el índice del producto con ese ID, o None si no existe."""
        for i, p in enumerate(self._productos):
            if p.id == pid:
                return i
        return None

    def obtener_por_id(self, pid: str) -> Optional[Producto]:
        idx = self._buscar_idx_por_id(pid)
        return self._productos[idx] if idx is not None else None

    def agregar(self, producto: Producto) -> None:
        """Añade un producto si el ID es único."""
        if self.obtener_por_id(producto.id) is not None:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos.append(producto)

    def eliminar(self, pid: str) -> bool:
        """Elimina un producto por ID. Devuelve True si lo eliminó, False si no existía."""
        idx = self._buscar_idx_por_id(pid)
        if idx is None:
            return False
        self._productos.pop(idx)
        return True

    def actualizar(self, pid: str, *, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        """Actualiza cantidad y/o precio por ID. Devuelve True si se actualizó."""
        prod = self.obtener_por_id(pid)
        if prod is None:
            return False
        if cantidad is not None:
            prod.cantidad = cantidad
        if precio is not None:
            prod.precio = precio
        return True

    def buscar_por_nombre(self, consulta: str) -> List[Producto]:
        """Búsqueda por coincidencia parcial (no sensible a mayúsculas)."""
        q = consulta.strip().lower()
        return [p for p in self._productos if q in p.nombre.lower()]

    def listar_todos(self) -> List[Producto]:
        """Devuelve una copia superficial de la lista de productos."""
        return list(self._productos)


# -------------------- Utilidades de entrada/salida para el menú --------------------

def input_no_vacio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("Entrada vacía. Intente de nuevo.")


def input_entero(msg: str, minimo: Optional[int] = None) -> int:
    while True:
        try:
            v = int(input(msg))
            if minimo is not None and v < minimo:
                print(f"El valor debe ser ≥ {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingrese un número entero válido.")


def input_float(msg: str, minimo: Optional[float] = None) -> float:
    while True:
        try:
            v = float(input(msg).replace(",", "."))
            if minimo is not None and v < minimo:
                print(f"El valor debe ser ≥ {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingrese un número válido (use punto decimal).")


def imprimir_tabla(productos: List[Producto]) -> None:
    """Imprime una tabla simple en la consola con los productos."""
    if not productos:
        print("No hay productos para mostrar.")
        return
    headers = ["ID", "Nombre", "Cantidad", "Precio"]
    filas = [[p.id, p.nombre, str(p.cantidad), f"{p.precio:.2f}"] for p in productos]
    anchos = [max(len(h), *(len(f[i]) for f in filas)) for i, h in enumerate(headers)]
    linea = " | ".join(h.ljust(anchos[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * anchos[i] for i in range(len(headers)))
    print(linea)
    print(sep)
    for f in filas:
        print(" | ".join(f[i].ljust(anchos[i]) for i in range(len(headers))))


def menu() -> None:
    inv = Inventario()

    opciones = {
        "1": "Añadir producto",
        "2": "Eliminar producto por ID",
        "3": "Actualizar cantidad/precio por ID",
        "4": "Buscar productos por nombre",
        "5": "Mostrar todos los productos",
        "0": "Salir",
    }

    while True:
        print("\n=== Sistema de Gestión de Inventarios ===")
        for k, v in opciones.items():
            print(f"{k}. {v}")

        op = input("Seleccione una opción: ").strip()
        if op == "1":
            try:
                pid = input_no_vacio("ID: ")
                nombre = input_no_vacio("Nombre: ")
                cantidad = input_entero("Cantidad: ", minimo=0)
                precio = input_float("Precio: ", minimo=0.0)
                inv.agregar(Producto(pid, nombre, cantidad, precio))
                print("✅ Producto agregado correctamente.")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif op == "2":
            pid = input_no_vacio("ID a eliminar: ")
            if inv.eliminar(pid):
                print("🗑️ Producto eliminado.")
            else:
                print("❌ No se encontró un producto con ese ID.")

        elif op == "3":
            pid = input_no_vacio("ID a actualizar: ")
            prod = inv.obtener_por_id(pid)
            if not prod:
                print("❌ No existe un producto con ese ID.")
                continue

            print(f"Producto actual: {prod}")
            cambiar_cant = input("¿Actualizar cantidad? (s/n): ").strip().lower() == "s"
            cambiar_prec = input("¿Actualizar precio? (s/n): ").strip().lower() == "s"

            kwargs = {}
            if cambiar_cant:
                kwargs["cantidad"] = input_entero("Nueva cantidad: ", minimo=0)
            if cambiar_prec:
                kwargs["precio"] = input_float("Nuevo precio: ", minimo=0.0)

            if kwargs and inv.actualizar(pid, **kwargs):
                print("✏️ Producto actualizado.")
            else:
                print("No se realizaron cambios.")

        elif op == "4":
            q = input_no_vacio("Buscar por nombre (coincidencia parcial): ")
            resultados = inv.buscar_por_nombre(q)
            imprimir_tabla(resultados)

        elif op == "5":
            imprimir_tabla(inv.listar_todos())

        elif op == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
