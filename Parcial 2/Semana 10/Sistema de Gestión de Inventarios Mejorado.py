# Sistema de Gestión de Inventarios (POO) con persistencia en archivo .txt (CSV) y manejo de excepciones.

from typing import Any, List, Optional, Dict
import csv
import os

ARCHIVO = "inventario.txt"   # .txt con formato CSV (encabezados)


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

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "nombre": self.nombre, "cantidad": self.cantidad, "precio": self.precio}

    def __repr__(self) -> str:
        return f"Producto(id={self.id!r}, nombre={self.nombre!r}, cantidad={self.cantidad}, precio={self.precio:.2f})"

    # --------- helpers para CSV ---------
    @staticmethod
    def from_row(row: Dict[str, str]) -> "Producto":
        """Construye un Producto desde un diccionario leído del CSV con validación robusta."""
        try:
            return Producto(
                pid=row["id"].strip(),
                nombre=row["nombre"].strip(),
                cantidad=int(row["cantidad"]),
                precio=float(row["precio"]),
            )
        except (KeyError, ValueError) as e:
            raise ValueError(f"Fila inválida en archivo: {row} -> {e}")


class Inventario:
    """Estructura de datos personalizada: lista de productos + operaciones CRUD + persistencia."""

    def __init__(self) -> None:
        self._productos: List[Producto] = []

    # ---------- Persistencia ----------
    def cargar_desde_archivo(self, ruta: str = ARCHIVO) -> None:
        """Carga productos desde archivo .txt (CSV con encabezados). No es error si no existe."""
        if not os.path.exists(ruta):
            print(f"[INFO] Archivo '{ruta}' no existe. Se creará al guardar.")
            return
        try:
            with open(ruta, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                self._productos.clear()
                for row in reader:
                    prod = Producto.from_row(row)
                    # evitar duplicados por ID dentro del archivo
                    if self.obtener_por_id(prod.id) is None:
                        self._productos.append(prod)
                    else:
                        print(f"[WARN] ID duplicado '{prod.id}' en archivo. Se omite esa fila.")
            print(f"[OK] Inventario cargado: {len(self._productos)} productos.")
        except PermissionError:
            print(f"[ERROR] Permisos insuficientes para leer '{ruta}'.")
        except FileNotFoundError:
            print(f"[ERROR] Archivo '{ruta}' no encontrado.")
        except ValueError as e:
            print(f"[ERROR] Datos corruptos: {e}")

    def guardar_en_archivo(self, ruta: str = ARCHIVO) -> None:
        """Guarda todos los productos en archivo .txt (CSV)."""
        try:
            with open(ruta, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "nombre", "cantidad", "precio"])
                writer.writeheader()
                for p in self._productos:
                    writer.writerow({"id": p.id, "nombre": p.nombre, "cantidad": p.cantidad, "precio": f"{p.precio:.2f}"})
            print(f"[OK] Cambios guardados en '{ruta}'.")
        except PermissionError:
            print(f"[ERROR] Permisos insuficientes para escribir en '{ruta}'.")
        except OSError as e:
            print(f"[ERROR] No se pudo escribir en '{ruta}': {e}")

    # ---------- Utilidades internas ----------
    def _buscar_idx_por_id(self, pid: str) -> Optional[int]:
        for i, p in enumerate(self._productos):
            if p.id == pid:
                return i
        return None

    def obtener_por_id(self, pid: str) -> Optional[Producto]:
        idx = self._buscar_idx_por_id(pid)
        return self._productos[idx] if idx is not None else None

    # ---------- CRUD (guardan automáticamente) ----------
    def agregar(self, producto: Producto) -> None:
        if self.obtener_por_id(producto.id) is not None:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        self._productos.append(producto)
        self.guardar_en_archivo()
        print(f"[OK] Producto '{producto.nombre}' añadido (ID={producto.id}).")

    def eliminar(self, pid: str) -> bool:
        idx = self._buscar_idx_por_id(pid)
        if idx is None:
            return False
        eliminado = self._productos.pop(idx)
        self.guardar_en_archivo()
        print(f"[OK] Producto '{eliminado.nombre}' (ID={pid}) eliminado.")
        return True

    def actualizar(self, pid: str, *, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        prod = self.obtener_por_id(pid)
        if prod is None:
            return False
        if cantidad is not None:
            prod.cantidad = cantidad
        if precio is not None:
            prod.precio = precio
        self.guardar_en_archivo()
        print(f"[OK] Producto ID={pid} actualizado.")
        return True

    # ---------- Búsquedas/consultas ----------
    def buscar_por_nombre(self, consulta: str) -> List[Producto]:
        q = consulta.strip().lower()
        return [p for p in self._productos if q in p.nombre.lower()]

    def listar_todos(self) -> List[Producto]:
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
    if not productos:
        print("No hay productos para mostrar.")
        return
    headers = ["ID", "Nombre", "Cantidad", "Precio"]
    filas = [[p.id, p.nombre, str(p.cantidad), f"{p.precio:.2f}"] for p in productos]
    anchos = [max(len(h), *(len(f[i]) for f in filas)) for i, h in enumerate(headers)]
    linea = " | ".join(h.ljust(anchos[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * anchos[i] for i in range(len(headers)))
    print(linea); print(sep)
    for f in filas:
        print(" | ".join(f[i].ljust(anchos[i]) for i in range(len(headers))))

# -------------------- Menú --------------------

def menu() -> None:
    inv = Inventario()
    # #2 Recuperación de inventarios desde archivos (carga automática)
    inv.cargar_desde_archivo()

    opciones = {
        "1": "Añadir producto",
        "2": "Eliminar producto por ID",
        "3": "Actualizar cantidad/precio por ID",
        "4": "Buscar productos por nombre",
        "5": "Mostrar todos los productos",
        "6": "Guardar manualmente",
        "0": "Salir",
    }

    while True:
        print("\n=== Sistema de Gestión de Inventarios ===")
        for k, v in opciones.items(): print(f"{k}. {v}")
        op = input("Seleccione una opción: ").strip()

        try:
            if op == "1":
                pid = input_no_vacio("ID: ")
                nombre = input_no_vacio("Nombre: ")
                cantidad = input_entero("Cantidad: ", minimo=0)
                precio = input_float("Precio: ", minimo=0.0)
                inv.agregar(Producto(pid, nombre, cantidad, precio))

            elif op == "2":
                pid = input_no_vacio("ID a eliminar: ")
                if not inv.eliminar(pid):
                    print("❌ No se encontró un producto con ese ID.")

            elif op == "3":
                pid = input_no_vacio("ID a actualizar: ")
                prod = inv.obtener_por_id(pid)
                if not prod:
                    print("❌ No existe un producto con ese ID.")
                else:
                    print(f"Producto actual: {prod}")
                    cambiar_cant = input("¿Actualizar cantidad? (s/n): ").strip().lower() == "s"
                    cambiar_prec = input("¿Actualizar precio? (s/n): ").strip().lower() == "s"
                    kwargs = {}
                    if cambiar_cant: kwargs["cantidad"] = input_entero("Nueva cantidad: ", minimo=0)
                    if cambiar_prec: kwargs["precio"] = input_float("Nuevo precio: ", minimo=0.0)
                    if kwargs and inv.actualizar(pid, **kwargs):
                        pass
                    else:
                        print("No se realizaron cambios.")

            elif op == "4":
                q = input_no_vacio("Buscar por nombre (coincidencia parcial): ")
                imprimir_tabla(inv.buscar_por_nombre(q))

            elif op == "5":
                imprimir_tabla(inv.listar_todos())

            elif op == "6":
                inv.guardar_en_archivo()

            elif op == "0":
                print("¡Hasta luego!")
                break

            else:
                print("Opción inválida. Intente de nuevo.")

        # Manejo genérico de errores de archivo (además de los ya controlados dentro de los métodos)
        except PermissionError:
            print("[ERROR] Permisos insuficientes para acceder al archivo de inventario.")
        except FileNotFoundError:
            print("[ERROR] No se encuentra el archivo de inventario.")
        except (TypeError, ValueError) as e:
            print(f"[ERROR] Dato inválido: {e}")
        except Exception as e:
            print(f"[ERROR] Inesperado: {e}")

if __name__ == "__main__":
    menu()
