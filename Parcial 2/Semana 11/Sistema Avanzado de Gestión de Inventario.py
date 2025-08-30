# inventario_avanzado.py
# Sistema Avanzado de Gestión de Inventario (POO + Colecciones + Archivos)
# Autor: Marlon Ávila
# Requisitos cubiertos:
# - Clase Producto con validaciones y properties (ID, nombre, cantidad, precio).
# - Clase Inventario con diccionario de Productos y un índice por nombre (set de IDs).
# - Operaciones: agregar, eliminar, actualizar, buscar por nombre, listar.
# - Persistencia: guardar/cargar en JSON (serialización/deserialización).
# - Menú interactivo en consola.

# El inventario se guarda automáticamente en "inventario.json" en la misma carpeta.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import json
import os
import unicodedata


def _norm(s: str) -> str:
    """Normaliza cadenas para búsquedas sin acentos y en minúsculas."""
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('ascii')
    return s.lower().strip()


@dataclass
class Producto:
    pid: str
    nombre: str
    cantidad: int
    precio: float

    # --- Validaciones mediante properties para cumplir POO ---
    def __post_init__(self):
        self.pid = self.pid          # dispara setter
        self.nombre = self.nombre
        self.cantidad = self.cantidad
        self.precio = self.precio

    @property
    def pid(self) -> str:
        return self._pid

    @pid.setter
    def pid(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("ID (pid) debe ser una cadena no vacía.")
        self._pid = value.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("Nombre debe ser una cadena no vacía.")
        self._nombre = value.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Cantidad debe ser un entero >= 0.")
        self._cantidad = int(value)

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float) -> None:
        try:
            f = float(value)
        except (TypeError, ValueError):
            raise ValueError("Precio debe ser un número >= 0.")
        if f < 0:
            raise ValueError("Precio debe ser un número >= 0.")
        self._precio = float(f)

    # Serialización para archivos
    def to_dict(self) -> Dict:
        return {
            "pid": self.pid,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @staticmethod
    def from_dict(d: Dict) -> "Producto":
        return Producto(
            pid=d["pid"],
            nombre=d["nombre"],
            cantidad=int(d["cantidad"]),
            precio=float(d["precio"]),
        )

    # Representación útil
    def __str__(self) -> str:
        return f"{self.pid} | {self.nombre} | {self.cantidad} | ${self.precio:.2f}"


class Inventario:
    def __init__(self) -> None:
        # Diccionario principal: ID -> Producto
        self._productos: Dict[str, Producto] = {}
        # Índice auxiliar por nombre normalizado: nombre_norm -> set de IDs
        self._index_nombre: Dict[str, Set[str]] = {}

    # --- Métodos internos para manejar índices ---
    def _index_add(self, p: Producto) -> None:
        key = _norm(p.nombre)
        self._index_nombre.setdefault(key, set()).add(p.pid)

    def _index_remove(self, p: Producto) -> None:
        key = _norm(p.nombre)
        ids = self._index_nombre.get(key)
        if ids:
            ids.discard(p.pid)
            if not ids:
                self._index_nombre.pop(key, None)

    def _index_update_nombre(self, p: Producto, nombre_anterior: str) -> None:
        if _norm(nombre_anterior) != _norm(p.nombre):
            # quitar de índice viejo y añadir al nuevo
            pseudo = Producto(p.pid, nombre_anterior, p.cantidad, p.precio)
            self._index_remove(pseudo)
            self._index_add(p)

    # --- API pública ---
    def agregar(self, p: Producto) -> None:
        if p.pid in self._productos:
            raise KeyError(f"Ya existe un producto con ID '{p.pid}'.")
        self._productos[p.pid] = p
        self._index_add(p)

    def eliminar(self, pid: str) -> Producto:
        if pid not in self._productos:
            raise KeyError(f"No existe producto con ID '{pid}'.")
        p = self._productos.pop(pid)
        self._index_remove(p)
        return p

    def actualizar_cantidad(self, pid: str, nueva_cantidad: int) -> None:
        p = self.obtener(pid)
        p.cantidad = nueva_cantidad

    def actualizar_precio(self, pid: str, nuevo_precio: float) -> None:
        p = self.obtener(pid)
        p.precio = nuevo_precio

    def actualizar_nombre(self, pid: str, nuevo_nombre: str) -> None:
        p = self.obtener(pid)
        nombre_prev = p.nombre
        p.nombre = nuevo_nombre
        self._index_update_nombre(p, nombre_prev)

    def obtener(self, pid: str) -> Producto:
        if pid not in self._productos:
            raise KeyError(f"No existe producto con ID '{pid}'.")
        return self._productos[pid]

    def buscar_por_nombre(self, consulta: str) -> List[Producto]:
        """Búsqueda flexible: coincide por subcadena normalizada."""
        q = _norm(consulta)
        if q in self._index_nombre:
            # coincidencia exacta del nombre normalizado -> rápido
            ids = self._index_nombre[q]
            return [self._productos[i] for i in ids]
        # búsqueda por subcadena
        res = []
        for p in self._productos.values():
            if q in _norm(p.nombre):
                res.append(p)
        return res

    def listar_todos(self, orden: str = "nombre") -> List[Producto]:
        items = list(self._productos.values())
        if orden == "id":
            items.sort(key=lambda x: x.pid)
        elif orden == "cantidad":
            items.sort(key=lambda x: x.cantidad, reverse=True)
        elif orden == "precio":
            items.sort(key=lambda x: x.precio, reverse=True)
        else:
            items.sort(key=lambda x: _norm(x.nombre))
        return items

    # --- Persistencia ---
    def guardar(self, ruta: str = "inventario.json") -> None:
        data = {pid: p.to_dict() for pid, p in self._productos.items()}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def cargar(ruta: str = "inventario.json") -> "Inventario":
        inv = Inventario()
        if not os.path.exists(ruta):
            return inv
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        # data es dict pid -> dict del producto
        for pid, pdict in data.items():
            p = Producto.from_dict(pdict)
            inv._productos[pid] = p
            inv._index_add(p)
        return inv


# ---------- Interfaz de usuario (menú de consola) ----------
def _input_no_vacio(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("️  No puede estar vacío.")


def _input_int(prompt: str, minimo: int = 0) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if v < minimo:
                print(f"️  Debe ser un entero >= {minimo}.")
            else:
                return v
        except ValueError:
            print("  Ingresa un entero válido.")


def _input_float(prompt: str, minimo: float = 0.0) -> float:
    while True:
        s = input(prompt).strip().replace(',', '.')
        try:
            v = float(s)
            if v < minimo:
                print(f"️  Debe ser un número >= {minimo}.")
            else:
                return v
        except ValueError:
            print("️  Ingresa un número válido.")


def _print_tabla(productos: List[Producto]) -> None:
    if not productos:
        print("No hay productos para mostrar.")
        return
    headers = ["ID", "Nombre", "Cantidad", "Precio (USD)"]
    cols = [10, 30, 10, 14]

    def fmt(cadena, n):
        s = str(cadena)
        return (s[:n-1] + "…") if len(s) > n else s.ljust(n)

    linea = "+".join(["-" * c for c in cols])
    print(
        fmt(headers[0], cols[0]),
        fmt(headers[1], cols[1]),
        fmt(headers[2], cols[2]),
        fmt(headers[3], cols[3]),
        sep=" | ",
    )
    print(linea)
    for p in productos:
        print(
            fmt(p.pid, cols[0]),
            fmt(p.nombre, cols[1]),
            fmt(p.cantidad, cols[2]),
            fmt(f"{p.precio:.2f}", cols[3]),
            sep=" | ",
        )


def menu():
    ruta_archivo = "inventario.json"
    inventario = Inventario.cargar(ruta_archivo)
    print(" Sistema Avanzado de Gestión de Inventario")
    print("Archivo de datos:", ruta_archivo)
    while True:
        print("""
Seleccione una opción:
  1) Agregar producto
  2) Eliminar producto por ID
  3) Actualizar cantidad
  4) Actualizar precio
  5) Actualizar nombre
  6) Buscar por nombre
  7) Listar todos
  8) Guardar
  9) Cargar
  0) Salir
""")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                pid = _input_no_vacio("ID único: ")
                nombre = _input_no_vacio("Nombre: ")
                cantidad = _input_int("Cantidad (>=0): ", 0)
                precio = _input_float("Precio (>=0): ", 0.0)
                inventario.agregar(Producto(pid, nombre, cantidad, precio))
                print(" Producto agregado.")
            elif op == "2":
                pid = _input_no_vacio("ID a eliminar: ")
                eliminado = inventario.eliminar(pid)
                print(f"️  Eliminado: {eliminado}")
            elif op == "3":
                pid = _input_no_vacio("ID: ")
                cantidad = _input_int("Nueva cantidad (>=0): ", 0)
                inventario.actualizar_cantidad(pid, cantidad)
                print(" Cantidad actualizada.")
            elif op == "4":
                pid = _input_no_vacio("ID: ")
                precio = _input_float("Nuevo precio (>=0): ", 0.0)
                inventario.actualizar_precio(pid, precio)
                print(" Precio actualizado.")
            elif op == "5":
                pid = _input_no_vacio("ID: ")
                nombre = _input_no_vacio("Nuevo nombre: ")
                inventario.actualizar_nombre(pid, nombre)
                print("  Nombre actualizado.")
            elif op == "6":
                q = _input_no_vacio("Buscar nombre (subcadena): ")
                res = inventario.buscar_por_nombre(q)
                _print_tabla(res)
            elif op == "7":
                orden = input("Orden [nombre|id|cantidad|precio]: ").strip().lower() or "nombre"
                _print_tabla(inventario.listar_todos(orden=orden))
            elif op == "8":
                inventario.guardar(ruta_archivo)
                print(" Guardado en", ruta_archivo)
            elif op == "9":
                inventario = Inventario.cargar(ruta_archivo)
                print(" Inventario cargado desde", ruta_archivo)
            elif op == "0":
                # Guardado automático al salir
                inventario.guardar(ruta_archivo)
                print(" Guardado y salida. ¡Hasta luego!")
                break
            else:
                print("️  Opción no válida.")
        except Exception as e:
            print(" Error:", e)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nSaliendo...")
