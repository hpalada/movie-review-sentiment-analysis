import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QApplication, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor

try:
    from ClaseLogin import ClaseLogin
    from FormRegistroUsuario import FormCrearUsuario
    from FormCambiarContra import FormCambioPass
    from catalogoPrincipal import CatalogoWindow
except ImportError:
    pass


class FormLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(1000, 650) 
        self._centrar_en_pantalla()
        self._aplicar_estilos()
        self._construir()
        self.old_pos = None

    def _centrar_en_pantalla(self):
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp); self.move(qr.topLeft())

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            #MainContainer { background-color: #000000; border-radius: 30px; }
            #Card { background-color: #ffffff; border-radius: 40px; }
            QLineEdit {
                background-color: #f1f5f9; border: 1px solid #e2e8f0;
                border-radius: 15px; padding: 12px; font-size: 14px; color: #1e293b;
            }
            QLineEdit:focus { border: 2px solid #000000; }
            QPushButton#BtnLogin {
                background-color: #000000; color: white; border-radius: 15px;
                font-size: 15px; font-weight: bold; padding: 14px;
            }
            QPushButton#BtnLogin:hover { background-color: #333333; }
            QCheckBox { color: #64748b; font-size: 12px; }
            #BtnLink { border: none; color: #64748b; font-size: 13px; background: transparent; }
            #BtnLink:hover { color: #000000; text-decoration: underline; }
            #BtnRegistrate { 
                border: none; color: #000000; font-size: 13px; font-weight: bold; background: transparent; 
            }
            #BtnRegistrate:hover { text-decoration: underline; }
            #BtnClose { border: none; color: #94a3b8; font-size: 20px; background: transparent; font-weight: bold; }
            #BtnClose:hover { color: #ff4444; }
            #LblError { color: #ef4444; font-size: 12px; font-weight: 600; }
        """)

    def _construir(self):
        self.container = QFrame(self)
        self.container.setObjectName("MainContainer")
        self.container.setFixedSize(1000, 650)
        layout_h = QHBoxLayout(self.container)

        # Panel Izquierdo
        seccion_izq = QWidget()
        layout_izq = QVBoxLayout(seccion_izq)
        layout_izq.setContentsMargins(80, 0, 40, 0); layout_izq.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_logo = QLabel("MOVIE AI"); lbl_logo.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: bold;")
        lbl_titulo = QLabel("Analiza el cine."); lbl_titulo.setStyleSheet("color: #ffffff; font-size: 52px; font-weight: 800;")
        lbl_desc = QLabel("Plataforma avanzada de análisis cinematográfico con IA."); lbl_desc.setStyleSheet("color: #94a3b8; font-size: 15px;")
        
        layout_izq.addWidget(lbl_logo, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_izq.addWidget(lbl_titulo, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_izq.addWidget(lbl_desc, alignment=Qt.AlignmentFlag.AlignLeft)

        # Panel Derecho (Tarjeta)
        seccion_der = QWidget()
        layout_der = QVBoxLayout(seccion_der); layout_der.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        self.card = QFrame(); self.card.setObjectName("Card"); self.card.setFixedSize(380, 560) 
        shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(60); shadow.setColor(QColor(0, 0, 0, 180))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(35, 25, 35, 35); card_layout.setSpacing(18) 

        btn_x = QPushButton("✕"); btn_x.setObjectName("BtnClose")
        btn_x.clicked.connect(self.close)
        card_layout.addWidget(btn_x, alignment=Qt.AlignmentFlag.AlignRight)

        lbl_welcome = QLabel("Bienvenido de nuevo")
        lbl_welcome.setStyleSheet("font-size: 24px; font-weight: 800; color: #0f172a;")
        lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_welcome)

        self.e_user = QLineEdit(); self.e_user.setPlaceholderText("Usuario o correo")
        card_layout.addWidget(self.e_user)

        self.e_pass = QLineEdit(); self.e_pass.setPlaceholderText("Contraseña"); self.e_pass.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.e_pass)

        self.chk_ver = QCheckBox("Mostrar contraseña"); self.chk_ver.stateChanged.connect(self._mostrar_pass)
        card_layout.addWidget(self.chk_ver)

        btn_olvido = QPushButton("¿Olvidaste tu contraseña?"); btn_olvido.setObjectName("BtnLink")
        btn_olvido.clicked.connect(self._abrir_cambio_pass)
        card_layout.addWidget(btn_olvido, alignment=Qt.AlignmentFlag.AlignRight)

        btn_ingresar = QPushButton("Ingresar"); btn_ingresar.setObjectName("BtnLogin")
        btn_ingresar.clicked.connect(self._login)
        card_layout.addWidget(btn_ingresar)

        card_layout.addStretch() 

        layout_reg = QHBoxLayout(); layout_reg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_t = QLabel("¿No tienes cuenta?"); lbl_t.setStyleSheet("color: #64748b;")
        btn_reg = QPushButton("Regístrate"); btn_reg.setObjectName("BtnRegistrate")
        btn_reg.clicked.connect(self._abrir_registro)
        layout_reg.addWidget(lbl_t); layout_reg.addWidget(btn_reg)
        card_layout.addLayout(layout_reg)

        self.lbl_error = QLabel(""); self.lbl_error.setObjectName("LblError"); self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.lbl_error)

        layout_der.addWidget(self.card)
        layout_h.addWidget(seccion_izq, 1); layout_h.addWidget(seccion_der, 1)

    def _abrir_registro(self):
        self.v_reg = FormCrearUsuario(self); self.v_reg.show(); self.hide()

    def _abrir_cambio_pass(self):
        self.v_pass = FormCambioPass(self); self.v_pass.show(); self.hide()

    def _mostrar_pass(self, state):
        self.e_pass.setEchoMode(QLineEdit.EchoMode.Normal if state == 2 else QLineEdit.EchoMode.Password)

    def _login(self):
        u, p = self.e_user.text().strip(), self.e_pass.text()
        if not u or not p: self.lbl_error.setText("Faltan datos"); return
        try:
            ok, err, d, a = ClaseLogin.autenticar(u, p)
            if ok:
                self.ventana_cat = CatalogoWindow(usuario=d, rol=d.get("rol", "lector"))
                self.ventana_cat.show(); self.close()
            else: self.lbl_error.setText(str(err))
        except: self.lbl_error.setText("Error interno")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.old_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y()); self.old_pos = event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event): self.old_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv); win = FormLogin(); win.show(); sys.exit(app.exec())