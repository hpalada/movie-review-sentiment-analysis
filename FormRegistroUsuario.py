# =============================================================================
#  FormCrearUsuario.py  –  Ventana para registrar un nuevo usuario
# =============================================================================
#
#  Responsabilidades:
#    · Mostrar el formulario de registro (nueva ventana)
#    · Recoger nombre_usuario, email, password y confirmación
#    · Delegar la lógica de registro a ClaseLogin
#
#  NO tiene lógica de negocio, NO toca el JSON, NO envía correos.
# =============================================================================

import tkinter as tk
from tkinter    import messagebox
from ClaseLogin import ClaseLogin

# ── Paleta de colores ─────────────────────────────────────────────────────────
BG       = "#0d0d1a"
PANEL    = "#12122a"
ACCENT   = "#6c63ff"
ACCENT2  = "#ff6b9d"
TEXT     = "#e8e8f0"
MUTED    = "#6b6b8a"
ENTRY_BG = "#1c1c38"
BORDER   = "#2a2a50"
SUCCESS  = "#4ade80"
ERROR    = "#f87171"

FONT_TITLE = ("Georgia", 24, "bold")
FONT_SUB   = ("Georgia", 10, "italic")
FONT_LABEL = ("Helvetica", 10)
FONT_ENTRY = ("Helvetica", 11)
FONT_BTN   = ("Helvetica", 11, "bold")


def _mk_entry(parent, show=None):
    return tk.Entry(parent, show=show, bg=ENTRY_BG, fg=TEXT,
                    insertbackground=ACCENT, relief="flat", font=FONT_ENTRY,
                    bd=0, highlightthickness=1,
                    highlightcolor=ACCENT, highlightbackground=BORDER)

def _mk_button(parent, text, cmd, color=ACCENT, fg="white"):
    return tk.Button(parent, text=text, command=cmd, bg=color, fg=fg,
                     font=FONT_BTN, relief="flat", bd=0, padx=20, pady=10,
                     cursor="hand2", activebackground=ACCENT2,
                     activeforeground="white")

def _mk_label(parent, text, font=FONT_LABEL, fg=TEXT):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=PANEL)


class FormCrearUsuario:
    """
    Ventana modal para registrar un nuevo usuario.
    Se abre como Toplevel desde FormLogin.
    """

    W, H = 460, 660

    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Crear Cuenta")
        self.win.resizable(False, False)
        self.win.configure(bg=BG)
        self.win.grab_set()          # ventana modal
        self._centrar()
        self._construir()

    # ── Centrar ventana ───────────────────────────────────────────────────────
    def _centrar(self):
        self.win.update_idletasks()
        x = (self.win.winfo_screenwidth()  - self.W) // 2
        y = (self.win.winfo_screenheight() - self.H) // 2
        self.win.geometry(f"{self.W}x{self.H}+{x}+{y}")

    # ── Construir UI ──────────────────────────────────────────────────────────
    def _construir(self):
        canvas = tk.Canvas(self.win, width=self.W, height=self.H,
                           bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Esferas decorativas
        canvas.create_oval(-80, -80, 210, 210, fill="#1a2a0a", outline="")
        canvas.create_oval(290, 450, 540, 700, fill="#0a0a3a", outline="")

        # Panel central
        panel = tk.Frame(canvas, bg=PANEL, padx=40, pady=36)
        canvas.create_window(230, 330, window=panel, width=380)

        # Encabezado
        _mk_label(panel, "✦  Crear Cuenta",
                  font=FONT_TITLE, fg=SUCCESS).pack(pady=(0, 4))
        _mk_label(panel, "Regístrate con tu correo electrónico",
                  font=FONT_SUB, fg=MUTED).pack(pady=(0, 22))

        # Nombre de usuario
        _mk_label(panel, "Nombre de usuario").pack(anchor="w")
        self.e_nombre = _mk_entry(panel)
        self.e_nombre.pack(fill="x", ipady=8, pady=(4, 14))

        # Correo electrónico
        _mk_label(panel, "Correo electrónico").pack(anchor="w")
        self.e_email = _mk_entry(panel)
        self.e_email.pack(fill="x", ipady=8, pady=(4, 14))

        # Contraseña
        _mk_label(panel, "Contraseña").pack(anchor="w")
        self.e_pass = _mk_entry(panel, show="●")
        self.e_pass.pack(fill="x", ipady=8, pady=(4, 14))

        # Confirmar contraseña
        _mk_label(panel, "Confirmar contraseña").pack(anchor="w")
        self.e_confirm = _mk_entry(panel, show="●")
        self.e_confirm.pack(fill="x", ipady=8, pady=(4, 24))

        # Botón registrar
        _mk_button(panel, "REGISTRARME →",
                   self._registrar, color=SUCCESS, fg=BG).pack(fill="x")

        # Mensaje de estado
        self.lbl_status = tk.Label(panel, text="", fg=ERROR, bg=PANEL,
                                   font=FONT_LABEL, wraplength=300)
        self.lbl_status.pack(pady=(12, 0))

    # ── Lógica de registro ────────────────────────────────────────────────────
    def _registrar(self):
        nombre   = self.e_nombre.get()
        email    = self.e_email.get()
        password = self.e_pass.get()
        confirm  = self.e_confirm.get()

        # Validación rápida de campos vacíos
        if not all([nombre.strip(), email.strip(), password, confirm]):
            self.lbl_status.config(
                text="⚠  Completa todos los campos.", fg=ERROR)
            return

        # Delegar a ClaseLogin
        ok, error, aviso = ClaseLogin.registrar(nombre, email, password, confirm)

        if not ok:
            self.lbl_status.config(text=f"✗  {error}", fg=ERROR)
            return

        # Éxito
        self.lbl_status.config(
            text="✓  Cuenta creada · Correo de bienvenida enviado 📧", fg=SUCCESS)

        info = f"¡Bienvenido, {nombre.strip()}!\nYa puedes iniciar sesión."
        if aviso:
            info += f"\n\n⚠ {aviso}"

        messagebox.showinfo("¡Registro exitoso!", info)
        self.win.destroy()