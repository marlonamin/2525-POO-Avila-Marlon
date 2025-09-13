"""
App GUI Básica con Tkinter
----------------------------------
Requisitos cubiertos:
- Ventana principal con título descriptivo.
- Componentes: Label, Entry (campo de texto), Botones, Tabla (ttk.Treeview).
- Funcionalidades: Agregar a la tabla, Eliminar seleccionado, Limpiar todo.
- Eventos: clic en botones y tecla Enter para agregar.
- Librería: Tkinter (Python estándar).

Cómo ejecutar:
1) Guarda este archivo como app_gui_basica.py
2) Ejecuta:  python app_gui_basica.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # --- Ventana principal ---
        self.title("Gestor de Ítems - GUI Básica (Tkinter)")
        self.geometry("600x400")
        self.minsize(520, 360)

        # --- Estilo ttk ---
        style = ttk.Style(self)
        # Usa tema disponible; si no existe 'clam', Tkinter usará el predeterminado
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # --- Marco superior: entrada y botones ---
        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="Nuevo ítem:").grid(row=0, column=0, sticky="w")

        self.var_texto = tk.StringVar()
        self.entry = ttk.Entry(top, textvariable=self.var_texto)
        self.entry.grid(row=0, column=1, sticky="ew", padx=8)
        self.entry.focus_set()

        btn_agregar = ttk.Button(top, text="Agregar", command=self.agregar)
        btn_agregar.grid(row=0, column=2, padx=(0,8))

        btn_eliminar = ttk.Button(top, text="Eliminar seleccionado", command=self.eliminar_seleccionado)
        btn_eliminar.grid(row=0, column=3)

        # Permitir que la columna 1 (entry) se expanda
        top.columnconfigure(1, weight=1)

        # --- Tabla (Treeview) con barra de desplazamiento ---
        mid = ttk.Frame(self, padding=(12, 0, 12, 0))
        mid.pack(fill="both", expand=True)

        columns = ("item",)
        self.tree = ttk.Treeview(mid, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("item", text="Ítem")
        self.tree.column("item", width=420, anchor="w")

        scrollbar = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Barra inferior: limpiar y estado ---
        bottom = ttk.Frame(self, padding=12)
        bottom.pack(fill="x")

        btn_limpiar = ttk.Button(bottom, text="Limpiar todo", command=self.limpiar_todo)
        btn_limpiar.pack(side="right")

        self.lbl_estado = ttk.Label(bottom, text="Listo.", anchor="w")
        self.lbl_estado.pack(side="left", fill="x", expand=True)

        # --- Atajos de teclado / eventos ---
        self.bind("<Return>", lambda e: self.agregar())         # Enter → Agregar
        self.bind("<Delete>", lambda e: self.eliminar_seleccionado())  # Supr → Eliminar seleccionado
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    # ---------- Lógica ----------
    def agregar(self):
        """Agrega el texto del Entry a la tabla si no está vacío."""
        texto = self.var_texto.get().strip()
        if not texto:
            self._alerta("El campo está vacío. Escribe algo para agregar.")
            return
        self.tree.insert("", "end", values=(texto,))
        self.var_texto.set("")
        self.entry.focus_set()
        self._estado(f"Agregado: {texto}")

    def eliminar_seleccionado(self):
        """Elimina el renglón seleccionado de la tabla (si existe)."""
        sel = self.tree.selection()
        if not sel:
            self._alerta("No hay ningún ítem seleccionado.")
            return
        item_id = sel[0]
        valor = self.tree.item(item_id, "values")[0]
        self.tree.delete(item_id)
        self._estado(f"Eliminado: {valor}")

    def limpiar_todo(self):
        """Borra todos los renglones de la tabla previa confirmación."""
        if not self.tree.get_children():
            self._estado("La tabla ya está vacía.")
            return
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar todos los ítems?"):
            for child in self.tree.get_children():
                self.tree.delete(child)
            self._estado("Tabla limpiada.")

    # ---------- Utilidades UI ----------
    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if sel:
            valor = self.tree.item(sel[0], "values")[0]
            self._estado(f"Seleccionado: {valor}")

    def _estado(self, texto: str):
        self.lbl_estado.config(text=texto)

    def _alerta(self, msg: str):
        messagebox.showwarning("Aviso", msg)
        self._estado(msg)

if __name__ == "__main__":
    AppGUI().mainloop()
