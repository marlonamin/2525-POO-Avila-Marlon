from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional


# ---------------------------
#  CLASES DEL DOMINIO
# ---------------------------

@dataclass(frozen=True)
class Libro:
    """
    Representa un libro.
    - 'meta' es una TUPLA inmutable: (titulo, autor).
      Se usa tupla porque no cambiará una vez creado.
    - 'categoria' y 'isbn' identifican y organizan el libro.
    """
    meta: Tuple[str, str]          # (título, autor)
    categoria: str
    isbn: str

    @property
    def titulo(self) -> str:
        return self.meta[0]

    @property
    def autor(self) -> str:
        return self.meta[1]

    def __str__(self) -> str:
        return f"{self.titulo} — {self.autor} [{self.categoria}] (ISBN {self.isbn})"


@dataclass
class Usuario:
    """Representa a un usuario de la biblioteca."""
    nombre: str
    user_id: str
    # Lista de ISBNs actualmente prestados al usuario
    prestados: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.nombre} (ID: {self.user_id})"


# ---------------------------
#  GESTOR DE BIBLIOTECA
# ---------------------------

class Biblioteca:
    """
    Gestiona colecciones de libros, usuarios y préstamos.
    - libros: diccionario ISBN -> Libro (búsqueda eficiente)
    - user_ids: conjunto de IDs para garantizar unicidad
    - usuarios: diccionario ID -> Usuario
    - prestamos: diccionario ISBN -> user_id (quién lo tiene)
    """
    def __init__(self) -> None:
        self.libros: Dict[str, Libro] = {}
        self.user_ids: Set[str] = set()
        self.usuarios: Dict[str, Usuario] = {}
        self.prestamos: Dict[str, str] = {}

    # ---------- Libros ----------
    def anadir_libro(self, libro: Libro) -> None:
        if libro.isbn in self.libros:
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn}.")
        self.libros[libro.isbn] = libro

    def quitar_libro(self, isbn: str) -> None:
        if isbn in self.prestamos:
            raise ValueError("No se puede eliminar: el libro está prestado.")
        if isbn not in self.libros:
            raise KeyError("ISBN no encontrado.")
        del self.libros[isbn]

    # ---------- Usuarios ----------
    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.user_id in self.user_ids:
            raise ValueError(f"El ID {usuario.user_id} ya está registrado.")
        self.user_ids.add(usuario.user_id)
        self.usuarios[usuario.user_id] = usuario

    def dar_de_baja_usuario(self, user_id: str) -> None:
        u = self.usuarios.get(user_id)
        if not u:
            raise KeyError("Usuario no encontrado.")
        if u.prestados:
            raise ValueError("No se puede dar de baja: el usuario tiene libros prestados.")
        self.user_ids.remove(user_id)
        del self.usuarios[user_id]

    # ---------- Préstamos ----------
    def prestar_libro(self, isbn: str, user_id: str) -> None:
        if isbn not in self.libros:
            raise KeyError("ISBN no encontrado en el catálogo.")
        if user_id not in self.usuarios:
            raise KeyError("Usuario no registrado.")
        if isbn in self.prestamos:
            actual = self.prestamos[isbn]
            raise ValueError(f"El libro ya está prestado al usuario {actual}.")
        # registrar préstamo
        self.prestamos[isbn] = user_id
        self.usuarios[user_id].prestados.append(isbn)

    def devolver_libro(self, isbn: str) -> None:
        if isbn not in self.prestamos:
            raise ValueError("Ese ISBN no está prestado.")
        user_id = self.prestamos.pop(isbn)
        u = self.usuarios[user_id]
        # quitar ISBN de la lista del usuario (si existiera)
        try:
            u.prestados.remove(isbn)
        except ValueError:
            pass  # coherencia defensiva

    # ---------- Consultas ----------
    def buscar_libros(
        self,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        categoria: Optional[str] = None,
    ) -> List[Libro]:
        """
        Búsqueda flexible por coincidencia parcial (case-insensitive).
        Si un criterio es None, no se filtra por ese campo.
        """
        q_tit = (titulo or "").strip().lower()
        q_aut = (autor or "").strip().lower()
        q_cat = (categoria or "").strip().lower()

        def match(lib: Libro) -> bool:
            ok_t = q_tit in lib.titulo.lower() if q_tit else True
            ok_a = q_aut in lib.autor.lower() if q_aut else True
            ok_c = q_cat in lib.categoria.lower() if q_cat else True
            return ok_t and ok_a and ok_c

        return [lib for lib in self.libros.values() if match(lib)]

    def libros_prestados_de(self, user_id: str) -> List[Libro]:
        if user_id not in self.usuarios:
            raise KeyError("Usuario no registrado.")
        isbns = self.usuarios[user_id].prestados
        return [self.libros[i] for i in isbns if i in self.libros]

    def disponible(self, isbn: str) -> bool:
        if isbn not in self.libros:
            raise KeyError("ISBN no encontrado en el catálogo.")
        return isbn not in self.prestamos

    # ---------- Utilidades ----------
    def __str.me__(self, libros: List[Libro]) -> str:
        return "\n".join(f"- {str(l)}" for l in libros) or "(sin resultados)"

    def resumen(self) -> str:
        return (
            f"Libros: {len(self.libros)} | Usuarios: {len(self.usuarios)} | "
            f"Prestamos activos: {len(self.prestamos)}"
        )


