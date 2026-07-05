import customtkinter as ctk
from db.database import get_session
from db.models import Alumno, Grupo, Admin


def _get_grupos():
    session = get_session()
    try:
        return session.query(Grupo).order_by(Grupo.grado, Grupo.nombre).all()
    finally:
        session.close()

def _get_alumnos(grupo_id=None):
    session = get_session()
    try:
        q = session.query(Alumno)
        if grupo_id:
            q = q.filter_by(grupo_id=grupo_id)
        return q.order_by(Alumno.nombre).all()
    finally:
        session.close()


class StudentsFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._grupos: list[Grupo] = []
        self._build()
        self._cargar_tabla()

    def _build(self):
        ctk.CTkLabel(self, text="Alumnos", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

        # Formulario
        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(form, text="Nombre:").grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self._nombre = ctk.CTkEntry(form, width=180, placeholder_text="Nombre completo")
        self._nombre.grid(row=0, column=1, padx=8, pady=10)

        ctk.CTkLabel(form, text="Grupo:").grid(row=0, column=2, padx=12, pady=10, sticky="w")
        self._grupo_var = ctk.StringVar()
        self._grupo_menu = ctk.CTkOptionMenu(form, variable=self._grupo_var, values=["—"], width=140)
        self._grupo_menu.grid(row=0, column=3, padx=8, pady=10)

        ctk.CTkLabel(form, text="RFID (opcional):").grid(row=0, column=4, padx=12, pady=10, sticky="w")
        self._rfid = ctk.CTkEntry(form, width=140, placeholder_text="UID tarjeta")
        self._rfid.grid(row=0, column=5, padx=8, pady=10)

        ctk.CTkButton(form, text="Agregar", command=self._agregar).grid(row=0, column=6, padx=12, pady=10)

        # Filtro por grupo
        filtro = ctk.CTkFrame(self, fg_color="transparent")
        filtro.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(filtro, text="Filtrar por grupo:").pack(side="left", padx=(0, 8))
        self._filtro_var = ctk.StringVar(value="Todos")
        self._filtro_menu = ctk.CTkOptionMenu(filtro, variable=self._filtro_var,
                                               values=["Todos"], width=160,
                                               command=lambda _: self._cargar_tabla())
        self._filtro_menu.pack(side="left")

        self._msg = ctk.CTkLabel(self, text="", text_color="#2ecc71")
        self._msg.pack(anchor="w")

        # Tabla
        header = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        header.pack(fill="x")
        for col, w in [("ID", 50), ("Nombre", 200), ("Grupo", 100), ("Turno", 120), ("RFID", 140), ("Acciones", 160)]:
            ctk.CTkLabel(header, text=col, font=("Arial", 12, "bold"),
                         width=w, anchor="w").pack(side="left", padx=8, pady=6)

        self._tabla = ctk.CTkScrollableFrame(self)
        self._tabla.pack(fill="both", expand=True, pady=(2, 0))

        self._refresh_grupos()

    def _refresh_grupos(self):
        self._grupos = _get_grupos()
        labels = [f"{g.grado}° {g.nombre}" for g in self._grupos]
        self._grupo_menu.configure(values=labels if labels else ["—"])
        if labels:
            self._grupo_var.set(labels[0])
        self._filtro_menu.configure(values=["Todos"] + labels)

    def _cargar_tabla(self):
        for w in self._tabla.winfo_children():
            w.destroy()
        filtro = self._filtro_var.get()
        grupo_id = None
        if filtro != "Todos":
            for g in self._grupos:
                if f"{g.grado}° {g.nombre}" == filtro:
                    grupo_id = g.id
                    break
        for a in _get_alumnos(grupo_id):
            self._fila(a)

    def _fila(self, a: Alumno):
        session = get_session()
        grupo = session.query(Grupo).filter_by(id=a.grupo_id).first()
        session.close()
        row = ctk.CTkFrame(self._tabla, fg_color="transparent")
        row.pack(fill="x", pady=1)
        datos = [
            (a.id, 50), (a.nombre, 200),
            (f"{grupo.grado}° {grupo.nombre}" if grupo else "—", 100),
            (grupo.turno if grupo else "—", 120),
            (a.rfid_uid or "—", 140),
        ]
        for val, w in datos:
            ctk.CTkLabel(row, text=str(val), width=w, anchor="w").pack(side="left", padx=8, pady=4)
        ctk.CTkButton(row, text="Editar", width=70,
                      command=lambda aid=a.id: self._editar(aid)).pack(side="left", padx=4)
        ctk.CTkButton(row, text="Eliminar", width=70, fg_color="#c0392b", hover_color="#a93226",
                      command=lambda aid=a.id: self._eliminar(aid)).pack(side="left", padx=4)

    def _agregar(self):
        nombre = self._nombre.get().strip()
        rfid = self._rfid.get().strip() or None
        seleccion = self._grupo_var.get()
        grupo_id = None
        for g in self._grupos:
            if f"{g.grado}° {g.nombre}" == seleccion:
                grupo_id = g.id
                break
        if not nombre or not grupo_id:
            self._msg.configure(text="Nombre y grupo son requeridos.", text_color="#e74c3c")
            return
        session = get_session()
        session.add(Alumno(nombre=nombre, grupo_id=grupo_id, rfid_uid=rfid))
        session.commit()
        session.close()
        self._nombre.delete(0, "end")
        self._rfid.delete(0, "end")
        self._msg.configure(text="Alumno agregado.", text_color="#2ecc71")
        self._cargar_tabla()

    def _eliminar(self, aid: int):
        session = get_session()
        a = session.query(Alumno).filter_by(id=aid).first()
        if a:
            session.delete(a)
            session.commit()
        session.close()
        self._cargar_tabla()

    def _editar(self, aid: int):
        EditStudentDialog(self, aid, grupos=self._grupos, on_save=self._cargar_tabla)


class EditStudentDialog(ctk.CTkToplevel):
    def __init__(self, master, aid: int, grupos: list, on_save):
        super().__init__(master)
        self.title("Editar alumno")
        self.geometry("380x300")
        self.resizable(False, False)
        self.grab_set()
        self._aid = aid
        self._grupos = grupos
        self._on_save = on_save

        session = get_session()
        a = session.query(Alumno).filter_by(id=aid).first()
        session.close()

        ctk.CTkLabel(self, text="Nombre:").pack(padx=24, anchor="w", pady=(20, 0))
        self._nombre = ctk.CTkEntry(self, width=330)
        self._nombre.insert(0, a.nombre)
        self._nombre.pack(padx=24)

        ctk.CTkLabel(self, text="Grupo:").pack(padx=24, anchor="w", pady=(12, 0))
        labels = [f"{g.grado}° {g.nombre}" for g in grupos]
        self._grupo_var = ctk.StringVar()
        self._grupo_menu = ctk.CTkOptionMenu(self, variable=self._grupo_var, values=labels, width=330)
        for g in grupos:
            if g.id == a.grupo_id:
                self._grupo_var.set(f"{g.grado}° {g.nombre}")
                break
        self._grupo_menu.pack(padx=24)

        ctk.CTkLabel(self, text="RFID (opcional):").pack(padx=24, anchor="w", pady=(12, 0))
        self._rfid = ctk.CTkEntry(self, width=330)
        self._rfid.insert(0, a.rfid_uid or "")
        self._rfid.pack(padx=24)

        ctk.CTkButton(self, text="Guardar", width=330, command=self._guardar).pack(padx=24, pady=20)

    def _guardar(self):
        session = get_session()
        a = session.query(Alumno).filter_by(id=self._aid).first()
        a.nombre = self._nombre.get().strip()
        a.rfid_uid = self._rfid.get().strip() or None
        sel = self._grupo_var.get()
        for g in self._grupos:
            if f"{g.grado}° {g.nombre}" == sel:
                a.grupo_id = g.id
                break
        session.commit()
        session.close()
        self._on_save()
        self.destroy()
