import math
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QSize
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QBrush, QIcon, QPixmap
from PyQt6.QtSvg import QSvgRenderer




from PyQt6.QtWidgets import QApplication

def _svg_pixmap_at_scale(svg_str: str, size: int, scale: int) -> QPixmap:
    physical = size * scale
    renderer = QSvgRenderer(svg_str.encode("utf-8"))
    px = QPixmap(physical, physical)
    px.fill(Qt.GlobalColor.transparent)
    painter = QPainter(px)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    px.setDevicePixelRatio(float(scale))
    return px


def _svg_pixmap(svg_str: str, size: int = 18) -> QPixmap:
    app = QApplication.instance()
    dpr = app.devicePixelRatio() if app else 1.0
    physical = int(size * dpr)
    renderer = QSvgRenderer(svg_str.encode("utf-8"))
    px = QPixmap(physical, physical)
    px.fill(Qt.GlobalColor.transparent)
    painter = QPainter(px)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    px.setDevicePixelRatio(dpr)
    return px


def _svg_icon(svg_str: str, size: int = 18) -> QIcon:
    icon = QIcon()
    icon.addPixmap(_svg_pixmap_at_scale(svg_str, size, 1), QIcon.Mode.Normal, QIcon.State.Off)
    icon.addPixmap(_svg_pixmap_at_scale(svg_str, size, 2), QIcon.Mode.Normal, QIcon.State.Off)
    return icon



# ICONOS SVG INLINE


# Botón "Analizar con IA" — estrella / chispa de IA
SVG_SPARKLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 2l2.4 7.2H22l-6.2 4.5 2.4 7.3L12 17l-6.2 4 2.4-7.3L2 9.2h7.6L12 2z"/>
</svg>"""

# Botón "Guardar reseña" — check / disco
SVG_SAVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#111827" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
  <polyline points="17 21 17 13 7 13 7 21"/>
  <polyline points="7 3 7 8 15 8"/>
</svg>"""

# Label "Idioma:" — globo
SVG_GLOBE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="2" y1="12" x2="22" y2="12"/>
  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10
           15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
</svg>"""

# Encabezado card formulario — lápiz
SVG_EDIT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
</svg>"""

# Encabezado card resultados — cerebro / chip IA
SVG_AI = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="7" width="20" height="10" rx="3"/>
  <line x1="6" y1="7" x2="6" y2="3"/><line x1="10" y1="7" x2="10" y2="3"/>
  <line x1="14" y1="7" x2="14" y2="3"/><line x1="18" y1="7" x2="18" y2="3"/>
  <line x1="6" y1="17" x2="6" y2="21"/><line x1="10" y1="17" x2="10" y2="21"/>
  <line x1="14" y1="17" x2="14" y2="21"/><line x1="18" y1="17" x2="18" y2="21"/>
</svg>"""

# Campo película — clapperboard
SVG_FILM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
  <line x1="7" y1="2" x2="7" y2="22"/>
  <line x1="17" y1="2" x2="17" y2="22"/>
  <line x1="2" y1="12" x2="22" y2="12"/>
  <line x1="2" y1="7" x2="7" y2="7"/>
  <line x1="17" y1="7" x2="22" y2="7"/>
  <line x1="17" y1="17" x2="22" y2="17"/>
  <line x1="2" y1="17" x2="7" y2="17"/>
</svg>"""

# Estado "Analizando..." — spinner (reloj)
SVG_CLOCK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>"""

# Estado "Error" — alerta
SVG_ALERT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="8" x2="12" y2="12"/>
  <line x1="12" y1="16" x2="12.01" y2="16"/>
</svg>"""

# Estado "Pendiente" — reloj de arena
SVG_PENDING = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M5 3h14M5 21h14"/>
  <path d="M6 3v5l6 4-6 4v5M18 3v5l-6 4 6 4v5"/>
</svg>"""

# Tag / chip de etiqueta — precio/tag
SVG_TAG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
  <line x1="7" y1="7" x2="7.01" y2="7"/>
</svg>"""


# ─────────────────────────────────────────────────────────────
# HILO PARA NO BLOQUEAR LA UI MIENTRAS LA IA ANALIZA
# ─────────────────────────────────────────────────────────────