# ---------------------------
#  PRUEBAS / DEMO
# ---------------------------

if __name__ == "__main__":
    bib = Biblioteca()

    # 1) Registrar usuarios (set para IDs únicos)
    u1 = Usuario("Marlon Ávila", "U001")
    u2 = Usuario("Valentina Ruiz", "U002")
    bib.registrar_usuario(u1)
    bib.registrar_usuario(u2)

    # 2) Añadir libros (tupla para (titulo, autor))
    l1 = Libro(("Python Crash Course", "Eric Matthes"), "Programación", "9781593279288")
    l2 = Libro(("Cien años de soledad", "Gabriel García Márquez"), "Novela", "9780307474728")
    l3 = Libro(("Clean Code", "Robert C. Martin"), "Ingeniería", "9780132350884")
    bib.anadir_libro(l1)
    bib.anadir_libro(l2)
    bib.anadir_libro(l3)

    print("== Estado inicial ==")
    print(bib.resumen())

    # 3) Buscar por autor / título / categoría
    print("\nBuscar por categoría 'program':")
    for x in bib.buscar_libros(categoria="program"):
        print("  ", x)

    print("\nBuscar por autor 'martin':")
    for x in bib.buscar_libros(autor="martin"):
        print("  ", x)

    # 4) Prestar y devolver
    print("\n¿Disponible Clean Code?", bib.disponible("9780132350884"))
    bib.prestar_libro("9780132350884", "U001")
    print("Prestado 'Clean Code' a Marlon.")
    print("¿Disponible Clean Code?", bib.disponible("9780132350884"))

    print("\nLibros prestados a Marlon:")
    for x in bib.libros_prestados_de("U001"):
        print("  ", x)

    # Intento de eliminar libro prestado (debe fallar)
    try:
        bib.quitar_libro("9780132350884")
    except Exception as e:
        print("\nNo se pudo eliminar libro prestado:", e)

    # Devolver
    bib.devolver_libro("9780132350884")
    print("\nDevuelto 'Clean Code'. ¿Disponible?", bib.disponible("9780132350884"))

    # 5) Dar de baja usuario con préstamos (probar validación)
    try:
        bib.prestar_libro("9780307474728", "U002")
        bib.dar_de_baja_usuario("U002")
    except Exception as e:
        print("\nNo se pudo dar de baja U002:", e)
        # devolver y dar de baja
        bib.devolver_libro("9780307474728")
        bib.dar_de_baja_usuario("U002")
        print("U002 dado de baja exitosamente.")

    print("\n== Estado final ==")
    print(bib.resumen())
