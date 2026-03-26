from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer
import sys

from ClaseLogin          import ClaseLogin
from FormRegistroUsuario import FormCrearUsuario
from FormCambiarContra   import FormCambioPass
from catalogoPrincipal   import CatalogoWindow


class FormLogin(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.setFixedSize(340, 280)
        self._centrar()
        self._construir()

    def _centrar(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width()  - self.width())  // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _construir(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # Título
        lbl_titulo = QLabel("Iniciar Sesión")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        # Campo usuario o correo
        lbl_credencial = QLabel("Usuario o correo electrónico:")
        layout.addWidget(lbl_credencial)

        self.e_credencial = QLineEdit()
        self.e_credencial.setPlaceholderText("Usuario o correo")
        layout.addWidget(self.e_credencial)

        # Campo contraseña
        lbl_pass = QLabel("Contraseña:")
        layout.addWidget(lbl_pass)

        self.e_pass = QLineEdit()
        self.e_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_pass.setPlaceholderText("Contraseña")
        layout.addWidget(self.e_pass)

        # Enlace "olvidé contraseña"
        btn_forgot = QPushButton("¿Olvidaste tu contraseña?")
        btn_forgot.setFlat(True)
        btn_forgot.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_forgot.clicked.connect(self._abrir_cambio_pass)
        layout.addWidget(btn_forgot, alignment=Qt.AlignmentFlag.AlignRight)

        # Botón Ingresar
        btn_login = QPushButton("Ingresar")
        btn_login.clicked.connect(self._login)
        btn_login.setDefault(True)
        layout.addWidget(btn_login)

        # Botón Crear cuenta
        btn_registro = QPushButton("Crear cuenta")
        btn_registro.clicked.connect(self._abrir_registro)
        layout.addWidget(btn_registro)

        # Etiqueta de estado
        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

        # Enter dispara login
        self.e_pass.returnPressed.connect(self._login)

    # ── Acciones ─────────────────────────────────────────────────────────

    def _abrir_cambio_pass(self):
        self._dlg_pass = FormCambioPass(self)
        self._dlg_pass.show()

    def _abrir_registro(self):
        self._dlg_reg = FormCrearUsuario(self)
        self._dlg_reg.show()

    def _login(self):
        credencial = self.e_credencial.text().strip()
        password   = self.e_pass.text()

        ok, error, usuario, aviso = ClaseLogin.autenticar(credencial, password)

        if not ok:
            self.lbl_status.setText(f"✗  {error}")
            return

        nombre = usuario["nombre_usuario"]
        self.lbl_status.setText(f"✓  ¡Bienvenido, {nombre}!")

        if aviso:
            QMessageBox.warning(self, "Aviso", aviso)

        rol = usuario.get("rol", "lector")
        QTimer.singleShot(600, lambda: self._abrir_catalogo(usuario, rol))

    def _abrir_catalogo(self, usuario: dict, rol: str):
        self.close()
        self._catalogo = CatalogoWindow(usuario=usuario, rol=rol)
        self._catalogo.show()


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    ventana = FormLogin()
    ventana.show()
    sys.exit(app.exec())