class HiloAnalisis(QThread):
    resultado_listo = pyqtSignal(dict)

    def __init__(self, clase_resena, datos):
        super().__init__()
        self.clase_resena = clase_resena
        self.datos        = datos

    def run(self):
        if self.datos.get("es_edicion"):
            resultado = self.clase_resena.editar_resena(
                resena_id   = self.datos["resena_id"],
                usuario_id  = self.datos["usuario_id"],
                nuevo_texto = self.datos["texto"],
                idioma      = self.datos["idioma"]
            )
        else:
            resultado = self.clase_resena.procesar_resena(
                usuario_id      = self.datos["usuario_id"],
                titulo_pelicula = self.datos["titulo_pelicula"],
                texto           = self.datos["texto"],
                idioma          = self.datos["idioma"]
            )
        self.resultado_listo.emit(resultado)



class CircularScore(QWidget):
    """Dibuja un arco de progreso con el número de puntuación en el centro."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._valor  = None
        self._maximo = 5.0
        self.setFixedSize(120, 120)
        self.setStyleSheet("background: transparent;")

    def set_valor(self, valor):
        try:
            self._valor = float(valor)
        except (TypeError, ValueError):
            self._valor = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width() / 2, self.height() / 2
        radio  = 44
        grosor = 8
        rect   = QRectF(cx - radio, cy - radio, radio * 2, radio * 2)

        # Círculo de fondo
        pen_bg = QPen(QColor("#E5E7EB"))
        pen_bg.setWidth(grosor)
        pen_bg.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_bg)
        painter.drawEllipse(rect)

        if self._valor is not None:
            progreso = min(self._valor, self._maximo) / self._maximo
            span     = int(-progreso * 360 * 16)

            if self._valor >= 4.0:
                color = "#22C55E"
            elif self._valor >= 2.5:
                color = "#F59E0B"
            else:
                color = "#EF4444"

            pen_arc = QPen(QColor(color))
            pen_arc.setWidth(grosor)
            pen_arc.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen_arc)
            painter.drawArc(rect, 90 * 16, span)

            painter.setPen(QColor("#111827"))
            fuente = QFont("Segoe UI", 18, QFont.Weight.Bold)
            painter.setFont(fuente)
            texto = (str(self._valor)
                     if self._valor != int(self._valor)
                     else str(int(self._valor)))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, texto)
        else:
            painter.setPen(QColor("#D1D5DB"))
            fuente = QFont("Segoe UI", 14)
            painter.setFont(fuente)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "—")

        painter.end()



class LanguageSwitch(QWidget):
    """Toggle compacto ES ↔ EN con estética coherente."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._idioma = "es"
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.lbl_es = QLabel("ES")
        self.btn    = QPushButton()
        self.btn.setFixedSize(44, 22)
        self.btn.setCheckable(True)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setToolTip("Cambiar idioma de análisis")
        self.btn.clicked.connect(self._toggle)
        self.lbl_en = QLabel("EN")

        for lbl in (self.lbl_es, self.lbl_en):
            lbl.setStyleSheet(
                "font-family: 'Segoe UI', sans-serif; font-size: 11px;"
                "font-weight: 600; background: transparent;"
            )

        layout.addWidget(self.lbl_es)
        layout.addWidget(self.btn)
        layout.addWidget(self.lbl_en)
        self._actualizar_estilo()

    def _toggle(self):
        self._idioma = "en" if self._idioma == "es" else "es"
        self._actualizar_estilo()

    def _actualizar_estilo(self):
        es_activo = self._idioma == "es"
        self.lbl_es.setStyleSheet(
            "font-family: 'Segoe UI', sans-serif; font-size: 11px;"
            f"font-weight: {'700' if es_activo else '400'};"
            f"color: {'#111827' if es_activo else '#9CA3AF'}; background: transparent;"
        )
        self.lbl_en.setStyleSheet(
            "font-family: 'Segoe UI', sans-serif; font-size: 11px;"
            f"font-weight: {'700' if not es_activo else '400'};"
            f"color: {'#111827' if not es_activo else '#9CA3AF'}; background: transparent;"
        )
        self.btn.setChecked(not es_activo)
        bg = "#111827" if not es_activo else "#E5E7EB"
        self.btn.setStyleSheet(f"""
            QPushButton {{
                border-radius: 11px;
                background-color: {bg};
                border: none;
            }}
        """)

    @property
    def idioma(self) -> str:
        return self._idioma



