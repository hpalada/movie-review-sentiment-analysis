from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt

from ClaseLogin import ClaseLogin

CLAVE_ADMIN = "Juanito123"


class FormCrearUsuario(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Cuenta")
        self.setFixedSize(360, 320)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self._centrar()
        self._construir()

    def _centrar(self):
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width()  - self.width())  // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _construir(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        lbl_titulo = QLabel("Crear Cuenta")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        layout.addWidget(QLabel("Nombre de usuario:"))
        self.e_nombre = QLineEdit()
        self.e_nombre.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.e_nombre)

        layout.addWidget(QLabel("Correo electrónico:"))
        self.e_email = QLineEdit()
        self.e_email.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.e_email)

        layout.addWidget(QLabel("Contraseña:"))
        self.e_pass = QLineEdit()
        self.e_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_pass.setPlaceholderText("Contraseña")
        layout.addWidget(self.e_pass)

        layout.addWidget(QLabel("Confirmar contraseña:"))
        self.e_confirm = QLineEdit()
        self.e_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_confirm.setPlaceholderText("Confirmar contraseña")
        layout.addWidget(self.e_confirm)

        btn_registrar = QPushButton("Registrarme")
        btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_registrar.clicked.connect(self._registrar)
        layout.addWidget(btn_registrar)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

    def _registrar(self):
        nombre = self.e_nombre.text()
        email  = self.e_email.text()
        campo1 = self.e_pass.text()
        campo2 = self.e_confirm.text()

        if not all([nombre.strip(), email.strip(), campo1, campo2]):
            self.lbl_status.setText("Completa todos los campos.")
            return

        if campo1 == CLAVE_ADMIN:
            rol      = "admin"
            password = campo2
            confirm  = campo2
        else:
            rol      = "lector"
            password = campo1
            confirm  = campo2

        ok, error, aviso = ClaseLogin.registrar(
            nombre, email, password, confirm, rol=rol)

        if not ok:
            self.lbl_status.setText(error)
            return

        rol_lbl = "Administrador" if rol == "admin" else "Lector"
        self.lbl_status.setText(f"Cuenta creada · {rol_lbl}")

        info = (f"¡Bienvenido, {nombre.strip()}!\n"
                f"Rol: {rol_lbl}\n"
                f"Ya puedes iniciar sesión.")
        if aviso:
            info += f"\n\n{aviso}"

        QMessageBox.information(self, "Registro exitoso", info)
        self.close()