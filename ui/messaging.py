import customtkinter as ctk
from db.models import Admin
from services.messaging import (
    get_tutores, get_grupos,
    enviar_mensaje_individual, enviar_mensaje_grupal,
)


class MessagingFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._tutores = []
        self._grupos = []
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Mensajes", font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

        # Selector de tipo
        tipo_frame = ctk.CTkFrame(self, fg_color="transparent")
        tipo_frame.pack(anchor="w", pady=(0, 12))
        ctk.CTkLabel(tipo_frame, text="Tipo de mensaje:").pack(side="left", padx=(0, 12))
        self._tipo = ctk.StringVar(value="individual")
        ctk.CTkRadioButton(tipo_frame, text="Individual", variable=self._tipo,
                           value="individual", command=self._on_tipo_change).pack(side="left", padx=8)
        ctk.CTkRadioButton(tipo_frame, text="Grupal", variable=self._tipo,
                           value="grupal", command=self._on_tipo_change).pack(side="left", padx=8)

        # Destinatario dinámico
        self._dest_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._dest_frame.pack(fill="x", pady=(0, 12))
        self._build_dest_individual()

        # Formulario mensaje
        form = ctk.CTkFrame(self)
        form.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(form, text="Asunto:").pack(padx=16, anchor="w", pady=(12, 0))
        self._asunto = ctk.CTkEntry(form, width=600, placeholder_text="Asunto del mensaje")
        self._asunto.pack(padx=16, pady=(4, 12))

        ctk.CTkLabel(form, text="Mensaje:").pack(padx=16, anchor="w")
        self._cuerpo = ctk.CTkTextbox(form, width=600, height=140)
        self._cuerpo.pack(padx=16, pady=(4, 12))

        ctk.CTkButton(form, text="Enviar mensaje", width=200,
                      command=self._enviar).pack(padx=16, pady=(0, 12), anchor="w")

        self._resultado = ctk.CTkLabel(self, text="", font=("Arial", 13))
        self._resultado.pack(anchor="w")

    def _build_dest_individual(self):
        for w in self._dest_frame.winfo_children():
            w.destroy()
        self._tutores = get_tutores()
        labels = [f"{t.nombre} ({t.email})" for t in self._tutores] or ["Sin tutores registrados"]
        ctk.CTkLabel(self._dest_frame, text="Tutor destinatario:").pack(side="left", padx=(0, 12))
        self._dest_var = ctk.StringVar(value=labels[0] if labels else "")
        ctk.CTkOptionMenu(self._dest_frame, variable=self._dest_var,
                          values=labels, width=380).pack(side="left")

    def _build_dest_grupal(self):
        for w in self._dest_frame.winfo_children():
            w.destroy()
        self._grupos = get_grupos()
        labels = [f"{g.grado}° {g.nombre} — {g.turno}" for g in self._grupos] or ["Sin grupos registrados"]
        ctk.CTkLabel(self._dest_frame, text="Grupo destinatario:").pack(side="left", padx=(0, 12))
        self._dest_var = ctk.StringVar(value=labels[0] if labels else "")
        ctk.CTkOptionMenu(self._dest_frame, variable=self._dest_var,
                          values=labels, width=380).pack(side="left")

    def _on_tipo_change(self):
        if self._tipo.get() == "individual":
            self._build_dest_individual()
        else:
            self._build_dest_grupal()

    def _enviar(self):
        asunto = self._asunto.get().strip()
        cuerpo = self._cuerpo.get("1.0", "end").strip()
        if not asunto or not cuerpo:
            self._resultado.configure(text="Asunto y mensaje son requeridos.", text_color="#e74c3c")
            return

        if self._tipo.get() == "individual":
            seleccion = self._dest_var.get()
            tutor_id = None
            for t in self._tutores:
                if f"{t.nombre} ({t.email})" == seleccion:
                    tutor_id = t.id
                    break
            if not tutor_id:
                self._resultado.configure(text="Selecciona un tutor.", text_color="#e74c3c")
                return
            res = enviar_mensaje_individual(tutor_id, asunto, cuerpo, self._admin.id)
        else:
            seleccion = self._dest_var.get()
            grupo_id = None
            for g in self._grupos:
                if f"{g.grado}° {g.nombre} — {g.turno}" == seleccion:
                    grupo_id = g.id
                    break
            if not grupo_id:
                self._resultado.configure(text="Selecciona un grupo.", text_color="#e74c3c")
                return
            res = enviar_mensaje_grupal(grupo_id, asunto, cuerpo, self._admin.id)

        if res.get("ok"):
            enviados = res.get("enviados", res.get("destinatarios", 1))
            self._resultado.configure(
                text=f"Mensaje enviado a {enviados} destinatario(s).", text_color="#2ecc71")
            self._asunto.delete(0, "end")
            self._cuerpo.delete("1.0", "end")
        else:
            self._resultado.configure(text=f"Error: {res.get('error')}", text_color="#e74c3c")
