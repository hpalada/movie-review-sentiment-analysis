# FormReseñas.py
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QPushButton, QFrame, QSizePolicy,
    QGraphicsDropShadowEffect, QDialog
)
from PyQt6.QtCore import Qt, QByteArray, QSize
from PyQt6.QtGui import QPixmap, QColor, QFont, QIcon, QPainter
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtSvg import QSvgRenderer
from ClaseReseña import Resena
from Json import JsonManager
from rutas import ruta_imagen

# ══════════════════════════════════════════════════════════════════════════════
#  THEME — siempre importado desde Catalogo para compartir el mismo _mode
# ══════════════════════════════════════════════════════════════════════════════
try:
    from catalogoPrincipal import Theme
    _HAS_THEME = True
except ImportError:
    _HAS_THEME = False

    class Theme:
        """Fallback solo para ejecución standalone de FormReseñas."""
        _mode = "light"

        LIGHT = {
            "bg_app": "#F7F8FA", "bg_card": "#FFFFFF",
            "border_main": "#E5E7EB", "border_card": "#E5E7EB",
            "text_primary": "#111827", "text_secondary": "#6B7280",
            "text_muted": "#9CA3AF", "accent_btn": "#111827",
            "accent_btn_h": "#1F2937", "accent_btn_p": "#374151",
            "accent_del": "#EF4444", "accent_del_bg": "#FEF2F2",
            "accent_del_border": "#FCA5A5", "bg_hover": "#F3F4F6",
            "bg_avatar": "#EEF2FF", "text_avatar": "#4F46E5",
            "icon_edit": "#6B7280", "icon_trash": "#EF4444",
        }
        DARK = {
            "bg_app": "#0D1117", "bg_card": "#1C2128",
            "border_main": "#30363D", "border_card": "#30363D",
            "text_primary": "#E6EDF3", "text_secondary": "#8B949E",
            "text_muted": "#6E7681", "accent_btn": "#238636",
            "accent_btn_h": "#2EA043", "accent_btn_p": "#196C2E",
            "accent_del": "#F85149", "accent_del_bg": "#1C0B0B",
            "accent_del_border": "#6E1010", "bg_hover": "#21262D",
            "bg_avatar": "#1F2D45", "text_avatar": "#79C0FF",
            "icon_edit": "#8B949E", "icon_trash": "#F85149",
        }

        @classmethod
        def get(cls, key: str) -> str:
            p = cls.DARK if cls._mode == "dark" else cls.LIGHT
            return p.get(key, "#000000")

        @classmethod
        def is_dark(cls) -> bool:
            return cls._mode == "dark"

        @classmethod
        def toggle(cls):
            cls._mode = "dark" if cls._mode == "light" else "light"


# ══════════════════════════════════════════════════════════════════════════════
#  SVG HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _make_svg_pixmap(svg_bytes: bytes, size: int) -> QPixmap:
    renderer = QSvgRenderer(QByteArray(svg_bytes))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def _svg_widget(svg_bytes: bytes, size: int) -> QSvgWidget:
    w = QSvgWidget()
    w.load(QByteArray(svg_bytes))
    w.setFixedSize(size, size)
    w.setStyleSheet("background: transparent;")
    return w


# ══════════════════════════════════════════════════════════════════════════════
#  SVG ESTÁTICOS
# ══════════════════════════════════════════════════════════════════════════════

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

SVG_STAR_BIG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#F59E0B" d="M12 2l3.09 6.26L22 9.27l-5 4.87
    1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>"""

SVG_PLUS = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="#FFFFFF" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
  <line x1="12" y1="5" x2="12" y2="19"/>
  <line x1="5" y1="12" x2="19" y2="12"/>
</svg>"""


# ══════════════════════════════════════════════════════════════════════════════
#  SVG DINÁMICOS — leen Theme.get() en el momento de llamarse
# ══════════════════════════════════════════════════════════════════════════════

