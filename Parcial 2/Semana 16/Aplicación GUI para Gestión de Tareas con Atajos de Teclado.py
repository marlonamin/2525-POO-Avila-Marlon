import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Tareas")
        self.geometry("460x360")
        self.minsize(420, 300)

        # ---- Entrada + Botones
        top = ttk.Frame(self, padding=8); top.pack(fill="x")
        self.entry = ttk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True)
        ttk.Button(top, text="Añadir", command=self.add_task).pack(side="left", padx=4)
        ttk.Button(top, text="Completada", command=self.toggle_done).pack(side="left")
        ttk.Button(top, text="Eliminar", command=self.delete_task).pack(side="left", padx=4)

        # ---- Lista (Treeview)
        self.tree = ttk.Treeview(self, columns=("tarea",), show="headings", selectmode="browse")
        self.tree.heading("tarea", text="Tarea")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", self.toggle_done)

        # Estilo para completadas: tachado + gris
        base_font = tkfont.nametofont("TkDefaultFont")
        done_font = base_font.copy()
        done_font.configure(overstrike=1)
        self.tree.tag_configure("done", font=done_font, foreground="#6b7280")

        # ---- Atajos de teclado (forma segura)
        self.entry.bind("<Return>", self.add_task)                    # Enter añade (enfocado en Entry)
        self.bind("<Key-c>", self.toggle_done)                        # c marca
        self.bind("<Key-C>", self.toggle_done)                        # C marca
        self.bind("<Key-d>", self.delete_task)                        # d elimina
        self.bind("<Key-D>", self.delete_task)                        # D elimina
        self.bind("<Delete>", self.delete_task)                       # Supr elimina
        self.bind("<Escape>", lambda e: self.destroy())               # Esc cierra

        # Enfocar entrada al iniciar
        self.after(100, self.entry.focus_set)

        # Ayuda
        ttk.Label(self, anchor="w", padding=(8, 2),
                  text="Atajos: Enter=añadir · C=marcar · D/Supr=eliminar · Doble clic=marcar · Esc=cerrar").pack(
            fill="x", side="bottom")

    # ---- Lógica
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
        if not iid:
            return
        tags = set(self.tree.item(iid, "tags"))
        if "done" in tags:
            tags.remove("done")
        else:
            tags.add("done")
        self.tree.item(iid, tags=tuple(tags))

    def delete_task(self, event=None):
        iid = self._selected()
        if iid:
            self.tree.delete(iid)

if __name__ == "__main__":
    TodoApp().mainloop()