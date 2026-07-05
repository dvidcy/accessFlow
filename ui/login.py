import customtkinter as ctk
from services.auth import login


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master, fg_color="transparent")
        self._on_login = on_login
        self._build()

    def _build(self):
        # Contenedor centrado
        card = ctk.CTkFrame(self, width=400, height=420)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="AccessFlow", font=("Arial", 28, "bold")).pack(pady=(40, 4))
        ctk.CTkLabel(card, text="Sistema de Asistencia Escolar",
                     font=("Arial", 13), text_color="gray").pack(pady=(0, 30))

        ctk.CTkLabel(card, text="Correo electrónico", anchor="w").pack(padx=40, fill="x")
        self._email = ctk.CTkEntry(card, width=320, placeholder_text="admin@accessflow.com")
        self._email.pack(padx=40, pady=(4, 16))

        ctk.CTkLabel(card, text="Contraseña", anchor="w").pack(padx=40, fill="x")
        self._password = ctk.CTkEntry(card, width=320, placeholder_text="••••••••", show="•")
        self._password.pack(padx=40, pady=(4, 8))

        self._error_lbl = ctk.CTkLabel(card, text="", text_color="#e74c3c", font=("Arial", 12))
        self._error_lbl.pack()

        ctk.CTkButton(card, text="Iniciar sesión", width=320,
                      command=self._intentar_login).pack(padx=40, pady=(12, 0))

        self._email.bind("<Return>", lambda e: self._intentar_login())
        self._password.bind("<Return>", lambda e: self._intentar_login())

    def _intentar_login(self):
        email = self._email.get().strip()
        password = self._password.get()
        if not email or not password:
            self._error_lbl.configure(text="Completa todos los campos.")
            return
        admin = login(email, password)
        if admin:
            self._on_login(admin)
        else:
            self._error_lbl.configure(text="Credenciales incorrectas.")
