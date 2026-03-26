from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt

from ClaseLogin import ClaseLogin


class FormCambioPass(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambiar Contraseña")
        self.setFixedSize(360, 260)
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

        lbl_titulo = QLabel("Cambiar Contraseña")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_titulo)

        layout.addWidget(QLabel("Correo electrónico registrado:"))
        self.e_email = QLineEdit()
        self.e_email.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.e_email)

        layout.addWidget(QLabel("Nueva contraseña:"))
        self.e_nueva = QLineEdit()
        self.e_nueva.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_nueva.setPlaceholderText("Nueva contraseña")
        layout.addWidget(self.e_nueva)

        layout.addWidget(QLabel("Confirmar nueva contraseña:"))
        self.e_confirm = QLineEdit()
        self.e_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_confirm.setPlaceholderText("Confirmar contraseña")
        layout.addWidget(self.e_confirm)

        btn_actualizar = QPushButton("Actualizar contraseña")
        btn_actualizar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_actualizar.clicked.connect(self._cambiar)
        layout.addWidget(btn_actualizar)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        layout.addWidget(self.lbl_status)

    def _cambiar(self):
        email   = self.e_email.text().strip()
        nueva   = self.e_nueva.text()
        confirm = self.e_confirm.text()

        if not all([email, nueva, confirm]):
            self.lbl_status.setText("Completa todos los campos.")
            return

        ok, error, aviso = ClaseLogin.cambiar_password(email, nueva, confirm)

        if not ok:
            self.lbl_status.setText(error)
            return

        self.lbl_status.setText("Contraseña actualizada correctamente.")

        info = "Tu contraseña fue actualizada correctamente."
        if aviso:
            info += f"\n\n{aviso}"

        QMessageBox.information(self, "Contraseña actualizada", info)
        self.close()