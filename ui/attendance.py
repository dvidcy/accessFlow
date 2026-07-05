import customtkinter as ctk
from db.database import get_session
from db.models import Admin, Alumno
from services.attendance import registrar_asistencia, get_asistencias_hoy
from services.email_service import enviar_notificacion_entrada, enviar_notificacion_salida


class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._build()
        self._cargar_tabla()

    def _build(self):
        ctk.CTkLabel(self, text="Registro de Asistencia",
                     font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

        # Panel de registro
        panel = ctk.CTkFrame(self)
        panel.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(panel, text="ID o UID RFID del alumno:").pack(side="left", padx=(16, 8), pady=12)
        self._id_entry = ctk.CTkEntry(panel, width=200, placeholder_text="Ej: 3 o UID de tarjeta")
        self._id_entry.pack(side="left", pady=12)
        self._id_entry.bind("<Return>", lambda e: self._registrar())

        ctk.CTkButton(panel, text="Registrar", width=120,
                      command=self._registrar).pack(side="left", padx=12, pady=12)

        self._estado_lbl = ctk.CTkLabel(panel, text="", font=("Arial", 13, "bold"))
        self._estado_lbl.pack(side="left", padx=8)

        # Tabla
        cols = ("Alumno", "Grupo", "Entrada", "Salida")
        self._tabla = ctk.CTkScrollableFrame(self)
        self._tabla.pack(fill="both", expand=True)

        header = ctk.CTkFrame(self._tabla, fg_color=("gray85", "gray20"))
        header.pack(fill="x", pady=(0, 2))
        for col in cols:
            ctk.CTkLabel(header, text=col, font=("Arial", 12, "bold"),
                         width=180, anchor="w").pack(side="left", padx=8, pady=6)

    def _registrar(self):
        valor = self._id_entry.get().strip()
        if not valor:
            return

        # Busca por RFID primero, luego por ID numérico
        session = get_session()
        alumno = session.query(Alumno).filter_by(rfid_uid=valor).first()
        if not alumno and valor.isdigit():
            alumno = session.query(Alumno).filter_by(id=int(valor)).first()
        session.close()

        if not alumno:
            self._estado_lbl.configure(text="Alumno no encontrado.", text_color="#e74c3c")
            self._id_entry.delete(0, "end")
            return

        tipo, registro = registrar_asistencia(alumno.id)

        if tipo == "completo":
            self._estado_lbl.configure(
                text=f"{alumno.nombre}: entrada y salida ya registradas hoy.",
                text_color="gray")
            self._id_entry.delete(0, "end")
            return

        hora = (registro.fecha_entrada if tipo == "entrada" else registro.fecha_salida).strftime("%H:%M:%S")
        color = "#2ecc71" if tipo == "entrada" else "#e67e22"
        self._estado_lbl.configure(
            text=f"{'Entrada' if tipo == 'entrada' else 'Salida'}: {alumno.nombre} — {hora}",
            text_color=color)

        # Notificar a todos los tutores del alumno
        session = get_session()
        alumno_db = session.query(Alumno).filter_by(id=alumno.id).first()
        for tutor in alumno_db.tutores:
            if tipo == "entrada":
                enviar_notificacion_entrada(tutor.email, alumno.nombre, hora)
            else:
                enviar_notificacion_salida(tutor.email, alumno.nombre, hora)
        session.close()

        self._id_entry.delete(0, "end")
        self._cargar_tabla()

    def _cargar_tabla(self):
        for widget in self._tabla.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self._tabla.winfo_children()[0]:
                widget.destroy()

        for fila in get_asistencias_hoy():
            row = ctk.CTkFrame(self._tabla, fg_color="transparent")
            row.pack(fill="x", pady=1)
            for valor in (fila["alumno"], fila["grupo"], fila["fecha_entrada"], fila["fecha_salida"]):
                ctk.CTkLabel(row, text=valor, width=180, anchor="w").pack(side="left", padx=8, pady=4)
