import os
import shutil
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QFrame,
    QGraphicsDropShadowEffect, QScrollArea, QWidget
)
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt
from clasePelicula import Pelicula

# Rutas base
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CARPETA_IMGS = os.path.join(BASE_DIR, "Imagenes")

def _ruta_completa(nombre_archivo: str) -> str:
    if not nombre_archivo:
        return ""
    if os.path.isabs(nombre_archivo):
        return nombre_archivo
    return os.path.join(CARPETA_IMGS, nombre_archivo)


# ══════════════════════════════════════════════════════════════════════════════
#  DIÁLOGO CUSTOM (sin barra de título del sistema operativo)
# ══════════════════════════════════════════════════════════════════════════════

class _CustomDialog(QDialog):
    def __init__(self, titulo: str, mensaje: str, btn_ok: str = "Aceptar",
                 btn_cancel: str = None, parent=None):
        super().__init__(parent)
        self._result = False
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self._build(titulo, mensaje, btn_ok, btn_cancel)

    def _build(self, titulo, mensaje, btn_ok, btn_cancel):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("dlgCard")
        card.setStyleSheet("""
            QFrame#dlgCard {
                background-color: #FFFFFF;
                border-radius: 14px;
                border: 1px solid #E5E7EB;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 24, 28, 20)
        lay.setSpacing(0)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            color: #111827;
            font-size: 15px; font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        """)
        lay.addWidget(lbl_titulo)
        lay.addSpacing(10)

        lbl_msg = QLabel(mensaje)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet("""
            color: #6B7280;
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        """)
        lay.addWidget(lbl_msg)
        lay.addSpacing(22)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        if btn_cancel:
            b_cancel = QPushButton(btn_cancel)
            b_cancel.setFixedHeight(38)
            b_cancel.setMinimumWidth(100)
            b_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            b_cancel.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #6B7280;
                    border: 1.5px solid #E5E7EB;
                    border-radius: 8px; padding: 0 18px;
                    font-size: 13px; font-weight: 600;
                    font-family: 'Segoe UI', sans-serif;
                }
                QPushButton:hover {
                    background-color: #F3F4F6;
                    border-color: #D1D5DB;
                    color: #374151;
                }
            """)
            b_cancel.clicked.connect(self.reject)
            btn_row.addWidget(b_cancel)

        b_ok = QPushButton(btn_ok)
        b_ok.setFixedHeight(38)
        b_ok.setMinimumWidth(100)
        b_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        b_ok.setStyleSheet("""
            QPushButton {
                background-color: #111827;
                color: #FFFFFF; border: none; border-radius: 8px;
                padding: 0 18px; font-size: 13px; font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover { background-color: #1F2937; }
            QPushButton:pressed { background-color: #374151; }
        """)
        b_ok.clicked.connect(self._on_ok)
        btn_row.addWidget(b_ok)

        lay.addLayout(btn_row)
        outer.addWidget(card)
        self.setFixedWidth(380)

    def _on_ok(self):
        self._result = True
        self.accept()

    @staticmethod
    def preguntar(titulo: str, mensaje: str, btn_si: str = "Sí",
                  btn_no: str = "No", parent=None) -> bool:
        dlg = _CustomDialog(titulo, mensaje, btn_ok=btn_si,
                             btn_cancel=btn_no, parent=parent)
        dlg.exec()
        return dlg._result

    @staticmethod
    def informar(titulo: str, mensaje: str, parent=None):
        dlg = _CustomDialog(titulo, mensaje, btn_ok="Aceptar",
                             btn_cancel=None, parent=parent)
        dlg.exec()


# Estilos
STYLE_MAIN = """
    QWidget {
        background-color: #F7F8FA;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_LABEL_SECTION = """
    QLabel {
        color: #6B7280;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.9px;
        background: transparent;
        padding: 0px;
        margin: 0px;
    }
"""

STYLE_INPUT = """
    QLineEdit {
        background-color: #FFFFFF;
        border: 1.5px solid #E5E7EB;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        color: #111827;
        font-family: 'Segoe UI', sans-serif;
        selection-background-color: #3B82F6;
    }
    QLineEdit:focus {
        border: 1.5px solid #3B82F6;
        background-color: #FFFFFF;
    }
    QLineEdit:hover {
        border: 1.5px solid #D1D5DB;
    }
    QLineEdit[readOnly="true"] {
        background-color: #F9FAFB;
        color: #6B7280;
    }
"""

STYLE_BTN_PRIMARY = """
    QPushButton {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 11px 20px;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }
    QPushButton:hover {
        background-color: #1F2937;
    }
    QPushButton:pressed {
        background-color: #374151;
    }
"""

STYLE_BTN_SECONDARY = """
    QPushButton {
        background-color: transparent;
        color: #6B7280;
        border: 1.5px solid #E5E7EB;
        border-radius: 10px;
        padding: 11px 20px;
        font-size: 13px;
        font-weight: 500;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #F3F4F6;
        border-color: #D1D5DB;
        color: #374151;
    }
    QPushButton:pressed {
        background-color: #E5E7EB;
    }
"""

STYLE_BTN_IMG = """
    QPushButton {
        background-color: #EEF2FF;
        color: #4F46E5;
        border: 1.5px solid #C7D2FE;
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #E0E7FF;
        border-color: #A5B4FC;
    }
    QPushButton:pressed {
        background-color: #C7D2FE;
    }
"""

STYLE_IMAGE_CONTAINER = """
    QLabel {
        background-color: #F3F4F6;
        border: 2px dashed #D1D5DB;
        border-radius: 12px;
        color: #9CA3AF;
        font-size: 12px;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_DIVIDER = """
    QFrame {
        background-color: #E5E7EB;
        border: none;
        max-height: 1px;
    }
"""

STYLE_DIVIDER_V = """
    QFrame {
        background-color: #E5E7EB;
        border: none;
        max-width: 1px;
    }
"""

STYLE_SCROLL = """
    QScrollArea {
        border: none;
        background: transparent;
    }
    QScrollArea > QWidget > QWidget {
        background: transparent;
    }
    QScrollBar:vertical {
        background: transparent;
        width: 5px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #D1D5DB;
        border-radius: 3px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #9CA3AF;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""


def _agregar_campo(parent_layout: QVBoxLayout, etiqueta: str, placeholder: str) -> QLineEdit:
    lbl = QLabel(etiqueta)
    lbl.setStyleSheet(STYLE_LABEL_SECTION)
    parent_layout.addWidget(lbl)
    parent_layout.addSpacing(7)

    inp = QLineEdit()
    inp.setPlaceholderText(placeholder)
    inp.setStyleSheet(STYLE_INPUT)
    inp.setFixedHeight(42)
    parent_layout.addWidget(inp)
    return inp


class PeliculaUI(QDialog):
    def __init__(self, pelicula=None, callback=None, parent=None):
        super().__init__(parent)
        self.pelicula   = pelicula
        self.callback   = callback
        self.es_edicion = pelicula is not None
        self._ruta_imagen_original = None
        # Flag para saber si el usuario explícitamente quitó la imagen
        self._imagen_eliminada = False

        self.setWindowTitle("Editar película" if self.es_edicion else "Agregar película")
        self.setFixedSize(820, 520)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setStyleSheet(STYLE_MAIN)

        os.makedirs(CARPETA_IMGS, exist_ok=True)
        self._construir_ui()

        if self.es_edicion:
            self._precargar()

    def _construir_ui(self):
        root = QVBoxLayout(self)
        # HEADER INTERNO
        header = QWidget()
        header.setStyleSheet("background: transparent;")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 10)
        header_layout.setSpacing(4)

        lbl_title = QLabel("Agregar película" if not self.es_edicion else "Editar película")
        lbl_title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        """)

        lbl_sub = QLabel(
            "Completa la información de la película"
            if not self.es_edicion else
            "Modifica los datos de la película"
        )
        lbl_sub.setStyleSheet("""
            color: #9CA3AF;
            font-size: 12px;
            font-family: 'Segoe UI', sans-serif;
        """)

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_sub)
        
        root.addWidget(header)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: #E5E7EB; max-height: 1px;")
        root.addWidget(div)
        # Cuerpo: columna izquierda + derecha
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # COLUMNA IZQUIERDA
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left_scroll.setStyleSheet(STYLE_SCROLL)
        left_scroll.setFixedWidth(410)

        left_widget = QWidget()
        left_widget.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(32, 28, 28, 28)
        left_layout.setSpacing(0)

        self.input_titulo = _agregar_campo(left_layout, "TÍTULO", "Nombre de la pelicula")
        left_layout.addSpacing(18)

        row1 = QHBoxLayout()
        row1.setSpacing(14)

        col_anio = QVBoxLayout()
        col_anio.setSpacing(0)
        lbl_anio = QLabel("AÑO")
        lbl_anio.setStyleSheet(STYLE_LABEL_SECTION)
        col_anio.addWidget(lbl_anio)
        col_anio.addSpacing(7)
        self.input_anio = QLineEdit()
        self.input_anio.setStyleSheet(STYLE_INPUT)
        self.input_anio.setFixedHeight(42)
        col_anio.addWidget(self.input_anio)

        col_dir = QVBoxLayout()
        col_dir.setSpacing(0)
        lbl_dir = QLabel("DIRECTOR")
        lbl_dir.setStyleSheet(STYLE_LABEL_SECTION)
        col_dir.addWidget(lbl_dir)
        col_dir.addSpacing(7)
        self.input_director = QLineEdit()
        self.input_director.setStyleSheet(STYLE_INPUT)
        self.input_director.setFixedHeight(42)
        col_dir.addWidget(self.input_director)

        row1.addLayout(col_anio, 1)
        row1.addLayout(col_dir, 2)
        left_layout.addLayout(row1)
        left_layout.addSpacing(18)

        self.input_fecha = _agregar_campo(left_layout, "FECHA DE PUBLICACIÓN", "Ejemplo: 2024-05-17")
        left_layout.addSpacing(18)

        self.input_desc = _agregar_campo(left_layout, "DESCRIPCIÓN", "Breve sinopsis de la película...")
        left_layout.addStretch()

        left_scroll.setWidget(left_widget)
        body.addWidget(left_scroll)

        # Separador vertical
        div_v = QFrame()
        div_v.setFrameShape(QFrame.Shape.VLine)
        div_v.setStyleSheet(STYLE_DIVIDER_V)
        body.addWidget(div_v)

        # COLUMNA DERECHA
        right_widget = QWidget()
        right_widget.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(28, 28, 32, 28)
        right_layout.setSpacing(0)

        lbl_img_sec = QLabel("IMAGEN DE PORTADA")
        lbl_img_sec.setStyleSheet(STYLE_LABEL_SECTION)
        right_layout.addWidget(lbl_img_sec)
        right_layout.addSpacing(7)

        img_row = QHBoxLayout()
        img_row.setSpacing(8)

        self.input_imagen = QLineEdit()
        self.input_imagen.setPlaceholderText("Selecciona una imagen")
        self.input_imagen.setReadOnly(True)
        self.input_imagen.setStyleSheet(STYLE_INPUT)
        self.input_imagen.setFixedHeight(42)
        self.input_imagen.setMinimumWidth(150)

        btn_remove = QPushButton("✕")
        btn_remove.setFixedSize(28, 28)
        btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_remove.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FF0000;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #FF0000;
                color: #FFFFFF;
            }
        """)
        btn_remove.clicked.connect(self._quitar_imagen)

        btn_img = QPushButton("＋ Explorar")
        btn_img.setFixedHeight(42)
        btn_img.setFixedWidth(100)
        btn_img.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_img.setStyleSheet(STYLE_BTN_IMG)
        btn_img.clicked.connect(self._seleccionar_imagen)

        img_row.addWidget(btn_remove)
        img_row.addWidget(self.input_imagen, 1)
        img_row.addWidget(btn_img)

        right_layout.addLayout(img_row)
        right_layout.addSpacing(18)

        self.label_imagen = QLabel("Sin imagen\nseleccionada")
        self.label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_imagen.setStyleSheet(STYLE_IMAGE_CONTAINER)
        self.label_imagen.setMinimumHeight(260)
        right_layout.addWidget(self.label_imagen, stretch=1)

        body.addWidget(right_widget, stretch=1)
        root.addLayout(body, stretch=1)

        # Footer con botones
        div_bot = QFrame()
        div_bot.setFrameShape(QFrame.Shape.HLine)
        div_bot.setStyleSheet(STYLE_DIVIDER)
        root.addWidget(div_bot)

        footer = QWidget()
        footer.setFixedHeight(70)
        footer.setStyleSheet("background: transparent;")
        foot_layout = QHBoxLayout(footer)
        foot_layout.setContentsMargins(32, 0, 32, 0)
        foot_layout.setSpacing(10)

        foot_layout.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFixedSize(130, 42)
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancelar.setStyleSheet(STYLE_BTN_SECONDARY)
        btn_cancelar.clicked.connect(self.close)

        self.btn_guardar = QPushButton(
            "✓  Actualizar" if self.es_edicion else "✓  Guardar"
        )
        self.btn_guardar.setFixedSize(160, 42)
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.setStyleSheet(STYLE_BTN_PRIMARY)
        self.btn_guardar.clicked.connect(self._guardar)

        foot_layout.addWidget(btn_cancelar)
        foot_layout.addWidget(self.btn_guardar)
        root.addWidget(footer)

    def _precargar(self):
        self.input_titulo.setText(self.pelicula.titulo or "")
        self.input_desc.setText(self.pelicula.descripcion or "")
        self.input_fecha.setText(self.pelicula.fecha or "")
        self.input_anio.setText(str(self.pelicula.anio) if self.pelicula.anio else "")
        self.input_director.setText(self.pelicula.director or "")

        nombre_img = self.pelicula.imagen or ""
        self.input_imagen.setText(nombre_img)
        if nombre_img:
            self._mostrar_imagen(_ruta_completa(nombre_img))

    def _seleccionar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if ruta:
            self._ruta_imagen_original = ruta
            self._imagen_eliminada = False          # nueva imagen, no eliminada
            self.input_imagen.setText(os.path.basename(ruta))
            self._mostrar_imagen(ruta)

    def _quitar_imagen(self):
        """Limpia la imagen visual Y marca el flag para que _guardar la elimine del registro."""
        self._ruta_imagen_original = None
        self._imagen_eliminada = True               # ← flag corregido
        self.input_imagen.clear()
        self.label_imagen.clear()
        self.label_imagen.setText("Sin imagen\nseleccionada")
        self.label_imagen.setStyleSheet(STYLE_IMAGE_CONTAINER)

    def _mostrar_imagen(self, ruta_absoluta: str):
        if ruta_absoluta and os.path.exists(ruta_absoluta):
            px = QPixmap(ruta_absoluta)
            if not px.isNull():
                self.label_imagen.setPixmap(
                    px.scaled(
                        self.label_imagen.width() - 8,
                        self.label_imagen.height() - 8,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                self.label_imagen.setStyleSheet("""
                    QLabel {
                        background-color: #F3F4F6;
                        border: 2px solid #E5E7EB;
                        border-radius: 12px;
                    }
                """)
                return
        self.label_imagen.clear()
        self.label_imagen.setText("Sin imagen\nseleccionada")
        self.label_imagen.setStyleSheet(STYLE_IMAGE_CONTAINER)

    def _copiar_imagen(self, ruta_origen: str) -> str:
        nombre  = os.path.basename(ruta_origen)
        destino = os.path.join(CARPETA_IMGS, nombre)
        if os.path.abspath(ruta_origen) != os.path.abspath(destino):
            base, ext = os.path.splitext(nombre)
            contador  = 1
            while os.path.exists(destino):
                nombre  = f"{base}_{contador}{ext}"
                destino = os.path.join(CARPETA_IMGS, nombre)
                contador += 1
            shutil.copy2(ruta_origen, destino)
        return nombre

    def _guardar(self):
        titulo = self.input_titulo.text().strip()
        if not titulo:
            _CustomDialog.informar("Error", "El título es obligatorio.", parent=self)
            return

        descripcion = self.input_desc.text().strip() or None
        fecha       = self.input_fecha.text().strip() or None
        director    = self.input_director.text().strip() or None
        anio_txt    = self.input_anio.text().strip()
        anio        = int(anio_txt) if anio_txt.isdigit() else None

        # Lógica de imagen corregida:
        # - Si el usuario seleccionó una nueva imagen → copiar y usar
        # - Si el usuario quitó la imagen (_imagen_eliminada) → None
        # - Si no tocó nada → mantener la imagen anterior (solo en edición)
        if self._ruta_imagen_original:
            imagen = self._copiar_imagen(self._ruta_imagen_original)
        elif self._imagen_eliminada:
            imagen = None                           # ← eliminación real
        elif self.es_edicion:
            imagen = self.pelicula.imagen           # ← mantener la anterior
        else:
            imagen = None

        if self.es_edicion:
            ok = self.pelicula.actualizar(
                titulo=titulo, descripcion=descripcion, imagen=imagen,
                fecha=fecha, anio=anio, director=director
            )
            msg_text = "Película actualizada." if ok else "No se pudo actualizar."
        else:
            Pelicula.guardar(
                titulo=titulo, descripcion=descripcion, imagen=imagen,
                fecha=fecha, anio=anio, director=director
            )
            msg_text = "Película guardada."

        _CustomDialog.informar("Éxito", msg_text, parent=self)

        if self.callback:
            self.callback()
        self.close()