def _svg_back_bytes() -> bytes:
    c = Theme.get("text_secondary")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="{c}" stroke-width="2.5"
     stroke-linecap="round" stroke-linejoin="round">
  <polyline points="15 18 9 12 15 6"/>
</svg>""".encode()


def _svg_edit_themed() -> bytes:
    c = Theme.get("icon_edit")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="{c}" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14 a2 2 0 0 0 2-2v-7"/>
  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3 L12 15l-4 1 1-4 9.5-9.5z"/>
</svg>""".encode()


def _svg_trash_themed() -> bytes:
    c = Theme.get("icon_trash")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     fill="none" stroke="{c}" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 6 5 6 21 6"/>
  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8 a2 2 0 0 1-2-2L5 6"/>
  <path d="M10 11v6"/><path d="M14 11v6"/>
  <path d="M9 6V4a1 1 0 0 1 1-1h4 a1 1 0 0 1 1 1v2"/>
</svg>""".encode()


# ══════════════════════════════════════════════════════════════════════════════
#  DIÁLOGO CUSTOM (reemplaza QMessageBox — sin barra del sistema)
# ══════════════════════════════════════════════════════════════════════════════

class _CustomDialog(QDialog):
    """
    Ventana emergente personalizada sin barra de título del sistema operativo.
    Muestra texto y uno o dos botones. Devuelve True si el usuario confirmó.
    """
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
        card.setStyleSheet(f"""
            QFrame#dlgCard {{
                background-color: {Theme.get('bg_card')};
                border-radius: 14px;
                border: 1px solid {Theme.get('border_main')};
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 24, 28, 20)
        lay.setSpacing(0)

        # Título
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(f"""
            color: {Theme.get('text_primary')};
            font-size: 15px; font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        """)
        lay.addWidget(lbl_titulo)
        lay.addSpacing(10)

        # Mensaje
        lbl_msg = QLabel(mensaje)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet(f"""
            color: {Theme.get('text_secondary')};
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        """)
        lay.addWidget(lbl_msg)
        lay.addSpacing(22)

        # Botones
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        if btn_cancel:
            b_cancel = QPushButton(btn_cancel)
            b_cancel.setFixedHeight(38)
            b_cancel.setMinimumWidth(100)
            b_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
            b_cancel.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {Theme.get('text_secondary')};
                    border: 1.5px solid {Theme.get('border_card')};
                    border-radius: 8px; padding: 0 18px;
                    font-size: 13px; font-weight: 600;
                    font-family: 'Segoe UI', sans-serif;
                }}
                QPushButton:hover {{
                    background-color: {Theme.get('bg_hover')};
                    border-color: {Theme.get('border_main')};
                    color: {Theme.get('text_primary')};
                }}
            """)
            b_cancel.clicked.connect(self.reject)
            btn_row.addWidget(b_cancel)

        b_ok = QPushButton(btn_ok)
        b_ok.setFixedHeight(38)
        b_ok.setMinimumWidth(100)
        b_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        b_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.get('accent_btn')};
                color: #FFFFFF; border: none; border-radius: 8px;
                padding: 0 18px; font-size: 13px; font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{ background-color: {Theme.get('accent_btn_h')}; }}
            QPushButton:pressed {{ background-color: {Theme.get('accent_btn_p')}; }}
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


# ══════════════════════════════════════════════════════════════════════════════
#  ESTILOS DINÁMICOS — todas leen Theme.get() en el momento de llamarse
# ══════════════════════════════════════════════════════════════════════════════

def S_MAIN():
    return f"QWidget {{ background-color: {Theme.get('bg_app')}; font-family: 'Segoe UI', sans-serif; }}"

def S_SCROLL():
    return f"""
    QScrollArea {{ border: none; background: transparent; }}
    QScrollBar:vertical {{ background: transparent; width: 5px; margin: 0px; }}
    QScrollBar::handle:vertical {{
        background: {Theme.get('border_main')}; border-radius: 3px; min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {Theme.get('text_muted')}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """

def S_CABECERA():
    return f"""
    QFrame#cabecera {{
        background-color: {Theme.get('bg_card')};
        border-bottom: 1px solid {Theme.get('border_main')};
    }}
    """

def S_POSTER():
    return f"""
    QLabel#poster {{
        background-color: {Theme.get('bg_app')};
        border: 2px dashed {Theme.get('border_main')};
        border-radius: 12px;
        color: {Theme.get('text_muted')};
        font-size: 12px;
    }}
    """

def S_POSTER_FILLED():
    return f"""
    QLabel#poster {{
        background-color: {Theme.get('bg_app')};
        border: 2px solid {Theme.get('border_card')};
        border-radius: 12px;
    }}
    """

def S_TITULO_PELICULA():
    return f"QLabel {{ color: {Theme.get('text_primary')}; font-size: 22px; font-weight: 700; font-family: 'Segoe UI', sans-serif; background: transparent; }}"

def S_SECCION_TITULO():
    return f"QLabel {{ color: {Theme.get('text_primary')}; font-size: 15px; font-weight: 700; font-family: 'Segoe UI', sans-serif; background: transparent; }}"

def S_TARJETA():
    return f"""
    QFrame#tarjeta {{
        background-color: {Theme.get('bg_card')};
        border: 1px solid {Theme.get('border_card')};
        border-radius: 14px;
    }}
    QFrame#tarjeta:hover {{
        border: 1px solid {Theme.get('border_main')};
    }}
    """

def S_USUARIO_LABEL():
    return f"QLabel {{ color: {Theme.get('text_primary')}; font-size: 13px; font-weight: 600; font-family: 'Segoe UI', sans-serif; background: transparent; }}"

def S_TEXTO_RESENA():
    return f"QLabel {{ color: {Theme.get('text_secondary')}; font-size: 12px; font-weight: 400; font-family: 'Segoe UI', sans-serif; background: transparent; line-height: 1.5; }}"

def S_LEER_MAS():
    return f"QLabel {{ color: {Theme.get('text_muted')}; font-size: 11px; font-weight: 500; font-family: 'Segoe UI', sans-serif; background: transparent; text-decoration: underline; }}"

def S_ETIQUETA_CHIP():
    return f"QLabel {{ background-color: {Theme.get('bg_hover')}; color: {Theme.get('text_secondary')}; border-radius: 6px; padding: 3px 10px; font-size: 11px; font-weight: 600; font-family: 'Segoe UI', sans-serif; letter-spacing: 0.3px; }}"

def S_BTN_AGREGAR():
    return f"""
    QPushButton {{
        background-color: {Theme.get('accent_btn')};
        color: #FFFFFF; border: none; border-radius: 0px;
        font-size: 13px; font-weight: 600;
        font-family: 'Segoe UI', sans-serif; letter-spacing: 0.5px;
    }}
    QPushButton:hover {{ background-color: {Theme.get('accent_btn_h')}; }}
    QPushButton:pressed {{ background-color: {Theme.get('accent_btn_p')}; }}
    """

def S_BTN_EDITAR():
    return f"""
    QPushButton {{
        background-color: transparent;
        color: {Theme.get('text_secondary')};
        border: 1.5px solid {Theme.get('border_card')};
        border-radius: 7px; padding: 4px 12px;
        font-size: 11px; font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }}
    QPushButton:hover {{
        background-color: {Theme.get('bg_hover')};
        border-color: {Theme.get('border_main')};
        color: {Theme.get('text_primary')};
    }}
    """

def S_BTN_ELIMINAR():
    return f"""
    QPushButton {{
        background-color: transparent;
        color: {Theme.get('accent_del')};
        border: 1.5px solid {Theme.get('accent_del_border')};
        border-radius: 7px; padding: 4px 12px;
        font-size: 11px; font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }}
    QPushButton:hover {{
        background-color: {Theme.get('accent_del_bg')};
        border-color: {Theme.get('accent_del')};
    }}
    """

def S_BTN_REGRESAR():
    return f"""
    QPushButton {{
        background-color: transparent;
        color: {Theme.get('text_secondary')};
        border: 1.5px solid {Theme.get('border_card')};
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 12px; font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }}
    QPushButton:hover {{
        background-color: {Theme.get('bg_hover')};
        border-color: {Theme.get('border_main')};
        color: {Theme.get('text_primary')};
    }}
    QPushButton:pressed {{
        background-color: {Theme.get('border_main')};
    }}
    """

def S_DIVIDER():
    return f"QFrame {{ background-color: {Theme.get('border_main')}; border: none; max-height: 1px; }}"

def S_AVATAR():
    return f"QLabel#avatar {{ background-color: {Theme.get('bg_avatar')}; color: {Theme.get('text_avatar')}; border-radius: 16px; font-size: 13px; font-weight: 700; font-family: 'Segoe UI', sans-serif; }}"

def S_NUM_GRANDE():
    return f"color: {Theme.get('text_primary')}; font-size: 22px; font-weight: 700; font-family: 'Segoe UI', sans-serif; background: transparent;"

def S_NUM_SOBRE():
    return f"color: {Theme.get('text_muted')}; font-size: 12px; font-family: 'Segoe UI', sans-serif; background: transparent;"

def S_PROMEDIO_NUM():
    return f"color: {Theme.get('text_primary')}; font-size: 28px; font-weight: 700; font-family: 'Segoe UI', sans-serif; background: transparent;"

def S_SOBRE_CINCO():
    return f"color: {Theme.get('text_muted')}; font-size: 16px; font-weight: 400; font-family: 'Segoe UI', sans-serif; background: transparent;"

def S_VACIO():
    return f"color: {Theme.get('text_muted')}; font-size: 13px; font-family: 'Segoe UI', sans-serif; background: transparent; padding: 40px 0px;"

def S_SCROLL_CONTENT():
    return f"background: {Theme.get('bg_app')};"


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS VISUALES
# ══════════════════════════════════════════════════════════════════════════════

def _estrellas_widget(valoracion, maximo: int = 5) -> QWidget:
    contenedor = QWidget()
    contenedor.setStyleSheet("background: transparent;")
    fila = QHBoxLayout(contenedor)
    fila.setContentsMargins(0, 0, 0, 0)
    fila.setSpacing(2)

    try:
        val = float(valoracion) if valoracion is not None else 0
    except (ValueError, TypeError):
        val = 0

    val_norm = min(val, maximo) / maximo * 5

    for i in range(5):
        if val_norm >= i + 1:
            star = _svg_widget(SVG_STAR_FILLED, 15)
        elif val_norm >= i + 0.5:
            star = _svg_widget(SVG_STAR_HALF, 15)
        else:
            star = _svg_widget(SVG_STAR_EMPTY, 15)
        fila.addWidget(star)

    fila.addStretch()
    return contenedor


def _sombra_tarjeta() -> QGraphicsDropShadowEffect:
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(18)
    s.setOffset(0, 3)
    alpha = 18 if not Theme.is_dark() else 60
    s.setColor(QColor(0, 0, 0, alpha))
    return s


# ══════════════════════════════════════════════════════════════════════════════
#  FORM PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class FormReseñas(QWidget):
    def __init__(self, pelicula_id, usuario_id, clase_pelicula,
                 clase_resena=None, titulo_pelicula="", pelicula_obj=None,
                 on_back=None):
        """
        on_back : callable opcional → se llama al pulsar "Regresar al catálogo".
                  Si no se pasa, el botón cierra la ventana (modo standalone).
        """
        super().__init__()
        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_pelicula  = clase_pelicula
        self.clase_resena    = Resena()
        self.titulo_pelicula = titulo_pelicula
        self.pelicula_obj    = pelicula_obj
        self.db              = JsonManager()
        self._on_back        = on_back

        usuario_actual = self.db.obtener_usuario_por_id(usuario_id)
        self.es_admin = (
            usuario_actual.get("rol", "").lower() == "admin"
            if usuario_actual else False
        )

        self.setWindowTitle("Reseñas")
        self.resize(1100, 750)
        self.setStyleSheet(S_MAIN())
        self._construir_ui()
        self._cargar_datos()

    # ── Construcción de UI ────────────────────────────────────────────────────

    def _construir_ui(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # Cabecera fija — SIN topbar duplicado, solo la cabecera con poster+info
        self.widget_cabecera = self._crear_cabecera()
        layout_raiz.addWidget(self.widget_cabecera)

        # Divisor
        self.div_cabecera = QFrame()
        self.div_cabecera.setFrameShape(QFrame.Shape.HLine)
        self.div_cabecera.setStyleSheet(S_DIVIDER())
        layout_raiz.addWidget(self.div_cabecera)

        # Área scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet(S_SCROLL())

        self.contenido_scroll = QWidget()
        self.contenido_scroll.setStyleSheet(S_SCROLL_CONTENT())
        self.layout_scroll = QVBoxLayout(self.contenido_scroll)
        self.layout_scroll.setContentsMargins(32, 24, 32, 24)
        self.layout_scroll.setSpacing(0)

        self.lbl_seccion = QLabel("Reseñas de usuarios")
        self.lbl_seccion.setStyleSheet(S_SECCION_TITULO())
        self.layout_scroll.addWidget(self.lbl_seccion)
        self.layout_scroll.addSpacing(16)

        self.layout_resenas = QVBoxLayout()
        self.layout_resenas.setSpacing(12)
        self.layout_scroll.addLayout(self.layout_resenas)
        self.layout_scroll.addStretch()

        self.scroll_area.setWidget(self.contenido_scroll)
        layout_raiz.addWidget(self.scroll_area, stretch=1)

        # Botón Agregar reseña (pie)
        self.btn_agregar = QPushButton("  Agregar reseña")
        self.btn_agregar.setFixedHeight(52)
        self.btn_agregar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_agregar.setStyleSheet(S_BTN_AGREGAR())
        self.btn_agregar.setIcon(QIcon(self._pixmap_from_svg(SVG_PLUS, 16)))
        self.btn_agregar.clicked.connect(self._abrir_form_agregar)
        layout_raiz.addWidget(self.btn_agregar)

    # ── Cabecera — altura aumentada para dar espacio a poster + estrellas ─────

    def _crear_cabecera(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("cabecera")
        frame.setStyleSheet(S_CABECERA())
        # Altura aumentada para que las estrellas no choquen con el poster
        frame.setFixedHeight(240)

        layout_raiz = QVBoxLayout(frame)
        layout_raiz.setContentsMargins(32, 14, 32, 16)
        layout_raiz.setSpacing(6)

        # ── Fila superior: btn regresar a la derecha ──────────────────────────
        fila_superior = QHBoxLayout()
        fila_superior.setContentsMargins(0, 0, 0, 0)
        fila_superior.setSpacing(0)
        fila_superior.addStretch()

        self.btn_regresar = QPushButton("  Regresar al catálogo")
        self.btn_regresar.setFixedHeight(32)
        self.btn_regresar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_regresar.setStyleSheet(S_BTN_REGRESAR())
        self.btn_regresar.setIcon(
            QIcon(self._pixmap_from_svg(_svg_back_bytes(), 14))
        )
        self.btn_regresar.setIconSize(QSize(14, 14))
        self.btn_regresar.clicked.connect(self._regresar)
        fila_superior.addWidget(self.btn_regresar)

        layout_raiz.addLayout(fila_superior)

        # ── Fila de contenido: poster + info ──────────────────────────────────
        fila_contenido = QHBoxLayout()
        fila_contenido.setContentsMargins(0, 0, 0, 0)
        fila_contenido.setSpacing(28)

        # Poster — tamaño fijo que no supere la cabecera
        self.lbl_poster = QLabel("POSTER")
        self.lbl_poster.setObjectName("poster")
        self.lbl_poster.setFixedSize(116, 155)   # más alto para que quepan las estrellas abajo
        self.lbl_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_poster.setStyleSheet(S_POSTER())
        fila_contenido.addWidget(
            self.lbl_poster, alignment=Qt.AlignmentFlag.AlignTop
        )

        # Columna de información
        layout_info = QVBoxLayout()
        layout_info.setSpacing(0)
        layout_info.setContentsMargins(0, 0, 0, 0)

        self.lbl_nombre = QLabel(self.titulo_pelicula or "Película")
        self.lbl_nombre.setStyleSheet(S_TITULO_PELICULA())
        layout_info.addWidget(self.lbl_nombre)
        layout_info.addSpacing(12)

        # Promedio
        fila_promedio = QHBoxLayout()
        fila_promedio.setSpacing(10)
        fila_promedio.setContentsMargins(0, 0, 0, 0)

        self.svg_estrella_grande = _svg_widget(SVG_STAR_BIG, 28)
        self.lbl_promedio_num = QLabel("—")
        self.lbl_promedio_num.setStyleSheet(S_PROMEDIO_NUM())
        self.lbl_sobre_cinco = QLabel("/ 5")
        self.lbl_sobre_cinco.setStyleSheet(S_SOBRE_CINCO())

        fila_promedio.addWidget(self.svg_estrella_grande)
        fila_promedio.addWidget(self.lbl_promedio_num)
        fila_promedio.addWidget(self.lbl_sobre_cinco)
        fila_promedio.addStretch()
        layout_info.addLayout(fila_promedio)
        layout_info.addSpacing(8)

        # Estrellas pequeñas — separadas del promedio con espacio propio
        self.widget_estrellas = _estrellas_widget(0, maximo=5)
        layout_info.addWidget(self.widget_estrellas)
        layout_info.addSpacing(12)

        # Chips de etiquetas
        self.fila_etiquetas = QHBoxLayout()
        self.fila_etiquetas.setSpacing(6)
        self.fila_etiquetas.setContentsMargins(0, 0, 0, 0)
        layout_info.addLayout(self.fila_etiquetas)
        layout_info.addStretch()

        fila_contenido.addLayout(layout_info)
        fila_contenido.addStretch()

        layout_raiz.addLayout(fila_contenido)
        return frame

    # ── Regresar ──────────────────────────────────────────────────────────────

    def _regresar(self):
        if callable(self._on_back):
            self._on_back()
        else:
            self.close()

    # ── Carga de datos ────────────────────────────────────────────────────────

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
                        pixmap.scaled(
                            116, 155,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                    )
                    self.lbl_poster.setStyleSheet(S_POSTER_FILLED())
                else:
                    # 🔥 si la imagen falla → limpiar
                    self.lbl_poster.clear()
                    self.lbl_poster.setText("POSTER")
                    self.lbl_poster.setStyleSheet(S_POSTER())
            else:
                # 🔥 SI NO HAY IMAGEN → limpiar (ESTO ERA LO QUE TE FALTABA)
                self.lbl_poster.clear()
                self.lbl_poster.setText("POSTER")
                self.lbl_poster.setStyleSheet(S_POSTER())

            titulo = getattr(self.pelicula_obj, "titulo", self.titulo_pelicula)
            self.lbl_nombre.setText(titulo or "Sin título")

            self._actualizar_promedio_ui()

        self._actualizar_promedio_ui()

    def _actualizar_promedio_ui(self):
        pelicula_data = self.db.obtener_pelicula_por_id(self.pelicula_id)

        if not pelicula_data:
            self.lbl_promedio_num.setText("—")
            return

        promedio = pelicula_data.get("promedio_calificacion")

        if promedio is not None:
            self.lbl_promedio_num.setText(str(promedio))
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

        # Limpiar chips
        while self.fila_etiquetas.count():
            item = self.fila_etiquetas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        resenas = self.db.obtener_resenas_por_pelicula(self.pelicula_id)
        conteo = {}
        for r in resenas:
            for etiqueta in r.get("etiquetas_ia", []):
                conteo[etiqueta] = conteo.get(etiqueta, 0) + 1

        if conteo:
            top = sorted(conteo, key=conteo.get, reverse=True)[:4]
            for tag in top:
                chip = QLabel(tag)
                chip.setStyleSheet(S_ETIQUETA_CHIP())
                chip.setFixedHeight(24)
                self.fila_etiquetas.addWidget(chip)
        self.fila_etiquetas.addStretch()

    def _cargar_resenas(self):
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
        lbl.setStyleSheet(S_VACIO())
        return lbl

    # ── Tarjeta de reseña ─────────────────────────────────────────────────────

    def _crear_tarjeta(self, resena: dict) -> QFrame:
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setStyleSheet(S_TARJETA())
        tarjeta.setGraphicsEffect(_sombra_tarjeta())
        layout_tarjeta = QHBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(20, 18, 20, 18)
        layout_tarjeta.setSpacing(20)

        layout_tarjeta.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Avatar
        nombre_usuario = resena.get("nombre_usuario", "?")
        inicial = nombre_usuario[0].upper() if nombre_usuario else "?"
        avatar = QLabel(inicial)
        avatar.setObjectName("avatar")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(S_AVATAR())
        layout_tarjeta.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)

        # Columna texto
        col_texto = QVBoxLayout()
        col_texto.setSpacing(8)
        col_texto.setContentsMargins(0, 0, 0, 0)

        fila_top = QHBoxLayout()
        fila_top.setSpacing(10)
        fila_top.setContentsMargins(0, 0, 0, 0)

        lbl_usuario = QLabel(nombre_usuario)
        lbl_usuario.setStyleSheet(S_USUARIO_LABEL())
        fila_top.addWidget(lbl_usuario)
        fila_top.addSpacing(8)

        stars = _estrellas_widget(resena.get("valoracion_ia"), maximo=5)
        fila_top.addWidget(stars)
        fila_top.addStretch()
        col_texto.addLayout(fila_top)

        texto_completo = resena.get("texto", "")
        texto_corto    = texto_completo[:160] + ("..." if len(texto_completo) > 160 else "")
        lbl_texto = QLabel(texto_corto)
        lbl_texto.setWordWrap(True)
        lbl_texto.setStyleSheet(S_TEXTO_RESENA())
        col_texto.addWidget(lbl_texto)

        if len(texto_completo) > 160:
            lbl_leer = QLabel("leer más")
            lbl_leer.setCursor(Qt.CursorShape.PointingHandCursor)
            lbl_leer.setStyleSheet(S_LEER_MAS())
            col_texto.addWidget(lbl_leer)

        layout_tarjeta.addLayout(col_texto, stretch=5)

        # Chips de etiquetas
        col_chips = QVBoxLayout()
        col_chips.setSpacing(5)
        col_chips.setContentsMargins(0, 0, 0, 0)

        for etiqueta in resena.get("etiquetas_ia", []):
            chip = QLabel(etiqueta)
            chip.setStyleSheet(S_ETIQUETA_CHIP())
            chip.setFixedHeight(24)
            chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col_chips.addWidget(chip)

        col_chips.addStretch()
        layout_tarjeta.addLayout(col_chips, stretch=2)

        # Columna derecha: valoración + botones
        col_derecha = QVBoxLayout()
        col_derecha.setSpacing(6)
        col_derecha.setContentsMargins(0, 0, 0, 0)
        col_derecha.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        val = resena.get("valoracion_ia", "?")
        lbl_num = QLabel(str(val))
        lbl_num.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_num.setStyleSheet(S_NUM_GRANDE())
        lbl_sobre = QLabel("/ 5")
        lbl_sobre.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_sobre.setStyleSheet(S_NUM_SOBRE())
        col_derecha.addWidget(lbl_num)
        col_derecha.addWidget(lbl_sobre)
        col_derecha.addStretch()

        if resena.get("usuario_id") == self.usuario_id or self.es_admin:
            btn_editar = QPushButton("  Editar")
            btn_editar.setFixedHeight(30)
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.setStyleSheet(S_BTN_EDITAR())
            btn_editar.setIcon(
                QIcon(self._pixmap_from_svg(_svg_edit_themed(), 14))
            )
            btn_editar.clicked.connect(
                lambda _, r=resena: self._abrir_form_editar(r)
            )
            col_derecha.addWidget(btn_editar)

            btn_eliminar = QPushButton("  Eliminar")
            btn_eliminar.setFixedHeight(30)
            btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_eliminar.setStyleSheet(S_BTN_ELIMINAR())
            btn_eliminar.setIcon(
                QIcon(self._pixmap_from_svg(_svg_trash_themed(), 14))
            )
            btn_eliminar.clicked.connect(
                lambda _, r=resena: self._eliminar_resena(r)
            )
            col_derecha.addWidget(btn_eliminar)

        layout_tarjeta.addLayout(col_derecha, stretch=1)
        return tarjeta

    # ── Helper SVG → pixmap ───────────────────────────────────────────────────

    def _pixmap_from_svg(self, svg_bytes: bytes, size: int) -> QPixmap:
        return _make_svg_pixmap(svg_bytes, size)

    # ── Acciones ──────────────────────────────────────────────────────────────

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
            callback        = self._cargar_resenas,
            es_admin        = self.es_admin
        )
        self.form_ae.show()

    def _eliminar_resena(self, resena: dict):
        confirmado = _CustomDialog.preguntar(
            "Eliminar reseña",
            "¿Estás seguro de que quieres eliminar esta reseña?",
            btn_si="Eliminar",
            btn_no="Cancelar",
            parent=self
        )
        if confirmado:
            uid_eliminar = resena.get("usuario_id") if self.es_admin else self.usuario_id
            resultado = self.clase_resena.eliminar_resena(
                resena_id  = resena["id"],
                usuario_id = uid_eliminar
            )
            if resultado["exito"]:
                self._cargar_resenas()
            else:
                _CustomDialog.informar(
                    "Error",
                    resultado["mensaje"],
                    parent=self
                )

    # ── Tema oscuro/claro ─────────────────────────────────────────────────────

    def refresh_theme(self):
        """Reaplica todos los estilos con el tema activo en ese momento."""
        self.setStyleSheet(S_MAIN())
        self.widget_cabecera.setStyleSheet(S_CABECERA())
        self.div_cabecera.setStyleSheet(S_DIVIDER())

        self.btn_regresar.setStyleSheet(S_BTN_REGRESAR())
        self.btn_regresar.setIcon(
            QIcon(self._pixmap_from_svg(_svg_back_bytes(), 14))
        )
        self.btn_regresar.setIconSize(QSize(14, 14))

        pixmap_actual = self.lbl_poster.pixmap()
        tiene_imagen = pixmap_actual is not None and not pixmap_actual.isNull()
        self.lbl_poster.setStyleSheet(
            S_POSTER_FILLED() if tiene_imagen else S_POSTER()
        )

        self.lbl_nombre.setStyleSheet(S_TITULO_PELICULA())
        self.lbl_promedio_num.setStyleSheet(S_PROMEDIO_NUM())
        self.lbl_sobre_cinco.setStyleSheet(S_SOBRE_CINCO())

        self.scroll_area.setStyleSheet(S_SCROLL())
        self.contenido_scroll.setStyleSheet(S_SCROLL_CONTENT())
        self.lbl_seccion.setStyleSheet(S_SECCION_TITULO())

        self.btn_agregar.setStyleSheet(S_BTN_AGREGAR())

        self._cargar_resenas()