#FormReseñas
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QPushButton, QFrame, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QByteArray
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon
from PyQt6.QtSvgWidgets import QSvgWidget
from ClaseReseña import Resena
from Json import JsonManager
from rutas import ruta_imagen


#Paleta y estilos
STYLE_MAIN = """
    QWidget {
        background-color: #F7F8FA;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_SCROLL = """
    QScrollArea {
        border: none;
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
        min-height: 24px;
    }
    QScrollBar::handle:vertical:hover {
        background: #9CA3AF;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

STYLE_CABECERA = """
    QFrame#cabecera {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E5E7EB;
    }
"""

STYLE_POSTER = """
    QLabel#poster {
        background-color: #F3F4F6;
        border: 2px dashed #D1D5DB;
        border-radius: 12px;
        color: #9CA3AF;
        font-size: 12px;
    }
"""

STYLE_POSTER_FILLED = """
    QLabel#poster {
        background-color: #F3F4F6;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
    }
"""

STYLE_TITULO_PELICULA = """
    QLabel {
        color: #111827;
        font-size: 22px;
        font-weight: 700;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
    }
"""

STYLE_META_LABEL = """
    QLabel {
        color: #6B7280;
        font-size: 12px;
        font-weight: 500;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
        letter-spacing: 0.5px;
    }
"""

STYLE_SECCION_TITULO = """
    QLabel {
        color: #111827;
        font-size: 15px;
        font-weight: 700;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
    }
"""

STYLE_TARJETA = """
    QFrame#tarjeta {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
    }
    QFrame#tarjeta:hover {
        border: 1px solid #D1D5DB;
    }
"""

STYLE_USUARIO_LABEL = """
    QLabel {
        color: #111827;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
    }
"""

STYLE_TEXTO_RESENA = """
    QLabel {
        color: #374151;
        font-size: 12px;
        font-weight: 400;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
        line-height: 1.5;
    }
"""

STYLE_LEER_MAS = """
    QLabel {
        color: #6B7280;
        font-size: 11px;
        font-weight: 500;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
        text-decoration: underline;
    }
    QLabel:hover {
        color: #374151;
    }
"""

STYLE_ETIQUETA_CHIP = """
    QLabel {
        background-color: #F3F4F6;
        color: #374151;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }
"""

STYLE_BTN_AGREGAR = """
    QPushButton {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 0px;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.5px;
    }
    QPushButton:hover {
        background-color: #1F2937;
    }
    QPushButton:pressed {
        background-color: #374151;
    }
"""

STYLE_BTN_EDITAR = """
    QPushButton {
        background-color: transparent;
        color: #6B7280;
        border: 1.5px solid #E5E7EB;
        border-radius: 7px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #F3F4F6;
        border-color: #D1D5DB;
        color: #374151;
    }
"""

STYLE_BTN_ELIMINAR = """
    QPushButton {
        background-color: transparent;
        color: #EF4444;
        border: 1.5px solid #FCA5A5;
        border-radius: 7px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #FEF2F2;
        border-color: #EF4444;
    }
"""

STYLE_DIVIDER = """
    QFrame {
        background-color: #E5E7EB;
        border: none;
        max-height: 1px;
    }
"""

STYLE_AVATAR = """
    QLabel#avatar {
        background-color: #EEF2FF;
        color: #4F46E5;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 700;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_MSGBOX = """
    QMessageBox {
        background-color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }
    QMessageBox QLabel {
        color: #111827;
        font-size: 13px;
    }
    QMessageBox QPushButton {
        background-color: #111827;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 12px;
        font-weight: 600;
        min-width: 80px;
    }
    QMessageBox QPushButton:hover {
        background-color: #1F2937;
    }
"""

# ── SVGs ──────────────────────────────────────────────────────────────────────

SVG_STAR_FILLED = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#F59E0B" d="M12 2l3.09 6.26L22 9.27l-5 4.87
    1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>"""

SVG_STAR_HALF = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs>
    <linearGradient id="h" x1="0" x2="1" y1="0" y2="0">
      <stop offset="50%" stop-color="#FCD34D"/>
      <stop offset="50%" stop-color="#D1D5DB"/>
    </linearGradient>
  </defs>
  <path fill="url(#h)" d="M12 2l3.09 6.26L22 9.27l-5 4.87
    1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>"""

SVG_STAR_EMPTY = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#D1D5DB" d="M12 2l3.09 6.26L22 9.27l-5 4.87
    1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>"""

# Estrella grande para el promedio de la cabecera
SVG_STAR_BIG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#F59E0B" d="M12 2l3.09 6.26L22 9.27l-5 4.87
    1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>"""

# Icono "+" para el botón Agregar reseña
SVG_PLUS = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="#FFFFFF" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
  <line x1="12" y1="5" x2="12" y2="19"/>
  <line x1="5" y1="12" x2="19" y2="12"/>
</svg>"""

# Icono lápiz para Editar
SVG_EDIT = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="#6B7280" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14
           a2 2 0 0 0 2-2v-7"/>
  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3
           L12 15l-4 1 1-4 9.5-9.5z"/>
</svg>"""

# Icono papelera para Eliminar
SVG_TRASH = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="#EF4444" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 6 5 6 21 6"/>
  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8
           a2 2 0 0 1-2-2L5 6"/>
  <path d="M10 11v6"/>
  <path d="M14 11v6"/>
  <path d="M9 6V4a1 1 0 0 1 1-1h4
           a1 1 0 0 1 1 1v2"/>
</svg>"""


def _svg_widget(svg_bytes: bytes, size: int) -> QSvgWidget:
    """Crea un QSvgWidget a partir de bytes SVG."""
    w = QSvgWidget()
    w.load(QByteArray(svg_bytes))
    w.setFixedSize(size, size)
    w.setStyleSheet("background: transparent;")
    return w


def _estrellas_widget(valoracion, maximo: int = 5) -> QWidget:
    """
    Devuelve un QWidget con estrellas SVG coloreadas según la valoración.
    Soporta valores sobre 5 (escala de la IA).
    """
    contenedor = QWidget()
    contenedor.setStyleSheet("background: transparent;")
    fila = QHBoxLayout(contenedor)
    fila.setContentsMargins(0, 0, 0, 0)
    fila.setSpacing(2)

    try:
        val = float(valoracion) if valoracion is not None else 0
    except (ValueError, TypeError):
        val = 0

    # Normalizar a escala /5
    val_norm = min(val, maximo) / maximo * 5

    for i in range(5):
        if val_norm >= i + 1:
            star = _svg_widget(SVG_STAR_FILLED, 18)
        elif val_norm >= i + 0.5:
            star = _svg_widget(SVG_STAR_HALF, 18)
        else:
            star = _svg_widget(SVG_STAR_EMPTY, 18)
        fila.addWidget(star)

    fila.addStretch()
    return contenedor


def _sombra_tarjeta() -> QGraphicsDropShadowEffect:
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(18)
    s.setOffset(0, 3)
    s.setColor(QColor(0, 0, 0, 18))
    return s


class FormResenas(QWidget):
    def __init__(self, pelicula_id, usuario_id, clase_pelicula,
                 clase_resena=None, titulo_pelicula="", pelicula_obj=None):
        super().__init__()
        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_pelicula  = clase_pelicula
        self.clase_resena    = Resena()
        self.titulo_pelicula = titulo_pelicula
        self.pelicula_obj    = pelicula_obj
        self.db              = JsonManager()

        self.setWindowTitle("Reseñas")
        self.resize(1100, 750)
        self.setStyleSheet(STYLE_MAIN)
        self._construir_ui()
        self._cargar_datos()



    def _construir_ui(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        #Cabecera fija
        self.widget_cabecera = self._crear_cabecera()
        layout_raiz.addWidget(self.widget_cabecera)

        # Divisor bajo la cabecera
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(STYLE_DIVIDER)
        layout_raiz.addWidget(div)

        #Área scrollable con las reseñas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet(STYLE_SCROLL)

        self.contenido_scroll = QWidget()
        self.contenido_scroll.setStyleSheet("background: transparent;")
        self.layout_scroll = QVBoxLayout(self.contenido_scroll)
        self.layout_scroll.setContentsMargins(32, 24, 32, 24)
        self.layout_scroll.setSpacing(0)

        # Título de sección
        lbl_sec = QLabel("Reseñas de usuarios")
        lbl_sec.setStyleSheet(STYLE_SECCION_TITULO)
        self.layout_scroll.addWidget(lbl_sec)
        self.layout_scroll.addSpacing(16)

        # Contenedor de tarjetas
        self.layout_resenas = QVBoxLayout()
        self.layout_resenas.setSpacing(12)
        self.layout_scroll.addLayout(self.layout_resenas)
        self.layout_scroll.addStretch()

        self.scroll_area.setWidget(self.contenido_scroll)
        layout_raiz.addWidget(self.scroll_area, stretch=1)

        #Botón agregar con icono SVG
        self.btn_agregar = QPushButton("  Agregar reseña")
        self.btn_agregar.setFixedHeight(52)
        self.btn_agregar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_agregar.setStyleSheet(STYLE_BTN_AGREGAR)
        self.btn_agregar.setIcon(QIcon(self._pixmap_from_svg(SVG_PLUS, 16)))
        self.btn_agregar.clicked.connect(self._abrir_form_agregar)
        layout_raiz.addWidget(self.btn_agregar)

    def _pixmap_from_svg(self, svg_bytes: bytes, size: int) -> QPixmap:
        """Convierte bytes SVG en QPixmap para usar como QIcon."""
        from PyQt6.QtSvg import QSvgRenderer
        from PyQt6.QtGui import QPainter
        renderer = QSvgRenderer(QByteArray(svg_bytes))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def _crear_cabecera(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("cabecera")
        frame.setStyleSheet(STYLE_CABECERA)
        frame.setFixedHeight(220)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(28)

        #Poster
        self.lbl_poster = QLabel("POSTER")
        self.lbl_poster.setObjectName("poster")
        self.lbl_poster.setFixedSize(116, 170)
        self.lbl_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_poster.setStyleSheet(STYLE_POSTER)
        layout.addWidget(self.lbl_poster)

        #Info: título, promedio con estrellas, etiquetas
        layout_info = QVBoxLayout()
        layout_info.setSpacing(0)
        layout_info.setContentsMargins(0, 0, 0, 0)

        self.lbl_nombre = QLabel(self.titulo_pelicula or "Película")
        self.lbl_nombre.setStyleSheet(STYLE_TITULO_PELICULA)
        layout_info.addWidget(self.lbl_nombre)
        layout_info.addSpacing(10)

        # Fila: estrella SVG grande + número promedio
        fila_promedio = QHBoxLayout()
        fila_promedio.setSpacing(10)
        fila_promedio.setContentsMargins(0, 0, 0, 0)

        self.svg_estrella_grande = _svg_widget(SVG_STAR_BIG, 28)
        self.lbl_promedio_num = QLabel("—")
        self.lbl_promedio_num.setStyleSheet(
            "color: #111827; font-size: 28px; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        self.lbl_sobre_cinco = QLabel("/ 5")
        self.lbl_sobre_cinco.setStyleSheet(
            "color: #9CA3AF; font-size: 16px; font-weight: 400; "
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        fila_promedio.addWidget(self.svg_estrella_grande)
        fila_promedio.addWidget(self.lbl_promedio_num)
        fila_promedio.addWidget(self.lbl_sobre_cinco)
        fila_promedio.addStretch()
        layout_info.addLayout(fila_promedio)
        layout_info.addSpacing(6)

        # Fila de estrellas pequeñas SVG
        self.widget_estrellas = _estrellas_widget(0, maximo=5)
        layout_info.addWidget(self.widget_estrellas)
        layout_info.addSpacing(10)

        # Etiquetas chips
        self.fila_etiquetas = QHBoxLayout()
        self.fila_etiquetas.setSpacing(6)
        self.fila_etiquetas.setContentsMargins(0, 0, 0, 0)
        layout_info.addLayout(self.fila_etiquetas)
        layout_info.addStretch()

        layout.addLayout(layout_info)
        layout.addStretch()
        return frame


    def _cargar_datos(self):
        self._cargar_info_pelicula()
        self._cargar_resenas()

    def _cargar_info_pelicula(self):
        if self.pelicula_obj:
            ruta_poster = ruta_imagen(getattr(self.pelicula_obj, "imagen", None))
            if ruta_poster and os.path.exists(ruta_poster):
                pixmap = QPixmap(ruta_poster)
                if not pixmap.isNull():
                    self.lbl_poster.setPixmap(
                        pixmap.scaled(116, 170,
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                    )
                    self.lbl_poster.setStyleSheet(STYLE_POSTER_FILLED)
            titulo = getattr(self.pelicula_obj, "titulo", self.titulo_pelicula)
            self.lbl_nombre.setText(titulo or "Sin título")

        self._actualizar_promedio_ui()

    def _actualizar_promedio_ui(self):
        """Lee el promedio del JSON y actualiza estrellas + chips de etiquetas."""
        pelicula_data = self.db.obtener_pelicula_por_id(self.pelicula_id)

        if not pelicula_data:
            self.lbl_promedio_num.setText("—")
            return

        promedio = pelicula_data.get("promedio_calificacion")

        if promedio is not None:
            self.lbl_promedio_num.setText(str(promedio))
            # Reconstruir widget de estrellas
            old = self.widget_estrellas
            self.widget_estrellas = _estrellas_widget(promedio, maximo=5)
            layout_info = old.parent().layout() if old.parent() else None
            if layout_info:
                idx = layout_info.indexOf(old)
                layout_info.removeWidget(old)
                old.deleteLater()
                layout_info.insertWidget(idx, self.widget_estrellas)
        else:
            self.lbl_promedio_num.setText("—")

        # Limpiar chips anteriores
        while self.fila_etiquetas.count():
            item = self.fila_etiquetas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Etiquetas top
        resenas = self.db.obtener_resenas_por_pelicula(self.pelicula_id)
        conteo = {}
        for r in resenas:
            for etiqueta in r.get("etiquetas_ia", []):
                conteo[etiqueta] = conteo.get(etiqueta, 0) + 1

        if conteo:
            top = sorted(conteo, key=conteo.get, reverse=True)[:4]
            for tag in top:
                chip = QLabel(tag)
                chip.setStyleSheet(STYLE_ETIQUETA_CHIP)
                chip.setFixedHeight(24)
                self.fila_etiquetas.addWidget(chip)
        self.fila_etiquetas.addStretch()

    def _cargar_resenas(self):
        # Limpiar tarjetas anteriores
        while self.layout_resenas.count():
            item = self.layout_resenas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._actualizar_promedio_ui()

        if not self.clase_resena:
            self.layout_resenas.addWidget(
                self._lbl_vacio("Aún no hay reseñas para esta película."))
            return

        resenas = self.clase_resena.obtener_resenas_pelicula(self.pelicula_id)

        if not resenas:
            self.layout_resenas.addWidget(
                self._lbl_vacio("Aún no hay reseñas para esta película."))
            return

        for resena in resenas:
            usuario = self.db.obtener_usuario_por_id(resena.get("usuario_id"))
            resena["nombre_usuario"] = (
                usuario["nombre_usuario"] if usuario
                else f"Usuario {resena.get('usuario_id', '?')}"
            )
            self.layout_resenas.addWidget(self._crear_tarjeta(resena))

    def _lbl_vacio(self, texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(
            "color: #9CA3AF; font-size: 13px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent; padding: 40px 0px;"
        )
        return lbl


    def _crear_tarjeta(self, resena: dict) -> QFrame:
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setStyleSheet(STYLE_TARJETA)
        tarjeta.setGraphicsEffect(_sombra_tarjeta())

        layout_tarjeta = QHBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(20, 18, 20, 18)
        layout_tarjeta.setSpacing(20)

        #Avatar circular con inicial
        nombre_usuario = resena.get("nombre_usuario", "?")
        inicial = nombre_usuario[0].upper() if nombre_usuario else "?"

        avatar = QLabel(inicial)
        avatar.setObjectName("avatar")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(STYLE_AVATAR)
        layout_tarjeta.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)

        #Columna principal: usuario + texto
        col_texto = QVBoxLayout()
        col_texto.setSpacing(4)
        col_texto.setContentsMargins(0, 0, 0, 0)

        # Fila: nombre usuario + estrellas SVG de esta reseña
        fila_top = QHBoxLayout()
        fila_top.setSpacing(10)
        fila_top.setContentsMargins(0, 0, 0, 0)

        lbl_usuario = QLabel(nombre_usuario)
        lbl_usuario.setStyleSheet(STYLE_USUARIO_LABEL)
        fila_top.addWidget(lbl_usuario)

        stars = _estrellas_widget(resena.get("valoracion_ia"), maximo=5)
        fila_top.addWidget(stars)
        fila_top.addStretch()
        col_texto.addLayout(fila_top)

        # Texto de la reseña
        texto_completo = resena.get("texto", "")
        texto_corto    = texto_completo[:160] + ("..." if len(texto_completo) > 160 else "")
        lbl_texto = QLabel(texto_corto)
        lbl_texto.setWordWrap(True)
        lbl_texto.setStyleSheet(STYLE_TEXTO_RESENA)
        col_texto.addWidget(lbl_texto)

        if len(texto_completo) > 160:
            lbl_leer = QLabel("leer más")
            lbl_leer.setCursor(Qt.CursorShape.PointingHandCursor)
            lbl_leer.setStyleSheet(STYLE_LEER_MAS)
            col_texto.addWidget(lbl_leer)

        layout_tarjeta.addLayout(col_texto, stretch=5)

        #Columna chips de etiquetas
        col_chips = QVBoxLayout()
        col_chips.setSpacing(5)
        col_chips.setContentsMargins(0, 0, 0, 0)

        for etiqueta in resena.get("etiquetas_ia", []):
            chip = QLabel(etiqueta)
            chip.setStyleSheet(STYLE_ETIQUETA_CHIP)
            chip.setFixedHeight(24)
            chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col_chips.addWidget(chip)

        col_chips.addStretch()
        layout_tarjeta.addLayout(col_chips, stretch=2)

        #Columna derecha: valoración numérica + botones con iconos SVG
        col_derecha = QVBoxLayout()
        col_derecha.setSpacing(6)
        col_derecha.setContentsMargins(0, 0, 0, 0)
        col_derecha.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Número de valoración grande
        val = resena.get("valoracion_ia", "?")
        lbl_num = QLabel(str(val))
        lbl_num.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_num.setStyleSheet(
            "color: #111827; font-size: 22px; font-weight: 700; "
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lbl_sobre = QLabel("/ 5")
        lbl_sobre.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_sobre.setStyleSheet(
            "color: #9CA3AF; font-size: 12px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent;"
        )
        col_derecha.addWidget(lbl_num)
        col_derecha.addWidget(lbl_sobre)
        col_derecha.addStretch()

        if resena.get("usuario_id") == self.usuario_id:
            btn_editar = QPushButton("  Editar")
            btn_editar.setFixedHeight(30)
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.setStyleSheet(STYLE_BTN_EDITAR)
            btn_editar.setIcon(QIcon(self._pixmap_from_svg(SVG_EDIT, 14)))
            btn_editar.clicked.connect(
                lambda _, r=resena: self._abrir_form_editar(r)
            )
            col_derecha.addWidget(btn_editar)

            btn_eliminar = QPushButton("  Eliminar")
            btn_eliminar.setFixedHeight(30)
            btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_eliminar.setStyleSheet(STYLE_BTN_ELIMINAR)
            btn_eliminar.setIcon(QIcon(self._pixmap_from_svg(SVG_TRASH, 14)))
            btn_eliminar.clicked.connect(
                lambda _, r=resena: self._eliminar_resena(r)
            )
            col_derecha.addWidget(btn_eliminar)

        layout_tarjeta.addLayout(col_derecha, stretch=1)
        return tarjeta


    def _abrir_form_agregar(self):
        from FormAgregaryEditar import FormAgregaryEditar
        self.form_ae = FormAgregaryEditar(
            pelicula_id     = self.pelicula_id,
            usuario_id      = self.usuario_id,
            clase_resena    = self.clase_resena,
            titulo_pelicula = self.titulo_pelicula,
            resena          = None,
            callback        = self._cargar_resenas
        )
        self.form_ae.show()

    def _abrir_form_editar(self, resena: dict):
        from FormAgregaryEditar import FormAgregaryEditar
        self.form_ae = FormAgregaryEditar(
            pelicula_id     = self.pelicula_id,
            usuario_id      = self.usuario_id,
            clase_resena    = self.clase_resena,
            titulo_pelicula = self.titulo_pelicula,
            resena          = resena,
            callback        = self._cargar_resenas
        )
        self.form_ae.show()

    def _eliminar_resena(self, resena: dict):
        from PyQt6.QtWidgets import QMessageBox

        confirmacion = QMessageBox.question(
            self,
            "Eliminar reseña",
            "¿Estás seguro de que quieres eliminar esta reseña?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            resultado = self.clase_resena.eliminar_resena(
                resena_id  = resena["id"],
                usuario_id = self.usuario_id
            )
            if resultado["exito"]:
                self._cargar_resenas()
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Error")
                msg.setText(resultado["mensaje"])
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStyleSheet(STYLE_MSGBOX)
                msg.exec()