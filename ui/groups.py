import customtkinter as ctk
from db.database import get_session
from db.models import Grupo, Admin


def _get_grupos():
    session = get_session()
    try:
        return session.query(Grupo).order_by(Grupo.grado, Grupo.nombre).all()
    finally:
        session.close()


class GroupsFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._build()
        self._cargar_tabla()

    def _build(self):
        ctk.CTkLabel(self, text="Grupos", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

        # Formulario
        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(form, text="Nombre:").grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self._nombre = ctk.CTkEntry(form, width=80, placeholder_text="1A")
        self._nombre.grid(row=0, column=1, padx=8, pady=10)

        ctk.CTkLabel(form, text="Grado:").grid(row=0, column=2, padx=12, pady=10, sticky="w")
        self._grado = ctk.CTkEntry(form, width=60, placeholder_text="1")
        self._grado.grid(row=0, column=3, padx=8, pady=10)

        ctk.CTkLabel(form, text="Turno:").grid(row=0, column=4, padx=12, pady=10, sticky="w")
        self._turno = ctk.CTkOptionMenu(form, values=["matutino", "vespertino", "nocturno"], width=140)
        self._turno.grid(row=0, column=5, padx=8, pady=10)

        ctk.CTkButton(form, text="Agregar grupo", command=self._agregar).grid(
            row=0, column=6, padx=12, pady=10)

        self._msg = ctk.CTkLabel(form, text="", text_color="#2ecc71")
        self._msg.grid(row=1, column=0, columnspan=7, padx=12, pady=(0, 8))

        # Tabla
        header = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        header.pack(fill="x")
        for col, w in [("ID", 50), ("Nombre", 120), ("Grado", 80), ("Turno", 140), ("Acciones", 160)]:
            ctk.CTkLabel(header, text=col, font=("Arial", 12, "bold"),
                         width=w, anchor="w").pack(side="left", padx=8, pady=6)

        self._tabla = ctk.CTkScrollableFrame(self)
        self._tabla.pack(fill="both", expand=True, pady=(2, 0))

    def _cargar_tabla(self):
        for w in self._tabla.winfo_children():
            w.destroy()
        for g in _get_grupos():
            self._fila(g)

    def _fila(self, g: Grupo):
        row = ctk.CTkFrame(self._tabla, fg_color="transparent")
        row.pack(fill="x", pady=1)
        for val, w in [(g.id, 50), (g.nombre, 120), (g.grado, 80), (g.turno, 140)]:
            ctk.CTkLabel(row, text=str(val), width=w, anchor="w").pack(side="left", padx=8, pady=4)
        ctk.CTkButton(row, text="Editar", width=70,
                      command=lambda gid=g.id: self._editar(gid)).pack(side="left", padx=4)
        ctk.CTkButton(row, text="Eliminar", width=70, fg_color="#c0392b", hover_color="#a93226",
                      command=lambda gid=g.id: self._eliminar(gid)).pack(side="left", padx=4)

    def _agregar(self):
        nombre = self._nombre.get().strip()
        grado_str = self._grado.get().strip()
        turno = self._turno.get()
        if not nombre or not grado_str or not grado_str.isdigit():
            self._msg.configure(text="Nombre y grado (número) son requeridos.", text_color="#e74c3c")
            return
        session = get_session()
        session.add(Grupo(nombre=nombre, grado=int(grado_str), turno=turno))
        session.commit()
        session.close()
        self._nombre.delete(0, "end")
        self._grado.delete(0, "end")
        self._msg.configure(text="Grupo agregado.", text_color="#2ecc71")
        self._cargar_tabla()

    def _eliminar(self, gid: int):
        session = get_session()
        g = session.query(Grupo).filter_by(id=gid).first()
        if g:
            session.delete(g)
            session.commit()
        session.close()
        self._cargar_tabla()

    def _editar(self, gid: int):
        EditGroupDialog(self, gid, on_save=self._cargar_tabla)


class EditGroupDialog(ctk.CTkToplevel):
    def __init__(self, master, gid: int, on_save):
        super().__init__(master)
        self.title("Editar grupo")
        self.geometry("360x260")
        self.resizable(False, False)
        self.grab_set()
        self._gid = gid
        self._on_save = on_save

        session = get_session()
        g = session.query(Grupo).filter_by(id=gid).first()
        session.close()

        ctk.CTkLabel(self, text="Nombre:").pack(padx=24, anchor="w", pady=(20, 0))
        self._nombre = ctk.CTkEntry(self, width=300)
        self._nombre.insert(0, g.nombre)
        self._nombre.pack(padx=24)

        ctk.CTkLabel(self, text="Grado:").pack(padx=24, anchor="w", pady=(12, 0))
        self._grado = ctk.CTkEntry(self, width=300)
        self._grado.insert(0, str(g.grado))
        self._grado.pack(padx=24)

        ctk.CTkLabel(self, text="Turno:").pack(padx=24, anchor="w", pady=(12, 0))
        self._turno = ctk.CTkOptionMenu(self, values=["matutino", "vespertino", "nocturno"], width=300)
        self._turno.set(g.turno)
        self._turno.pack(padx=24)

        ctk.CTkButton(self, text="Guardar", width=300, command=self._guardar).pack(padx=24, pady=20)

    def _guardar(self):
        session = get_session()
        g = session.query(Grupo).filter_by(id=self._gid).first()
        g.nombre = self._nombre.get().strip()
        g.grado = int(self._grado.get().strip())
        g.turno = self._turno.get()
        session.commit()
        session.close()
        self._on_save()
        self.destroy()
