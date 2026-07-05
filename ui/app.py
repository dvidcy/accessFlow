import customtkinter as ctk
from db.models import Admin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AccessFlow")
        self.geometry("1100x680")
        self.resizable(False, False)
        self.admin: Admin | None = None
        self._frame_actual = None
        self._mostrar_login()

    def _cambiar_frame(self, nuevo_frame):
        if self._frame_actual:
            self._frame_actual.destroy()
        self._frame_actual = nuevo_frame
        self._frame_actual.pack(fill="both", expand=True)

    def _mostrar_login(self):
        from ui.login import LoginFrame
        self._cambiar_frame(LoginFrame(self, on_login=self._on_login_exitoso))

    def _on_login_exitoso(self, admin: Admin):
        self.admin = admin
        self._mostrar_dashboard()

    def _mostrar_dashboard(self):
        from ui.dashboard import DashboardFrame
        self._cambiar_frame(DashboardFrame(self, admin=self.admin, on_logout=self._mostrar_login))


def run():
    app = App()
    app.mainloop()
