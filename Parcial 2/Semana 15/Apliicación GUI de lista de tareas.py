import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas")
        self.geometry("420x350")

        # ---- Entrada + Botones
        top = ttk.Frame(self, padding=8); top.pack(fill="x")
        self.entry = ttk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_task)

        ttk.Button(top, text="Añadir Tarea", command=self.add_task).pack(side="left", padx=4)
        ttk.Button(top, text="Completada", command=self.toggle_done).pack(side="left")
        ttk.Button(top, text="Eliminar", command=self.delete_task).pack(side="left", padx=4)

        # ---- Lista (Treeview con estilos)
        self.tree = ttk.Treeview(self, columns=("tarea",), show="headings", selectmode="browse")
        self.tree.heading("tarea", text="Tarea")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", self.toggle_done)   # Doble clic marca/ desmarca
        self.bind("<Delete>", self.delete_task)          # Tecla Supr elimina

        # Estilo para tareas completadas (tachado + gris)
        base_font = tkfont.nametofont("TkDefaultFont")
        done_font = base_font.copy(); done_font.configure(overstrike=1)
        self.tree.tag_configure("done", font=done_font, foreground="#6b7280")

    # ---- Acciones
    def add_task(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.tree.insert("", "end", values=(text,))
        self.entry.delete(0, "end")

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Atención", "Selecciona una tarea primero.")
            return None
        return sel[0]

    def toggle_done(self, event=None):
        iid = self._selected()
        if not iid: return
        tags = set(self.tree.item(iid, "tags"))
        if "done" in tags:
            tags.discard("done")
        else:
            tags.add("done")
        self.tree.item(iid, tags=tuple(tags))

    def delete_task(self, event=None):
        iid = self._selected()
        if iid: self.tree.delete(iid)

if __name__ == "__main__":
    TodoApp().mainloop()
