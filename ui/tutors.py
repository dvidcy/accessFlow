import customtkinter as ctk
from db.database import get_session
from db.models import Tutor, Alumno, Admin, alumno_tutor


def _get_tutores():
    session = get_session()
    try:
        return session.query(Tutor).order_by(Tutor.nombre).all()
    finally:
        session.close()

def _get_alumnos():
    session = get_session()
    try:
        return session.query(Alumno).order_by(Alumno.nombre).all()
    finally:
        session.close()


class TutorsFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._alumnos: list[Alumno] = []
        self._build()
        self._cargar_tabla()

    def _build(self):
        ctk.CTkLabel(self, text="Tutores", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 8))

        # Fila 1: nombre, email, teléfono
        ctk.CTkLabel(form, text="Nombre:").grid(row=0, column=0, padx=12, pady=(12,4), sticky="w")
        self._nombre = ctk.CTkEntry(form, width=160, placeholder_text="Nombre completo")
        self._nombre.grid(row=0, column=1, padx=8, pady=(12,4))

        ctk.CTkLabel(form, text="Email:").grid(row=0, column=2, padx=12, pady=(12,4), sticky="w")
        self._email = ctk.CTkEntry(form, width=180, placeholder_text="correo@ejemplo.com")
        self._email.grid(row=0, column=3, padx=8, pady=(12,4))

        ctk.CTkLabel(form, text="Teléfono:").grid(row=0, column=4, padx=12, pady=(12,4), sticky="w")
        self._tel = ctk.CTkEntry(form, width=120, placeholder_text="Opcional")
        self._tel.grid(row=0, column=5, padx=8, pady=(12,4))

        # Fila 2: alumno vinculado, parentesco, botón
        ctk.CTkLabel(form, text="Alumno:").grid(row=1, column=0, padx=12, pady=(4,12), sticky="w")
        self._alumnos = _get_alumnos()
        alumnos_labels = [a.nombre for a in self._alumnos] or ["—"]
        self._alumno_var = ctk.StringVar(value=alumnos_labels[0])
        ctk.CTkOptionMenu(form, variable=self._alumno_var, values=alumnos_labels, width=160).grid(
            row=1, column=1, padx=8, pady=(4,12))

        ctk.CTkLabel(form, text="Parentesco:").grid(row=1, column=2, padx=12, pady=(4,12), sticky="w")
        self._parentesco = ctk.CTkEntry(form, width=120, placeholder_text="madre / padre...")
        self._parentesco.grid(row=1, column=3, padx=8, pady=(4,12))

        ctk.CTkButton(form, text="Agregar tutor", command=self._agregar).grid(
            row=1, column=4, columnspan=2, padx=12, pady=(4,12))

        self._msg = ctk.CTkLabel(self, text="", text_color="#2ecc71")
        self._msg.pack(anchor="w")

        # Tabla
        header = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        header.pack(fill="x")
        for col, w in [("ID", 40), ("Nombre", 180), ("Email", 200), ("Teléfono", 120), ("Alumnos", 200), ("Acciones", 160)]:
            ctk.CTkLabel(header, text=col, font=("Arial", 12, "bold"),
                         width=w, anchor="w").pack(side="left", padx=8, pady=6)

        self._tabla = ctk.CTkScrollableFrame(self)
        self._tabla.pack(fill="both", expand=True, pady=(2, 0))

    def _cargar_tabla(self):
        for w in self._tabla.winfo_children():
            w.destroy()
        for t in _get_tutores():
            self._fila(t)

    def _fila(self, t: Tutor):
        session = get_session()
        tutor = session.query(Tutor).filter_by(id=t.id).first()
        alumnos_str = ", ".join(a.nombre for a in tutor.alumnos) or "—"
        session.close()

        row = ctk.CTkFrame(self._tabla, fg_color="transparent")
        row.pack(fill="x", pady=1)
        for val, w in [(t.id, 40), (t.nombre, 180), (t.email, 200), (t.telefono or "—", 120), (alumnos_str, 200)]:
            ctk.CTkLabel(row, text=str(val), width=w, anchor="w").pack(side="left", padx=8, pady=4)
        ctk.CTkButton(row, text="Editar", width=70,
                      command=lambda tid=t.id: self._editar(tid)).pack(side="left", padx=4)
        ctk.CTkButton(row, text="Eliminar", width=70, fg_color="#c0392b", hover_color="#a93226",
                      command=lambda tid=t.id: self._eliminar(tid)).pack(side="left", padx=4)

    def _agregar(self):
        nombre = self._nombre.get().strip()
        email = self._email.get().strip()
        tel = self._tel.get().strip() or None
        parentesco = self._parentesco.get().strip() or None
        seleccion = self._alumno_var.get()
        alumno_id = None
        for a in self._alumnos:
            if a.nombre == seleccion:
                alumno_id = a.id
                break
        if not nombre or not email:
            self._msg.configure(text="Nombre y email son requeridos.", text_color="#e74c3c")
            return
        session = get_session()
        tutor = Tutor(nombre=nombre, email=email, telefono=tel)
        session.add(tutor)
        session.flush()
        if alumno_id:
            session.execute(alumno_tutor.insert().values(
                alumno_id=alumno_id, tutor_id=tutor.id, parentesco=parentesco))
        session.commit()
        session.close()
        self._nombre.delete(0, "end")
        self._email.delete(0, "end")
        self._tel.delete(0, "end")
        self._parentesco.delete(0, "end")
        self._msg.configure(text="Tutor agregado.", text_color="#2ecc71")
        self._cargar_tabla()

    def _eliminar(self, tid: int):
        session = get_session()
        t = session.query(Tutor).filter_by(id=tid).first()
        if t:
            session.delete(t)
            session.commit()
        session.close()
        self._cargar_tabla()

    def _editar(self, tid: int):
        EditTutorDialog(self, tid, on_save=self._cargar_tabla)


class EditTutorDialog(ctk.CTkToplevel):
    def __init__(self, master, tid: int, on_save):
        super().__init__(master)
        self.title("Editar tutor")
        self.geometry("380x280")
        self.resizable(False, False)
        self.grab_set()
        self._tid = tid
        self._on_save = on_save

        session = get_session()
        t = session.query(Tutor).filter_by(id=tid).first()
        session.close()

        for label, attr, ph in [
            ("Nombre:", t.nombre, ""),
            ("Email:", t.email, ""),
            ("Teléfono:", t.telefono or "", "Opcional"),
        ]:
            ctk.CTkLabel(self, text=label).pack(padx=24, anchor="w", pady=(12, 0))
            entry = ctk.CTkEntry(self, width=330, placeholder_text=ph)
            entry.insert(0, attr)
            entry.pack(padx=24)
            setattr(self, f"_{label[:-1].lower().replace('é','e')}", entry)

        ctk.CTkButton(self, text="Guardar", width=330, command=self._guardar).pack(padx=24, pady=20)

    def _guardar(self):
        session = get_session()
        t = session.query(Tutor).filter_by(id=self._tid).first()
        t.nombre   = self._nombre.get().strip()
        t.email    = self._email.get().strip()
        t.telefono = self._telefono.get().strip() or None
        session.commit()
        session.close()
        self._on_save()
        self.destroy()
