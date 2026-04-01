import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QGraphicsDropShadowEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QCursor

# --- IMPORTACIONES DE TU PROYECTO ---
try:
    from ClaseLogin import ClaseLogin
except ImportError:
    pass

CLAVE_ADMIN = "Juanito123"

class FormCrearUsuario(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # parent es el FormLogin. Lo guardamos para mostrarlo al cerrar.
        self._login_referencia = parent 
        
        # Configuración de ventana moderna (Sin bordes de Windows)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(450, 620)
        
        self._centrar_en_pantalla()
        self._aplicar_estilos()
        self._construir()
        self.old_pos = None

    def _centrar_en_pantalla(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            #MainFrame {
                background-color: #000000;
                border-radius: 30px;
            }
            #Card {
                background-color: #ffffff;
                border-radius: 30px;
            }
            QLabel#Titulo {
                font-size: 24px;
                font-weight: 800;
                color: #0f172a;
            }
            QLabel#Subtitulo {
                font-size: 13px;
                color: #64748b;
            }
            QLineEdit {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
                color: #1e293b;
            }
            QLineEdit:focus { border: 2px solid #000000; }
            
            QPushButton#BtnRegistrar {
                background-color: #000000;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                margin-top: 10px;
            }
            QPushButton#BtnRegistrar:hover { background-color: #333333; }
            
            QPushButton#BtnCerrar {
                border: none;
                color: #94a3b8;
                font-size: 18px;
                background: transparent;
                font-weight: bold;
            }
            QPushButton#BtnCerrar:hover { color: #ff4444; }

            #LblError {
                color: #ef4444;
                font-size: 12px;
                font-weight: 600;
            }
            #LblExito {
                color: #10b981;
                font-size: 12px;
                font-weight: 600;
            }
        """)

    def _construir(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedSize(450, 620)

        main_layout = QVBoxLayout(self.main_frame)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.card = QFrame()
        self.card.setObjectName("Card")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(35, 20, 35, 30)
        card_layout.setSpacing(15)

        # Botón Cerrar (X)
        btn_x = QPushButton("✕")
        btn_x.setObjectName("BtnCerrar")
        btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_x.clicked.connect(self.close)
        card_layout.addWidget(btn_x, alignment=Qt.AlignmentFlag.AlignRight)

        # Cabecera
        lbl_t = QLabel("Crear Cuenta")
        lbl_t.setObjectName("Titulo")
        lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_st = QLabel("Únete a la experiencia Movie AI")
        lbl_st.setObjectName("Subtitulo")
        lbl_st.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(lbl_t)
        card_layout.addWidget(lbl_st)
        card_layout.addSpacing(10)

        # Campos
        self.e_nombre = QLineEdit()
        self.e_nombre.setPlaceholderText("Nombre de usuario")
        self.e_nombre.textChanged.connect(self._limpiar_status)
        card_layout.addWidget(self.e_nombre)

        self.e_email = QLineEdit()
        self.e_email.setPlaceholderText("Correo electrónico")
        self.e_email.textChanged.connect(self._limpiar_status)
        card_layout.addWidget(self.e_email)

        self.e_pass = QLineEdit()
        self.e_pass.setPlaceholderText("Contraseña")
        self.e_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_pass.textChanged.connect(self._limpiar_status)
        card_layout.addWidget(self.e_pass)

        self.e_confirm = QLineEdit()
        self.e_confirm.setPlaceholderText("Confirmar contraseña")
        self.e_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.e_confirm.textChanged.connect(self._limpiar_status)
        card_layout.addWidget(self.e_confirm)

        # Botón Registro
        btn_registrar = QPushButton("Registrarme ahora")
        btn_registrar.setObjectName("BtnRegistrar")
        btn_registrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_registrar.clicked.connect(self._registrar)
        card_layout.addWidget(btn_registrar)

        # Label de estado
        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("LblError")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setWordWrap(True)
        card_layout.addWidget(self.lbl_status)

        main_layout.addWidget(self.card)

    def _limpiar_status(self):
        self.lbl_status.setText("")
        self.lbl_status.setObjectName("LblError")

    def _registrar(self):
        nombre = self.e_nombre.text().strip()
        email  = self.e_email.text().strip()
        campo1 = self.e_pass.text()
        campo2 = self.e_confirm.text()

        if not all([nombre, email, campo1, campo2]):
            self.lbl_status.setText("Completa todos los campos")
            return

        # Lógica de roles según tu código original
        if campo1 == CLAVE_ADMIN:
            rol, password, confirm = "admin", campo2, campo2
        else:
            rol, password, confirm = "lector", campo1, campo2

        try:
            ok, error, aviso = ClaseLogin.registrar(nombre, email, password, confirm, rol=rol)

            if not ok:
                self.lbl_status.setObjectName("LblError")
                self.lbl_status.setText(str(error))
                self.lbl_status.setStyleSheet("color: #ef4444;") # Forzar color rojo
                return

            # ÉXITO
            self.lbl_status.setStyleSheet("color: #10b981;") # Forzar color verde
            self.lbl_status.setText("¡Cuenta creada! Volviendo al Login...")
            
            # Bloquear botón para evitar doble clic
            self.findChild(QPushButton, "BtnRegistrar").setEnabled(False)
            
            # Esperar 1.5 seg y cerrar (esto disparará el closeEvent)
            QTimer.singleShot(1500, self.close)

        except Exception as e:
            self.lbl_status.setText(f"Error: {e}")

    # --- LÓGICA DE NAVEGACIÓN ---
    def closeEvent(self, event):
        """Al cerrar esta ventana, el Login reaparece"""
        if self._login_referencia:
            self._login_referencia.show()
        event.accept()

    # Mover ventana sin bordes
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.old_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event): self.old_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ejemplo de uso solo (sin login parent)
    win = FormCrearUsuario()
    win.show()
    sys.exit(app.exec())