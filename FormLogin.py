import tkinter as tk
from tkinter              import messagebox
from ClaseLogin           import ClaseLogin
from FormRegistroUsuario  import FormCrearUsuario
from FormCambiarContra    import FormCambioPass

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

FONT_TITLE = ("Georgia", 26, "bold")
FONT_SUB   = ("Georgia", 11, "italic")
FONT_LABEL = ("Helvetica", 10)
FONT_ENTRY = ("Helvetica", 11)
FONT_BTN   = ("Helvetica", 11, "bold")
FONT_LINK  = ("Helvetica", 9, "underline")

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


class FormLogin:
    W, H = 440, 580

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Iniciar Sesión")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._centrar()
        self._construir()
        self.root.mainloop()

    def _centrar(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - self.W) // 2
        y = (self.root.winfo_screenheight() - self.H) // 2
        self.root.geometry(f"{self.W}x{self.H}+{x}+{y}")

    def _construir(self):
        canvas = tk.Canvas(self.root, width=self.W, height=self.H,
                           bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_oval(-80, -80, 200, 200, fill="#1a0a3a", outline="")
        canvas.create_oval(280, 390, 520, 630, fill="#0a1a3a", outline="")

        panel = tk.Frame(canvas, bg=PANEL, padx=40, pady=36)
        canvas.create_window(220, 290, window=panel, width=360)

        _mk_label(panel, "◈  Bienvenido", font=FONT_TITLE, fg=ACCENT).pack(pady=(0, 4))
        _mk_label(panel, "Ingresa tus credenciales para continuar",
                  font=FONT_SUB, fg=MUTED).pack(pady=(0, 24))

        _mk_label(panel, "Correo electrónico").pack(anchor="w")
        self.e_email = _mk_entry(panel)
        self.e_email.pack(fill="x", ipady=8, pady=(4, 14))

        _mk_label(panel, "Contraseña").pack(anchor="w")
        self.e_pass = _mk_entry(panel, show="●")
        self.e_pass.pack(fill="x", ipady=8, pady=(4, 6))

        lnk = tk.Label(panel, text="¿Olvidaste tu contraseña?",
                       font=FONT_LINK, fg=ACCENT2, bg=PANEL, cursor="hand2")
        lnk.pack(anchor="e", pady=(0, 20))
        lnk.bind("<Button-1>", lambda _: FormCambioPass(self.root))

        _mk_button(panel, "INGRESAR →", self._login).pack(fill="x", pady=(0, 14))

        sep = tk.Frame(panel, bg=PANEL)
        sep.pack(fill="x", pady=(0, 14))
        tk.Frame(sep, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, pady=6)
        tk.Label(sep, text="  o  ", fg=MUTED, bg=PANEL, font=FONT_LABEL).pack(side="left")
        tk.Frame(sep, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, pady=6)

        _mk_button(panel, "CREAR CUENTA",
                   lambda: FormCrearUsuario(self.root),
                   color=ENTRY_BG, fg=ACCENT).pack(fill="x")

        self.lbl_status = tk.Label(panel, text="", fg=ERROR, bg=PANEL,
                                   font=FONT_LABEL, wraplength=300)
        self.lbl_status.pack(pady=(14, 0))

    def _login(self):
        email    = self.e_email.get().strip()
        password = self.e_pass.get()

        ok, error, usuario, aviso = ClaseLogin.autenticar(email, password)

        if not ok:
            self.lbl_status.config(text=f"✗  {error}", fg=ERROR)
            return

        # FIX: usuario es dict, se accede con ["nombre_usuario"] no .nombre_usuario
        nombre = usuario["nombre_usuario"]
        self.lbl_status.config(
            text=f"✓  ¡Bienvenido, {nombre}! · Correo enviado 📧", fg=SUCCESS)

        info = f"¡Hola, {nombre}!\nHas iniciado sesión correctamente."
        if aviso:
            info += f"\n\n⚠ {aviso}"

        messagebox.showinfo("Sesión iniciada", info)
        self.e_email.delete(0, tk.END)
        self.e_pass.delete(0, tk.END)
        self.lbl_status.config(text="")

if __name__ == "__main__":
    FormLogin()