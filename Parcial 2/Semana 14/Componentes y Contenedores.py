"""Agenda Personal (ES)
GUI con Tkinter si está disponible; si no, modo consola.
Uso:  python agenda.py   |   python agenda.py --cli   |   python agenda.py --test
"""
from __future__ import annotations

# Detectar Tkinter
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TK = True
except Exception:
    TK = False

from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
import argparse

# ---- Validación ----

def es_fecha(s: str) -> bool:
    try: datetime.strptime(s, "%Y-%m-%d"); return True
    except ValueError: return False

def es_hora(s: str) -> bool:
    try: datetime.strptime(s, "%H:%M"); return True
    except ValueError: return False

# ---- Modelo ----
@dataclass
class Evento:
    fecha: str; hora: str; descripcion: str

class Agenda:
    def __init__(self): self.items: List[Evento] = []
    def agregar(self, f: str, h: str, d: str):
        if not (f and h and d): raise ValueError("Faltan datos")
        if not es_fecha(f): raise ValueError("Fecha inválida (YYYY-MM-DD)")
        if not es_hora(h): raise ValueError("Hora inválida (HH:MM)")
        self.items.append(Evento(f,h,d))
        self.items.sort(key=lambda e:(e.fecha,e.hora,e.descripcion))
    def eliminar_indices(self, idxs: List[int]) -> int:
        n=0
        for i in sorted(set(idxs), reverse=True):
            if 0<=i<len(self.items): del self.items[i]; n+=1
        return n

# ---- GUI ----
if TK:
    class DatePicker(tk.Toplevel):
        def __init__(self, master: tk.Misc, initial: Optional[date]=None):
            super().__init__(master); self.title("Fecha"); self.resizable(False,False); self.transient(master); self.grab_set()
            h=date.today(); initial=initial or h
            frm=ttk.Frame(self,padding=8); frm.grid()
            yrs=[str(y) for y in range(h.year-5,h.year+6)]; mos=[f"{m:02d}" for m in range(1,13)]; dys=[f"{d:02d}" for d in range(1,32)]
            for i,t in enumerate(("Año","Mes","Día")): ttk.Label(frm,text=t).grid(row=0,column=i)
            self.y=ttk.Combobox(frm,values=yrs,width=6,state="readonly"); self.m=ttk.Combobox(frm,values=mos,width=4,state="readonly"); self.d=ttk.Combobox(frm,values=dys,width=4,state="readonly")
            self.y.set(str(initial.year)); self.m.set(f"{initial.month:02d}"); self.d.set(f"{initial.day:02d}")
            self.y.grid(row=1,column=0,padx=2,pady=2); self.m.grid(row=1,column=1,padx=2,pady=2); self.d.grid(row=1,column=2,padx=2,pady=2)
            b=ttk.Frame(frm); b.grid(row=2,column=0,columnspan=3,pady=4)
            ttk.Button(b,text="Hoy",command=self._hoy).grid(row=0,column=0,padx=2)
            ttk.Button(b,text="OK",command=self._ok).grid(row=0,column=1,padx=2)
            ttk.Button(b,text="Cancelar",command=self.destroy).grid(row=0,column=2,padx=2)
            self.result=None
        def _hoy(self): H=date.today(); self.y.set(str(H.year)); self.m.set(f"{H.month:02d}"); self.d.set(f"{H.day:02d}")
        def _ok(self):
            f=f"{self.y.get()}-{self.m.get()}-{self.d.get()}"
            if es_fecha(f): self.result=f; self.destroy()
            else: messagebox.showerror("Error","Fecha inválida")

    class App(tk.Tk):
        def __init__(self, model: Agenda):
            super().__init__(); self.m=model; self.title("Agenda Personal"); self.geometry("680x480")
            a=ttk.LabelFrame(self,text="Nuevo",padding=8); a.pack(fill="x",padx=10,pady=6)
            e=ttk.LabelFrame(self,text="Eventos",padding=8); e.pack(fill="both",expand=True,padx=10,pady=6)
            f=ttk.Frame(self); f.pack(fill="x",padx=10,pady=6)
            ttk.Label(a,text="Fecha").grid(row=0,column=0,sticky="w"); self.fch=ttk.Entry(a,width=14); self.fch.grid(row=1,column=0)
            ttk.Button(a,text="📅",width=3,command=self.sel_fecha).grid(row=1,column=1,padx=3)
            ttk.Label(a,text="Hora").grid(row=0,column=2,sticky="w",padx=(10,0)); self.hra=ttk.Entry(a,width=8); self.hra.grid(row=1,column=2)
            ttk.Label(a,text="Descripción").grid(row=0,column=3,sticky="w",padx=(10,0)); self.dsc=ttk.Entry(a,width=40); self.dsc.grid(row=1,column=3,sticky="we")
            a.columnconfigure(3,weight=1)
            cols=("fecha","hora","desc"); self.tree=ttk.Treeview(e,columns=cols,show="headings",height=12)
            for c,t in zip(cols,["Fecha","Hora","Descripción"]): self.tree.heading(c,text=t)
            self.tree.column("fecha",width=110,anchor="center"); self.tree.column("hora",width=80,anchor="center")
            self.tree.pack(fill="both",expand=True); vs=ttk.Scrollbar(e,orient="vertical",command=self.tree.yview); self.tree.configure(yscroll=vs.set); vs.pack(side="right",fill="y")
            ttk.Button(f,text="Agregar",command=self.add).pack(side="left"); ttk.Button(f,text="Eliminar",command=self.rm).pack(side="left",padx=6); ttk.Button(f,text="Salir",command=self.destroy).pack(side="right")
        def sel_fecha(self):
            init=None
            if es_fecha(self.fch.get().strip()): init=datetime.strptime(self.fch.get().strip(),"%Y-%m-%d").date()
            dp=DatePicker(self,init); self.wait_window(dp)
            if dp.result: self.fch.delete(0,tk.END); self.fch.insert(0,dp.result)
        def _refresh(self):
            for i in self.tree.get_children(): self.tree.delete(i)
            for ev in self.m.items: self.tree.insert("",tk.END,values=(ev.fecha,ev.hora,ev.descripcion))
        def add(self):
            try: self.m.agregar(self.fch.get().strip(), self.hra.get().strip(), self.dsc.get().strip())
            except ValueError as e: messagebox.showerror("Error",str(e)); return
            self._refresh(); self.hra.delete(0,tk.END); self.dsc.delete(0,tk.END)
        def rm(self):
            sel=self.tree.selection()
            if not sel: messagebox.showinfo("Info","Selecciona un evento"); return
            if not messagebox.askyesno("Confirmar","¿Eliminar seleccionado(s)?"): return
            idxs=[]; cur=[(ev.fecha,ev.hora,ev.descripcion) for ev in self.m.items]
            for iid in sel:
                v=tuple(self.tree.item(iid,"values"))
                if v in cur: idxs.append(cur.index(v))
            self.m.eliminar_indices(idxs); self._refresh()