STYLE_MAIN = """
    QWidget {
        background-color: #F7F8FA;
        font-family: 'Segoe UI', sans-serif;
    }
"""
STYLE_CARD = """
    QFrame#card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
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
STYLE_SECCION_SUB = """
    QLabel {
        color: #9CA3AF;
        font-size: 12px;
        font-weight: 400;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
    }
"""
STYLE_LABEL_SECTION = """
    QLabel {
        color: #6B7280;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.9px;
        background: transparent;
    }
"""
STYLE_INPUT_READONLY = """
    QLineEdit {
        background-color: #F9FAFB;
        border: 1.5px solid #E5E7EB;
        border-radius: 10px;
        padding: 10px 14px 10px 38px;
        font-size: 13px;
        color: #6B7280;
        font-family: 'Segoe UI', sans-serif;
    }
"""
STYLE_TEXTAREA = """
    QTextEdit {
        background-color: #FFFFFF;
        border: 1.5px solid #E5E7EB;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        color: #111827;
        font-family: 'Segoe UI', sans-serif;
        selection-background-color: #3B82F6;
    }
    QTextEdit:focus {
        border: 1.5px solid #3B82F6;
    }
    QTextEdit:hover {
        border: 1.5px solid #D1D5DB;
    }
"""
STYLE_BTN_ANALIZAR = """
    QPushButton {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }
    QPushButton:hover  { background-color: #1F2937; }
    QPushButton:pressed { background-color: #374151; }
    QPushButton:disabled {
        background-color: #E5E7EB;
        color: #9CA3AF;
    }
"""
STYLE_BTN_GUARDAR = """
    QPushButton {
        background-color: #FFFFFF;
        color: #111827;
        border: 1.5px solid #E5E7EB;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover  { background-color: #F9FAFB; border-color: #D1D5DB; }
    QPushButton:pressed { background-color: #F3F4F6; }
    QPushButton:disabled {
        background-color: #F9FAFB;
        color: #D1D5DB;
        border-color: #F3F4F6;
    }
"""
STYLE_ETIQUETA_CHIP = """
    QLabel {
        background-color: #F3F4F6;
        color: #374151;
        border-radius: 6px;
        padding: 4px 10px 4px 6px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }
"""
STYLE_ESTADO_LABEL = """
    QLabel {
        color: #9CA3AF;
        font-size: 12px;
        font-family: 'Segoe UI', sans-serif;
        background: transparent;
    }
"""
STYLE_DIVIDER_V = """
    QFrame {
        background-color: #E5E7EB;
        border: none;
        max-width: 1px;
    }
"""



def _lbl_con_icono(svg: str, texto: str, svg_size: int = 14) -> QWidget:
    """Devuelve un QWidget horizontal con ícono SVG + texto."""
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    lay = QHBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)

    icono = QLabel()
    icono.setPixmap(_svg_pixmap(svg, svg_size))
    icono.setFixedSize(svg_size, svg_size)
    icono.setStyleSheet("background: transparent;")

    lbl = QLabel(texto)
    lbl.setStyleSheet(STYLE_ESTADO_LABEL)

    lay.addWidget(icono)
    lay.addWidget(lbl)
    lay.addStretch()
    return w


def _campo_con_icono(svg: str, svg_size: int = 15) -> QWidget:
    """
    Devuelve un QWidget que superpone un ícono SVG
    a la izquierda de un QLineEdit de solo lectura.
    Expone .line_edit para leer/escribir el valor.
    """
    wrap = QWidget()
    wrap.setStyleSheet("background: transparent;")
    wrap.setFixedHeight(42)

    # El QLineEdit ocupa todo el ancho del contenedor
    le = QLineEdit(wrap)
    le.setReadOnly(True)
    le.setStyleSheet(STYLE_INPUT_READONLY)
    le.setFixedHeight(42)

    # Ícono flotante, transparente a eventos de ratón
    ico = QLabel(wrap)
    ico.setPixmap(_svg_pixmap(svg, svg_size))
    ico.setFixedSize(svg_size, svg_size)
    ico.move(12, (42 - svg_size) // 2)
    ico.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    ico.setStyleSheet("background: transparent;")
    ico.raise_()

    wrap.line_edit = le  # acceso público

    # Ajustar ancho cuando el contenedor cambia de tamaño
    original_resize = wrap.resizeEvent
    def _on_resize(e):
        le.setFixedWidth(wrap.width())
        if callable(original_resize):
            original_resize(e)
    wrap.resizeEvent = _on_resize

    return wrap

class FormAgregaryEditar(QWidget):

    def __init__(self, pelicula_id: int, usuario_id: int,
                 clase_resena, titulo_pelicula: str,
                 resena: dict = None, callback=None):
        super().__init__()
        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_resena    = clase_resena
        self.titulo_pelicula = titulo_pelicula
        self.resena          = resena
        self.callback        = callback
        self.es_edicion      = resena is not None

        self._configurar_ventana()
        self._construir_ui()

        if self.es_edicion:
            self._precargar_texto()

    # ── CONFIGURACIÓN DE VENTANA 
    def _configurar_ventana(self):
        self.setWindowTitle("Editar reseña" if self.es_edicion else "Agregar reseña")
        self.setFixedSize(780, 480)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setStyleSheet(STYLE_MAIN)

    # ── CONSTRUCCIÓN DE LA UI 

    def _construir_ui(self):
        raiz = QHBoxLayout(self)
        raiz.setContentsMargins(20, 20, 20, 20)
        raiz.setSpacing(16)
        raiz.addWidget(self._card_formulario(), stretch=3)
        raiz.addWidget(self._card_resultados(), stretch=2)

    # ── CARD IZQUIERDA: FORMULARIO 

    def _card_formulario(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(STYLE_CARD)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(0)

        # Encabezado con ícono SVG
        fila_titulo = QHBoxLayout()
        fila_titulo.setSpacing(8)
        fila_titulo.setContentsMargins(0, 0, 0, 0)

        ico_header = QLabel()
        ico_header.setPixmap(_svg_pixmap(SVG_EDIT, 16))
        ico_header.setFixedSize(16, 16)
        ico_header.setStyleSheet("background: transparent;")

        lbl_titulo = QLabel("Escribir reseña")
        lbl_titulo.setStyleSheet(STYLE_SECCION_TITULO)

        fila_titulo.addWidget(ico_header)
        fila_titulo.addWidget(lbl_titulo)
        fila_titulo.addStretch()

        lbl_sub = QLabel(
            "Paso 1: Edita tu opinión" if self.es_edicion else "Paso 1: Tu opinión"
        )
        lbl_sub.setStyleSheet(STYLE_SECCION_SUB)

        layout.addLayout(fila_titulo)
        layout.addWidget(lbl_sub)
        layout.addSpacing(18)

        # Label película
        lbl_pelicula = QLabel("PELÍCULA")
        lbl_pelicula.setStyleSheet(STYLE_LABEL_SECTION)
        layout.addWidget(lbl_pelicula)
        layout.addSpacing(6)

        # Campo película con ícono clapperboard superpuesto
        self._wrap_pelicula = _campo_con_icono(SVG_FILM, svg_size=14)
        self._wrap_pelicula.line_edit.setText(self.titulo_pelicula)
        self._wrap_pelicula.line_edit.setPlaceholderText("Nombre película")
        # Alias para compatibilidad con código externo que pudiera usar campo_pelicula
        self.campo_pelicula = self._wrap_pelicula.line_edit
        layout.addWidget(self._wrap_pelicula)
        layout.addSpacing(14)

        # Label reseña
        lbl_resena = QLabel("TU RESEÑA")
        lbl_resena.setStyleSheet(STYLE_LABEL_SECTION)
        layout.addWidget(lbl_resena)
        layout.addSpacing(6)

        self.campo_resena = QTextEdit()
        self.campo_resena.setPlaceholderText("Escribe tu opinión sobre la película...")
        self.campo_resena.setStyleSheet(STYLE_TEXTAREA)
        self.campo_resena.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.campo_resena, stretch=1)
        layout.addSpacing(12)

        # Fila inferior: ícono globo + switch idioma + botón analizar
        fila_bottom = QHBoxLayout()
        fila_bottom.setSpacing(8)
        fila_bottom.setContentsMargins(0, 0, 0, 0)

        # Ícono globo (idioma) con SVG
        ico_globe = QLabel()
        ico_globe.setPixmap(_svg_pixmap(SVG_GLOBE, 14))
        ico_globe.setFixedSize(14, 14)
        ico_globe.setStyleSheet("background: transparent;")

        lbl_idioma = QLabel("Idioma:")
        lbl_idioma.setStyleSheet(STYLE_ESTADO_LABEL)

        self.switch_idioma = LanguageSwitch()

        fila_bottom.addWidget(ico_globe)
        fila_bottom.addWidget(lbl_idioma)
        fila_bottom.addWidget(self.switch_idioma)
        fila_bottom.addStretch()

        # Botón "Analizar con IA" con ícono SVG estrella
        self.btn_analizar = QPushButton("  Analizar con IA")
        self.btn_analizar.setFixedHeight(44)
        self.btn_analizar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_analizar.setIcon(_svg_icon(SVG_SPARKLE, 15))
        self.btn_analizar.setIconSize(QSize(15, 15))
        self.btn_analizar.setStyleSheet(STYLE_BTN_ANALIZAR)
        self.btn_analizar.clicked.connect(self._guardar)

        fila_bottom.addWidget(self.btn_analizar)
        layout.addLayout(fila_bottom)

        return card

    # ── CARD DERECHA: RESULTADOS ─────────────────────────────

    def _card_resultados(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(STYLE_CARD)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(0)

        # Encabezado con ícono SVG chip/IA
        fila_titulo = QHBoxLayout()
        fila_titulo.setSpacing(8)
        fila_titulo.setContentsMargins(0, 0, 0, 0)

        ico_header = QLabel()
        ico_header.setPixmap(_svg_pixmap(SVG_AI, 16))
        ico_header.setFixedSize(16, 16)
        ico_header.setStyleSheet("background: transparent;")

        lbl_titulo = QLabel("Resultados IA")
        lbl_titulo.setStyleSheet(STYLE_SECCION_TITULO)

        fila_titulo.addWidget(ico_header)
        fila_titulo.addWidget(lbl_titulo)
        fila_titulo.addStretch()

        lbl_sub = QLabel("Paso 2: Análisis automático")
        lbl_sub.setStyleSheet(STYLE_SECCION_SUB)

        layout.addLayout(fila_titulo)
        layout.addWidget(lbl_sub)
        layout.addSpacing(20)

        # Label puntuación
        lbl_puntuacion = QLabel("PUNTUACIÓN IA")
        lbl_puntuacion.setStyleSheet(STYLE_LABEL_SECTION)
        lbl_puntuacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_puntuacion)
        layout.addSpacing(10)

        # Círculo de puntuación
        self.circulo = CircularScore()
        layout.addWidget(self.circulo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(18)

        # Label etiquetas
        lbl_etiq_titulo = QLabel("ETIQUETAS DETECTADAS")
        lbl_etiq_titulo.setStyleSheet(STYLE_LABEL_SECTION)
        lbl_etiq_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_etiq_titulo)
        layout.addSpacing(8)

        # Estado pendiente con ícono reloj de arena
        self._fila_estado = QHBoxLayout()
        self._fila_estado.setSpacing(6)
        self._fila_estado.setContentsMargins(0, 0, 0, 0)
        self._fila_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ico_estado = QLabel()
        self.ico_estado.setPixmap(_svg_pixmap(SVG_PENDING, 13))
        self.ico_estado.setFixedSize(13, 13)
        self.ico_estado.setStyleSheet("background: transparent;")

        self.lbl_estado = QLabel("Pendiente de análisis")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_estado.setStyleSheet(STYLE_ESTADO_LABEL)

        self._fila_estado.addWidget(self.ico_estado)
        self._fila_estado.addWidget(self.lbl_estado)

        estado_wrap = QWidget()
        estado_wrap.setStyleSheet("background: transparent;")
        estado_wrap.setLayout(self._fila_estado)
        layout.addWidget(estado_wrap, alignment=Qt.AlignmentFlag.AlignCenter)

        # Contenedor chips
        self.widget_chips = QWidget()
        self.widget_chips.setStyleSheet("background: transparent;")
        self.layout_chips = QHBoxLayout(self.widget_chips)
        self.layout_chips.setContentsMargins(0, 0, 0, 0)
        self.layout_chips.setSpacing(6)
        self.layout_chips.addStretch()
        layout.addWidget(self.widget_chips, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        # Botón guardar con ícono SVG disco/save
        self.btn_cerrar = QPushButton("  Guardar reseña")
        self.btn_cerrar.setFixedHeight(44)
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.setEnabled(False)
        self.btn_cerrar.setIcon(_svg_icon(SVG_SAVE, 15))
        self.btn_cerrar.setIconSize(QSize(15, 15))
        self.btn_cerrar.setStyleSheet(STYLE_BTN_GUARDAR)
        self.btn_cerrar.clicked.connect(self._cerrar)
        layout.addWidget(self.btn_cerrar)

        return card

    # ── PRECARGA EN MODO EDICIÓN ─────────────────────────────

    def _precargar_texto(self):
        self.campo_resena.setPlainText(self.resena.get("texto", ""))

    # ── GUARDAR / ANALIZAR ───────────────────────────────────

    def _guardar(self):
        texto = self.campo_resena.toPlainText().strip()
        if not texto:
            self.ico_estado.setPixmap(_svg_pixmap(SVG_ALERT, 13))
            self.lbl_estado.setText("Escribe una reseña primero.")
            self.lbl_estado.setStyleSheet(
                "color: #EF4444; font-size: 12px;"
                "font-family: 'Segoe UI'; background: transparent;"
            )
            return

        self.btn_analizar.setEnabled(False)
        self.campo_resena.setReadOnly(True)
        self.switch_idioma.btn.setEnabled(False)

        # Estado "Analizando..." con ícono reloj
        self.ico_estado.setPixmap(_svg_pixmap(SVG_CLOCK, 13))
        self.lbl_estado.setText("Analizando...")
        self.lbl_estado.setStyleSheet(STYLE_ESTADO_LABEL)
        self.lbl_estado.show()
        self.ico_estado.show()

        self._limpiar_chips()
        self.circulo.set_valor(None)

        datos = {
            "es_edicion"     : self.es_edicion,
            "usuario_id"     : self.usuario_id,
            "titulo_pelicula": self.titulo_pelicula,
            "texto"          : texto,
            "resena_id"      : self.resena["id"] if self.es_edicion else None,
            "idioma"         : self.switch_idioma.idioma,
        }
        self.hilo = HiloAnalisis(self.clase_resena, datos)
        self.hilo.resultado_listo.connect(self._mostrar_resultados)
        self.hilo.start()

    # ── MOSTRAR RESULTADOS ───────────────────────────────────

    def _mostrar_resultados(self, resultado: dict):
        self.switch_idioma.btn.setEnabled(True)

        if not resultado.get("exito"):
            self.ico_estado.setPixmap(_svg_pixmap(SVG_ALERT, 13))
            self.lbl_estado.setText(resultado.get("mensaje", "Error desconocido"))
            self.lbl_estado.setStyleSheet(
                "color: #EF4444; font-size: 12px;"
                "font-family: 'Segoe UI'; background: transparent;"
            )
            self.btn_analizar.setEnabled(True)
            self.campo_resena.setReadOnly(False)
            return

        # Puntuación
        self.circulo.set_valor(resultado.get("valoracion"))

        # Ocultar estado y mostrar chips
        self.lbl_estado.hide()
        self.ico_estado.hide()
        self._limpiar_chips()

        for etiqueta in resultado.get("etiquetas", []):
            # Chip con ícono tag + texto
            chip_w = QWidget()
            chip_w.setStyleSheet(
                "background-color: #F3F4F6; border-radius: 6px;"
            )
            chip_lay = QHBoxLayout(chip_w)
            chip_lay.setContentsMargins(6, 4, 10, 4)
            chip_lay.setSpacing(5)

            ico_tag = QLabel()
            ico_tag.setPixmap(_svg_pixmap(SVG_TAG, 10))
            ico_tag.setFixedSize(10, 10)
            ico_tag.setStyleSheet("background: transparent;")

            lbl_chip = QLabel(etiqueta)
            lbl_chip.setStyleSheet(
                "background: transparent; color: #374151;"
                "font-size: 11px; font-weight: 600;"
                "font-family: 'Segoe UI', sans-serif;"
            )

            chip_lay.addWidget(ico_tag)
            chip_lay.addWidget(lbl_chip)

            # Insertar antes del stretch final
            self.layout_chips.insertWidget(self.layout_chips.count() - 1, chip_w)

        self.btn_cerrar.setEnabled(True)
        self.btn_analizar.setEnabled(False)

    #CERRAR

    def _cerrar(self):
        if self.callback:
            self.callback()
        self.close()

    #LIMPIAR CHIPS 

    def _limpiar_chips(self):
        while self.layout_chips.count() > 1:   # conservar stretch final
            item = self.layout_chips.takeAt(0)
            if item.widget():
                item.widget().deleteLater()