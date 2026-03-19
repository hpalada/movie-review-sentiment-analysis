# =============================================================================
#  FormCambioPass.py  –  Ventana para cambiar la contraseña
# =============================================================================
#
#  Responsabilidades:
#    · Mostrar el formulario de cambio de contraseña (nueva ventana)
#    · Recoger email, nueva contraseña y confirmación
#    · Delegar la lógica de cambio a ClaseLogin
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


class FormCambioPass:
    """
    Ventana modal para cambiar la contraseña de un usuario existente.
    Se abre desde FormLogin al hacer clic en '¿Olvidaste tu contraseña?'.
    """

    W, H = 460, 560

    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Cambiar Contraseña")
        self.win.resizable(False, False)
        self.win.configure(bg=BG)
        self.win.grab_set()
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
        canvas.create_oval(-80, -80, 210, 210, fill="#2a0a1a", outline="")
        canvas.create_oval(290, 370, 540, 620, fill="#1a0a2a", outline="")

        # Panel central
        panel = tk.Frame(canvas, bg=PANEL, padx=40, pady=36)
        canvas.create_window(230, 280, window=panel, width=380)

        # Encabezado
        _mk_label(panel, "⟳  Cambiar Clave",
                  font=FONT_TITLE, fg=ACCENT2).pack(pady=(0, 4))
        _mk_label(panel, "Ingresa tu correo y tu nueva contraseña",
                  font=FONT_SUB, fg=MUTED).pack(pady=(0, 22))

        # Correo registrado
        _mk_label(panel, "Correo electrónico registrado").pack(anchor="w")
        self.e_email = _mk_entry(panel)
        self.e_email.pack(fill="x", ipady=8, pady=(4, 14))

        # Nueva contraseña
        _mk_label(panel, "Nueva contraseña").pack(anchor="w")
        self.e_nueva = _mk_entry(panel, show="●")
        self.e_nueva.pack(fill="x", ipady=8, pady=(4, 14))

        # Confirmar nueva contraseña
        _mk_label(panel, "Confirmar nueva contraseña").pack(anchor="w")
        self.e_confirm = _mk_entry(panel, show="●")
        self.e_confirm.pack(fill="x", ipady=8, pady=(4, 26))

        # Botón actualizar
        _mk_button(panel, "ACTUALIZAR CONTRASEÑA →",
                   self._cambiar, color=ACCENT2, fg="white").pack(fill="x")

        # Mensaje de estado
        self.lbl_status = tk.Label(panel, text="", fg=ERROR, bg=PANEL,
                                   font=FONT_LABEL, wraplength=300)
        self.lbl_status.pack(pady=(12, 0))

    # ── Lógica de cambio de contraseña ───────────────────────────────────────
    def _cambiar(self):
        email   = self.e_email.get()
        nueva   = self.e_nueva.get()
        confirm = self.e_confirm.get()

        # Validación rápida de campos vacíos
        if not all([email.strip(), nueva, confirm]):
            self.lbl_status.config(
                text="⚠  Completa todos los campos.", fg=ERROR)
            return

        # Delegar a ClaseLogin
        ok, error, aviso = ClaseLogin.cambiar_password(email, nueva, confirm)

        if not ok:
            self.lbl_status.config(text=f"✗  {error}", fg=ERROR)
            return

        # Éxito
        self.lbl_status.config(
            text="✓  Contraseña actualizada · Correo enviado 📧", fg=SUCCESS)

        info = "Tu contraseña fue actualizada correctamente."
        if aviso:
            info += f"\n\n⚠ {aviso}"

        messagebox.showinfo("¡Contraseña actualizada!", info)
        self.win.destroy()