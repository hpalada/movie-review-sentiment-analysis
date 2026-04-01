import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, 
    QFrame, QGraphicsDropShadowEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

# --- IMPORTACIONES DE TU PROYECTO ---
try:
    from ClaseLogin import ClaseLogin
except ImportError:
    pass


class FormCambioPass(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._login_referencia = parent # Referencia para volver al Login
        
        # Configuración de ventana moderna
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(450, 550)
        
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
            #MainFrame { background-color: #000000; border-radius: 30px; }
            #Card { background-color: #ffffff; border-radius: 30px; }
            
            QLabel#Titulo { font-size: 22px; font-weight: 800; color: #0f172a; }
            QLabel#Subtitulo { font-size: 13px; color: #64748b; }
            
            QLineEdit {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
                color: #1e293b;
            }
            QLineEdit:focus { border: 2px solid #000000; }
            
            QPushButton#BtnActualizar {
                background-color: #000000;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                margin-top: 10px;
            }
            QPushButton#BtnActualizar:hover { background-color: #333333; }
            
            QPushButton#BtnCerrar {
                border: none; color: #94a3b8; font-size: 18px; background: transparent; font-weight: bold;
            }
            QPushButton#BtnCerrar:hover { color: #ff4444; }

            #LblStatus { font-size: 12px; font-weight: 600; }
        """)

    def _construir(self):
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedSize(450, 550)

        main_layout = QVBoxLayout(self.main_frame)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.card = QFrame()
        self.card.setObjectName("Card")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40); shadow.setColor(QColor(0, 0, 0, 150))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(35, 20, 35, 30); card_layout.setSpacing(15)

        # Cerrar
        btn_x = QPushButton("✕")
        btn_x.setObjectName("BtnCerrar")
        btn_x.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_x.clicked.connect(self.close)
        card_layout.addWidget(btn_x, alignment=Qt.AlignmentFlag.AlignRight)

        # Cabecera
        lbl_t = QLabel("Recuperar Acceso")
        lbl_t.setObjectName("Titulo"); lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_st = QLabel("Ingresa los datos para actualizar")
        lbl_st.setObjectName("Subtitulo"); lbl_st.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_t); card_layout.addWidget(lbl_st)
        card_layout.addSpacing(10)

        # Campos
        self.e_email = QLineEdit()
        self.e_email.setPlaceholderText("Correo electrónico registrado")
        card_layout.addWidget(self.e_email)

        self.e_nueva = QLineEdit()
        self.e_nueva.setPlaceholderText("Nueva contraseña")
        self.e_nueva.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.e_nueva)

        self.e_confirm = QLineEdit()
        self.e_confirm.setPlaceholderText("Confirmar nueva contraseña")
        self.e_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.e_confirm)

        # Botón
        btn_act = QPushButton("Actualizar Contraseña")
        btn_act.setObjectName("BtnActualizar")
        btn_act.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_act.clicked.connect(self._cambiar)
        card_layout.addWidget(btn_act)

        # Status
        self.lbl_status = QLabel("")
        self.lbl_status.setObjectName("LblStatus")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl_status.setWordWrap(True)
        card_layout.addWidget(self.lbl_status)

        main_layout.addWidget(self.card)

    def _cambiar(self):
        em, n, c = self.e_email.text().strip(), self.e_nueva.text(), self.e_confirm.text()
        if not all([em, n, c]):
            self.lbl_status.setStyleSheet("color: #ef4444;")
            self.lbl_status.setText("Completa todos los campos")
            return

        try:
            ok, err, aviso = ClaseLogin.cambiar_password(em, n, c)
            if ok:
                self.lbl_status.setStyleSheet("color: #10b981;")
                self.lbl_status.setText("¡Éxito! Contraseña actualizada.")
                QTimer.singleShot(1500, self.close)
            else:
                self.lbl_status.setStyleSheet("color: #ef4444;")
                self.lbl_status.setText(str(err))
        except:
            self.lbl_status.setText("Error de conexión")

    def closeEvent(self, event):
        if self._login_referencia: self._login_referencia.show()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.old_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y()); self.old_pos = event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event): self.old_pos = None