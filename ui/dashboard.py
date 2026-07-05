import customtkinter as ctk
from db.models import Admin


NAV_ITEMS = [
    ("Asistencia",  "ui.attendance",  "AttendanceFrame"),
    ("Alumnos",     "ui.students",    "StudentsFrame"),
    ("Grupos",      "ui.groups",      "GroupsFrame"),
    ("Tutores",     "ui.tutors",      "TutorsFrame"),
    ("Mensajes",    "ui.messaging",   "MessagingFrame"),
]


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, admin: Admin, on_logout):
        super().__init__(master, fg_color="transparent")
        self._admin = admin
        self._on_logout = on_logout
        self._content_frame = None
        self._nav_buttons: list[ctk.CTkButton] = []
        self._build()
        # Abrir asistencia por defecto
        self._navegar(0)

    def _build(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="AccessFlow",
                     font=("Arial", 20, "bold")).pack(pady=(24, 4))
        ctk.CTkLabel(sidebar, text=self._admin.nombre,
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 24))

        for i, (label, _, _) in enumerate(NAV_ITEMS):
            btn = ctk.CTkButton(
                sidebar, text=label, width=160,
                fg_color="transparent", anchor="w",
                command=lambda idx=i: self._navegar(idx),
            )
            btn.pack(padx=20, pady=4)
            self._nav_buttons.append(btn)

        ctk.CTkButton(sidebar, text="Cerrar sesión", width=160,
                      fg_color="#c0392b", hover_color="#a93226",
                      command=self._on_logout).pack(side="bottom", padx=20, pady=20)

        # Área de contenido
        self._content_area = ctk.CTkFrame(self, fg_color="transparent")
        self._content_area.pack(side="left", fill="both", expand=True, padx=16, pady=16)

    def _navegar(self, idx: int):
        # Resaltar botón activo
        for i, btn in enumerate(self._nav_buttons):
            btn.configure(fg_color=("gray75", "gray25") if i == idx else "transparent")

        if self._content_frame:
            self._content_frame.destroy()

        _, modulo, clase = NAV_ITEMS[idx]
        import importlib
        mod = importlib.import_module(modulo)
        frame_cls = getattr(mod, clase)
        self._content_frame = frame_cls(self._content_area, admin=self._admin)
        self._content_frame.pack(fill="both", expand=True)