# ---- CLI ----

def cli(model: Agenda):
    print("Agenda (consola). Comandos: a=agregar, l=listar, e=eliminar, s=salir")
    while True:
        c=input("> ").strip().lower()
        if c in ("s","salir","q"): print("Adiós"); return
        if c in ("l","listar"):
            if not model.items: print("(sin eventos)")
            else:
                for i,ev in enumerate(model.items): print(f"{i:02d} | {ev.fecha} {ev.hora} | {ev.descripcion}")
        elif c in ("a","agregar"):
            f=input("Fecha YYYY-MM-DD: ").strip(); h=input("Hora HH:MM: ").strip(); d=input("Descripción: ").strip()
            try: model.agregar(f,h,d); print("✔ Agregado")
            except ValueError as e: print(f"✘ {e}")
        elif c in ("e","eliminar"):
            try: idxs=[int(x) for x in input("Índices (coma): ").split(',') if x.strip()]
            except ValueError: print("✘ Índices inválidos"); continue
            print(f"✔ Eliminados: {model.eliminar_indices(idxs)}")
        else: print("Comando no reconocido")

# ---- Pruebas ----

def tests():
    assert es_fecha("2025-12-31") and not es_fecha("2025-02-30")
    assert es_hora("23:59") and not es_hora("24:00")
    m=Agenda(); m.agregar("2025-01-01","08:00","A"); m.agregar("2025-01-02","09:00","B")
    assert len(m.items)==2
    try: m.agregar("2025-13-01","10:00","X"); raise AssertionError
    except ValueError: pass
    n=m.eliminar_indices([0]); assert n==1 and len(m.items)==1
    print("Pruebas OK")

# ---- Main ----
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--cli",action="store_true")
    ap.add_argument("--test",action="store_true")
    a=ap.parse_args()
    if a.test: tests(); raise SystemExit
    modelo=Agenda()
    if TK and not a.cli:
        app=App(modelo)  # type: ignore
        app.mainloop()
    else:
        if not TK: print("[Aviso] Tkinter no está disponible. Usando consola.")
        cli(modelo)