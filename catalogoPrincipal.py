from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QGridLayout, QSizePolicy,
    QMessageBox, QApplication, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPixmap, QCursor, QColor, QIcon, QPainter, QPainterPath
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter

import os
import sys

from Json import JsonManager
from rutas import ruta_imagen

try:
    from clasePelicula import Pelicula
    def _get_all():  return Pelicula.todas()
    def _search(q):
        return [p for p in Pelicula.todas()
                if q.lower() in p.titulo.lower()]
    def _del(p): p.eliminar()
    USE_MODEL = True
except ImportError:
    _db = JsonManager()
    class _FakePelicula:
        def __init__(self, d):
            self.__dict__.update(d)
        def eliminar(self):
            _db.eliminar_pelicula(self.id)
    def _get_all():
        return [_FakePelicula(d) for d in _db.obtener_peliculas()]
    def _search(q):
        return [p for p in _get_all() if q.lower() in p.titulo.lower()]
    def _del(p): p.eliminar()
    USE_MODEL = False



# ICONOS SVG INLINE


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
    px1 = _svg_pixmap_at_scale(svg_str, size, scale=1)
    icon.addPixmap(px1, QIcon.Mode.Normal, QIcon.State.Off)
    px2 = _svg_pixmap_at_scale(svg_str, size, scale=2)
    icon.addPixmap(px2, QIcon.Mode.Normal, QIcon.State.Off)
    return icon


SVG_HOME = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/>
  <polyline points="9 21 9 12 15 12 15 21"/>
</svg>"""

SVG_HOME_ACTIVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#111827" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/>
  <polyline points="9 21 9 12 15 12 15 21"/>
</svg>"""

SVG_STAR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02
                   12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
</svg>"""

SVG_STAR_ACTIVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#111827" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02
                   12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
</svg>"""

#  stroke visible en gris oscuro 
SVG_SEARCH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="8"/>
  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
</svg>"""

# variantes inactivo / activo (blanco) para grid y lista
SVG_GRID = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
  <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
</svg>"""

SVG_GRID_ACTIVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
  <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
</svg>"""

SVG_LIST = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
  <line x1="8" y1="18" x2="21" y2="18"/>
  <line x1="3" y1="6" x2="3.01" y2="6"/>
  <line x1="3" y1="12" x2="3.01" y2="12"/>
  <line x1="3" y1="18" x2="3.01" y2="18"/>
</svg>"""

SVG_LIST_ACTIVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
  <line x1="8" y1="18" x2="21" y2="18"/>
  <line x1="3" y1="6" x2="3.01" y2="6"/>
  <line x1="3" y1="12" x2="3.01" y2="12"/>
  <line x1="3" y1="18" x2="3.01" y2="18"/>
</svg>"""

SVG_PLUS = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round">
  <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
</svg>"""

SVG_PLUS_DARK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#9CA3AF" stroke-width="2" stroke-linecap="round">
  <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
</svg>"""

SVG_EDIT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
</svg>"""

SVG_TRASH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
  stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 6 5 6 21 6"/>
  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
  <path d="M10 11v6"/><path d="M14 11v6"/>
  <path d="M9 6V4h6v2"/>
</svg>"""



# ESTILOS


STYLE_APP = """
    QWidget {
        background-color: #F7F8FA;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
        color: #111827;
    }
"""

STYLE_SIDEBAR = """
    QFrame#sidebar {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
"""

STYLE_TOPBAR = """
    QFrame#topbar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E5E7EB;
    }
"""

STYLE_SEARCH = """
    QLineEdit {
        background-color: #F9FAFB;
        border: 1.5px solid #E5E7EB;
        border-radius: 9px;
        padding: 8px 14px 8px 36px;
        font-size: 13px;
        color: #111827;
        font-family: 'Segoe UI', sans-serif;
    }
    QLineEdit:focus {
        border: 1.5px solid #3B82F6;
        background-color: #FFFFFF;
    }
"""

STYLE_SCROLL = """
    QScrollArea { border: none; background: transparent; }
    QScrollBar:vertical {
        background: transparent; width: 5px;
    }
    QScrollBar::handle:vertical {
        background: #D1D5DB; border-radius: 3px; min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background: #9CA3AF; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""

STYLE_MOVIE_CARD = """
    QFrame#movieCard {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
    }
"""

STYLE_MOVIE_ROW = """
    QFrame#movieRow {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
    }
"""

STYLE_ADD_CARD = """
    QFrame#addCard {
        background-color: #FFFFFF;
        border: 2px dashed #D1D5DB;
        border-radius: 14px;
    }
    QFrame#addCard:hover {
        border-color: #9CA3AF;
        background-color: #F9FAFB;
    }
"""

STYLE_BTN_NAV = """
    QPushButton {
        background: transparent;
        color: #6B7280;
        border: none;
        border-radius: 8px;
        padding: 9px 12px;
        text-align: left;
        font-size: 13px;
        font-weight: 500;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #F3F4F6;
        color: #111827;
    }
"""

STYLE_BTN_NAV_ACTIVE = """
    QPushButton {
        background-color: #F3F4F6;
        color: #111827;
        border: none;
        border-radius: 8px;
        padding: 9px 12px;
        text-align: left;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_BTN_EXPLORE = """
    QPushButton {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 8px 0px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover { background-color: #1F2937; }
    QPushButton:pressed { background-color: #374151; }
"""

STYLE_BTN_EDIT = """
    QPushButton {
        background: transparent;
        color: #6B7280;
        border: 1.5px solid #E5E7EB;
        border-radius: 7px;
        padding: 5px 10px;
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

STYLE_BTN_DELETE = """
    QPushButton {
        background: transparent;
        color: #EF4444;
        border: 1.5px solid #FCA5A5;
        border-radius: 7px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover {
        background-color: #FEF2F2;
        border-color: #EF4444;
    }
"""

STYLE_BTN_ADD = """
    QPushButton {
        background-color: #111827;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 9px 16px;
        font-size: 13px;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton:hover { background-color: #1F2937; }
    QPushButton:pressed { background-color: #374151; }
"""

STYLE_BTN_TOGGLE = """
    QPushButton {
        background: #F3F4F6;
        color: #6B7280;
        border: none;
        border-radius: 8px;
        font-size: 13px;
    }
    QPushButton:hover { background: #E5E7EB; color: #111827; }
    QPushButton:checked { background: #111827; color: #FFFFFF; }
"""

STYLE_AVATAR = """
    QLabel#avatar {
        background-color: #EEF2FF;
        color: #4F46E5;
        border-radius: 22px;
        font-size: 16px;
        font-weight: 700;
        font-family: 'Segoe UI', sans-serif;
    }
"""

STYLE_MSGBOX = """
    QMessageBox { background-color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    QMessageBox QLabel { color: #111827; font-size: 13px; }
    QMessageBox QPushButton {
        background-color: #111827; color: white; border: none;
        border-radius: 8px; padding: 8px 20px;
        font-size: 12px; font-weight: 600; min-width: 80px;
    }
    QMessageBox QPushButton:hover { background-color: #1F2937; }
"""



# HELPERS


def _sombra(blur=16, dy=3, alpha=16) -> QGraphicsDropShadowEffect:
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(blur)
    s.setOffset(0, dy)
    s.setColor(QColor(0, 0, 0, alpha))
    return s

def _estrellas(promedio) -> str:
    try:
        v = float(promedio)
        v = max(0, min(5, round(v)))
        return "\u2605" * v + "\u2606" * (5 - v)
    except (TypeError, ValueError):
        return "\u2606\u2606\u2606\u2606\u2606"

def _cargar_px(pelicula, w, h):
    ruta = ruta_imagen(getattr(pelicula, "imagen", None))
    if ruta and os.path.exists(ruta):
        px = QPixmap(ruta)
        if not px.isNull():
            return px.scaled(w, h,
                             Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)
    return None


# TARJETA DE PELICULA (grid)


class MovieCard(QFrame):
    explore_clicked = pyqtSignal(object)
    edit_clicked    = pyqtSignal(object)
    delete_clicked  = pyqtSignal(object)

    def __init__(self, pelicula, es_admin=False, parent=None):
        super().__init__(parent)
        self.pelicula = pelicula
        self.es_admin = es_admin
        self._db      = JsonManager()
        self.setObjectName("movieCard")
        self.setStyleSheet(STYLE_MOVIE_CARD)
        self.setFixedWidth(220)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setGraphicsEffect(_sombra())
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Poster
        img = QLabel()
        img.setFixedSize(220, 200)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setStyleSheet("""
            QLabel {
                background-color: #F3F4F6;
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
                color: #9CA3AF;
                font-size: 18px;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        px = _cargar_px(self.pelicula, 220, 200)
        if px:
            img.setPixmap(px)
        else:
            img.setText((self.pelicula.titulo or "?")[:2].upper())
        img.mousePressEvent = lambda e: (
            self.explore_clicked.emit(self.pelicula)
            if e.button() == Qt.MouseButton.LeftButton else None
        )
        root.addWidget(img)

        # Info
        pad = QVBoxLayout()
        pad.setContentsMargins(16, 14, 16, 16)
        pad.setSpacing(4)

        lbl_titulo = QLabel(self.pelicula.titulo or "Sin titulo")
        lbl_titulo.setStyleSheet(
            "color: #111827; font-size: 14px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lbl_titulo.setWordWrap(False)

        meta_parts = []
        if getattr(self.pelicula, "anio", None):
            meta_parts.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None):
            meta_parts.append(self.pelicula.director)
        lbl_meta = QLabel("  \u00b7  ".join(meta_parts))
        lbl_meta.setStyleSheet(
            "color: #9CA3AF; font-size: 11px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent;"
        )

        data     = self._db.obtener_pelicula_por_id(getattr(self.pelicula, "id", None))
        promedio = data.get("promedio_calificacion") if data else None
        estrellas_str = _estrellas(promedio)
        prom_str = f"  {promedio}" if promedio is not None else "  -"

        lbl_stars = QLabel(estrellas_str + prom_str)
        lbl_stars.setStyleSheet(
            "color: #F59E0B; font-size: 12px; background: transparent;"
            "font-family: 'Segoe UI', sans-serif;"
        )

        pad.addWidget(lbl_titulo)
        pad.addWidget(lbl_meta)
        pad.addWidget(lbl_stars)
        pad.addSpacing(10)

        btn_exp = QPushButton("Explorar y resenar")
        btn_exp.setFixedHeight(34)
        btn_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exp.setStyleSheet(STYLE_BTN_EXPLORE)
        btn_exp.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        pad.addWidget(btn_exp)

        if self.es_admin:
            fila = QHBoxLayout()
            fila.setSpacing(6)
            fila.setContentsMargins(0, 6, 0, 0)

            btn_edit = QPushButton("Editar")
            btn_edit.setFixedHeight(28)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet(STYLE_BTN_EDIT)
            btn_edit.setIcon(_svg_icon(SVG_EDIT, 12))
            btn_edit.setIconSize(QSize(12, 12))
            btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.pelicula))

            btn_del = QPushButton("Eliminar")
            btn_del.setFixedHeight(28)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet(STYLE_BTN_DELETE)
            btn_del.setIcon(_svg_icon(SVG_TRASH, 12))
            btn_del.setIconSize(QSize(12, 12))
            btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.pelicula))

            fila.addWidget(btn_edit)
            fila.addWidget(btn_del)
            pad.addLayout(fila)

        root.addLayout(pad)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.explore_clicked.emit(self.pelicula)
        super().mousePressEvent(event)


# FILA DE PELICULA (lista)


class MovieRow(QFrame):
    explore_clicked = pyqtSignal(object)
    edit_clicked    = pyqtSignal(object)
    delete_clicked  = pyqtSignal(object)

    def __init__(self, pelicula, es_admin=False, parent=None):
        super().__init__(parent)
        self.pelicula = pelicula
        self.es_admin = es_admin
        self._db      = JsonManager()
        self.setObjectName("movieRow")
        self.setStyleSheet(STYLE_MOVIE_ROW)
        self.setFixedHeight(100)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setGraphicsEffect(_sombra())
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 14, 18, 14)
        layout.setSpacing(16)

        # Thumbnail
        thumb = QLabel()
        thumb.setFixedSize(54, 76)
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb.setStyleSheet("""
            QLabel {
                background-color: #F3F4F6;
                border-radius: 8px;
                color: #9CA3AF;
                font-size: 11px;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        px = _cargar_px(self.pelicula, 54, 76)
        if px:
            thumb.setPixmap(px)
        else:
            thumb.setText((self.pelicula.titulo or "?")[:2].upper())
        layout.addWidget(thumb)

        # Info
        col_info = QVBoxLayout()
        col_info.setSpacing(3)
        col_info.setContentsMargins(0, 0, 0, 0)

        lbl_titulo = QLabel(self.pelicula.titulo or "Sin titulo")
        lbl_titulo.setStyleSheet(
            "color: #111827; font-size: 14px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        meta_parts = []
        if getattr(self.pelicula, "anio", None):
            meta_parts.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None):
            meta_parts.append(self.pelicula.director)
        lbl_meta = QLabel("  \u00b7  ".join(meta_parts))
        lbl_meta.setStyleSheet(
            "color: #9CA3AF; font-size: 11px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent;"
        )
        desc = getattr(self.pelicula, "descripcion", "") or ""
        lbl_desc = QLabel(desc[:80] + ("..." if len(desc) > 80 else ""))
        lbl_desc.setStyleSheet(
            "color: #6B7280; font-size: 12px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent;"
        )
        col_info.addWidget(lbl_titulo)
        col_info.addWidget(lbl_meta)
        col_info.addWidget(lbl_desc)
        col_info.addStretch()
        layout.addLayout(col_info, stretch=1)

        # Derecha: estrellas + botones
        col_right = QVBoxLayout()
        col_right.setSpacing(4)
        col_right.setContentsMargins(0, 0, 0, 0)
        col_right.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        data     = self._db.obtener_pelicula_por_id(getattr(self.pelicula, "id", None))
        promedio = data.get("promedio_calificacion") if data else None

        lbl_stars = QLabel(
            _estrellas(promedio) + (f"  {promedio}" if promedio is not None else "  -")
        )
        lbl_stars.setStyleSheet(
            "color: #F59E0B; font-size: 12px; background: transparent;"
        )
        lbl_stars.setAlignment(Qt.AlignmentFlag.AlignRight)
        col_right.addWidget(lbl_stars)
        col_right.addSpacing(6)

        fila_btns = QHBoxLayout()
        fila_btns.setSpacing(6)

        btn_exp = QPushButton("Explorar")
        btn_exp.setFixedHeight(30)
        btn_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exp.setStyleSheet(STYLE_BTN_EXPLORE)
        btn_exp.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        fila_btns.addWidget(btn_exp)

        if self.es_admin:
            btn_edit = QPushButton()
            btn_edit.setFixedSize(30, 30)
            btn_edit.setIcon(_svg_icon(SVG_EDIT, 14))
            btn_edit.setIconSize(QSize(14, 14))
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet(STYLE_BTN_EDIT)
            btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.pelicula))

            btn_del = QPushButton()
            btn_del.setFixedSize(30, 30)
            btn_del.setIcon(_svg_icon(SVG_TRASH, 14))
            btn_del.setIconSize(QSize(14, 14))
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet(STYLE_BTN_DELETE)
            btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.pelicula))

            fila_btns.addWidget(btn_edit)
            fila_btns.addWidget(btn_del)

        col_right.addLayout(fila_btns)
        layout.addLayout(col_right)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.explore_clicked.emit(self.pelicula)
        super().mousePressEvent(event)


# TARJETA AGREGAR (solo admin)


class AddMovieCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, modo_lista=False, parent=None):
        super().__init__(parent)
        self.setObjectName("addCard")
        self.setStyleSheet(STYLE_ADD_CARD)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedWidth(220) if not modo_lista else self.setFixedHeight(100)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(_svg_pixmap(SVG_PLUS_DARK, 28))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent;")

        text = QLabel("Agregar pelicula")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet(
            "color: #9CA3AF; font-size: 12px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        layout.addWidget(icon_lbl)
        layout.addWidget(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


# BADGE DE USUARIO (sidebar)


class UserBadge(QWidget):
    def __init__(self, nombre: str, rol: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar = QLabel(nombre[0].upper() if nombre else "?")
        avatar.setObjectName("avatar")
        avatar.setFixedSize(44, 44)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(STYLE_AVATAR)

        lbl_nombre = QLabel(nombre)
        lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_nombre.setStyleSheet(
            "color: #111827; font-size: 13px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lbl_rol = QLabel("Administrador" if rol == "admin" else "Lector")
        lbl_rol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_rol.setStyleSheet(
            "color: #9CA3AF; font-size: 11px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_nombre)
        layout.addWidget(lbl_rol)



# VENTANA PRINCIPAL DEL CATALOGO


class CatalogoWindow(QWidget):
    open_edit    = pyqtSignal(object)
    open_reviews = pyqtSignal(object)

    def __init__(self, usuario="usuario", rol: str = "lector", parent=None):
        super().__init__(parent)

        if isinstance(usuario, dict):
            self.usuario_dict = usuario
            self.usuario      = usuario.get("nombre_usuario", "usuario")
            rol_raw           = str(usuario.get("rol", rol)).lower().strip()
        else:
            self.usuario_dict = {"nombre_usuario": usuario, "id": None, "rol": rol}
            self.usuario      = usuario
            rol_raw           = str(rol).lower().strip()

        self.rol        = "admin" if rol_raw in ("admin", "administrador") else "lector"
        self.es_admin   = (self.rol == "admin")
        self.usuario_id = self.usuario_dict.get("id") or 0
        self._vista     = "grid"

        self.setWindowTitle("Catalogo de peliculas")
        self.setMinimumSize(980, 660)
        self.setStyleSheet(STYLE_APP)
        self._build_ui()
        self._cargar_catalogo()

    def _build_ui(self):
        raiz = QHBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        # SIDEBAR 
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(STYLE_SIDEBAR)
        sidebar.setFixedWidth(220)

        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(12, 0, 12, 20)
        sb.setSpacing(2)

        sb.addWidget(UserBadge(self.usuario, self.rol))

        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: #E5E7EB; border: none; max-height: 1px;")
        sb.addWidget(div)
        sb.addSpacing(10)

        self.btn_inicio  = self._nav_btn(SVG_HOME_ACTIVE, "Inicio",      activo=True)
        self.btn_resenas = self._nav_btn(SVG_STAR,        "Mis Resenas", activo=False)

        # conectar ambos botones de navegación
        self.btn_inicio.clicked.connect(self._ir_a_inicio)
        self.btn_resenas.clicked.connect(self._abrir_mis_resenas)

        sb.addWidget(self.btn_inicio)
        sb.addWidget(self.btn_resenas)
        sb.addStretch()

        if self.es_admin:
            btn_add_sb = QPushButton("  Nueva pelicula")
            btn_add_sb.setFixedHeight(40)
            btn_add_sb.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_add_sb.setIcon(_svg_icon(SVG_PLUS, 14))
            btn_add_sb.setIconSize(QSize(14, 14))
            btn_add_sb.setStyleSheet(STYLE_BTN_ADD)
            btn_add_sb.clicked.connect(self._abrir_agregar)
            sb.addWidget(btn_add_sb)

        raiz.addWidget(sidebar)

        # ── AREA PRINCIPAL
        main = QWidget()
        main.setStyleSheet("background: #F7F8FA;")
        ml = QVBoxLayout(main)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        # Topbar
        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setStyleSheet(STYLE_TOPBAR)
        topbar.setFixedHeight(64)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(28, 0, 28, 0)
        tb.setSpacing(12)

        lbl_titulo = QLabel("Lista de peliculas")
        lbl_titulo.setStyleSheet(
            "color: #111827; font-size: 20px; font-weight: 700;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        tb.addWidget(lbl_titulo)
        tb.addStretch()

        # contenedor relativo para superponer el ícono de búsqueda
        search_wrap = QWidget()
        search_wrap.setFixedSize(230, 36)
        search_wrap.setStyleSheet("background: transparent;")

        self.search_input = QLineEdit(search_wrap)
        self.search_input.setPlaceholderText("Buscar peliculas...")
        self.search_input.setFixedSize(230, 36)
        self.search_input.setStyleSheet(STYLE_SEARCH)
        self.search_input.textChanged.connect(self._on_search)

        # Ícono de lupa flotante sobre el input (transparente a eventos de ratón)
        icon_search = QLabel(search_wrap)
        icon_search.setPixmap(_svg_pixmap(SVG_SEARCH, 15))
        icon_search.setFixedSize(15, 15)
        icon_search.move(11, 10)
        icon_search.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        icon_search.setStyleSheet("background: transparent;")
        icon_search.raise_()

        tb.addWidget(search_wrap)

        # toggles con íconos que cambian color según estado activo
        self.btn_grid_t = QPushButton()
        self.btn_list_t = QPushButton()
        for b in (self.btn_grid_t, self.btn_list_t):
            b.setFixedSize(36, 36)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setCheckable(True)
            b.setStyleSheet(STYLE_BTN_TOGGLE)
            b.setIconSize(QSize(16, 16))

        # Estado inicial: grid activo con ícono blanco
        self.btn_grid_t.setChecked(True)
        self.btn_grid_t.setIcon(_svg_icon(SVG_GRID_ACTIVE, 16))
        self.btn_list_t.setIcon(_svg_icon(SVG_LIST, 16))

        self.btn_grid_t.clicked.connect(lambda: self._cambiar_vista("grid"))
        self.btn_list_t.clicked.connect(lambda: self._cambiar_vista("lista"))

        tb.addWidget(self.btn_grid_t)
        tb.addWidget(self.btn_list_t)

        ml.addWidget(topbar)

        # Contador
        bar = QWidget()
        bar.setStyleSheet("background: transparent;")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setContentsMargins(28, 12, 28, 8)
        self.count_label = QLabel()
        self.count_label.setStyleSheet(
            "color: #9CA3AF; font-size: 12px; font-family: 'Segoe UI', sans-serif;"
            "background: transparent;"
        )
        bar_lay.addWidget(self.count_label)
        bar_lay.addStretch()
        ml.addWidget(bar)

        # Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(STYLE_SCROLL)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.inner = QVBoxLayout(self.container)
        self.inner.setContentsMargins(28, 4, 28, 28)
        self.inner.setSpacing(10)

        self.scroll.setWidget(self.container)
        ml.addWidget(self.scroll, stretch=1)

        raiz.addWidget(main, stretch=1)

    def _nav_btn(self, svg: str, texto: str, activo: bool = False) -> QPushButton:
        btn = QPushButton(f"    {texto}")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(40)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setIcon(_svg_icon(svg, 15))
        btn.setIconSize(QSize(15, 15))
        btn.setStyleSheet(STYLE_BTN_NAV_ACTIVE if activo else STYLE_BTN_NAV)
        return btn

    # VISTAS 

    def _cambiar_vista(self, vista: str):
        self._vista = vista
        self.btn_grid_t.setChecked(vista == "grid")
        self.btn_list_t.setChecked(vista == "lista")
        # FIX 2: intercambiar ícono SVG al cambiar estado
        self.btn_grid_t.setIcon(
            _svg_icon(SVG_GRID_ACTIVE if vista == "grid" else SVG_GRID, 16)
        )
        self.btn_list_t.setIcon(
            _svg_icon(SVG_LIST_ACTIVE if vista == "lista" else SVG_LIST, 16)
        )
        self._cargar_catalogo(self.search_input.text().strip())

    def _cargar_catalogo(self, query=""):
        peliculas = _search(query) if query else _get_all()
        self._render(peliculas)

    def _render(self, peliculas):
        while self.inner.count():
            item = self.inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.count_label.setText(
            f"{len(peliculas)} pelicula{'s' if len(peliculas) != 1 else ''}"
        )

        if self._vista == "grid":
            self._render_grid(peliculas)
        else:
            self._render_lista(peliculas)

        self.inner.addStretch()

    def _render_grid(self, peliculas):
        COLS = max(1, (self.scroll.width() - 56) // 240)
        grid_w = QWidget()
        grid_w.setStyleSheet("background: transparent;")
        grid = QGridLayout(grid_w)
        grid.setSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)

        for i, peli in enumerate(peliculas):
            card = MovieCard(peli, es_admin=self.es_admin)
            card.explore_clicked.connect(self._navigate_to_reviews)
            card.edit_clicked.connect(self._abrir_editar)
            card.delete_clicked.connect(self._confirmar_eliminar)
            grid.addWidget(card, i // COLS, i % COLS)

        if self.es_admin:
            add = AddMovieCard()
            add.setFixedSize(220, grid.itemAt(0).widget().height()
                             if grid.count() > 0 else 300)
            add.clicked.connect(self._abrir_agregar)
            pos = len(peliculas)
            grid.addWidget(add, pos // COLS, pos % COLS)

        self.inner.addWidget(grid_w)

    def _render_lista(self, peliculas):
        for peli in peliculas:
            row = MovieRow(peli, es_admin=self.es_admin)
            row.explore_clicked.connect(self._navigate_to_reviews)
            row.edit_clicked.connect(self._abrir_editar)
            row.delete_clicked.connect(self._confirmar_eliminar)
            self.inner.addWidget(row)

        if self.es_admin:
            add = AddMovieCard(modo_lista=True)
            add.clicked.connect(self._abrir_agregar)
            self.inner.addWidget(add)

    def _on_search(self, text):
        self._cargar_catalogo(text.strip())

    # ── CRUD ─────────────────────────────────────────────────

    def _abrir_agregar(self):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=None, callback=self.refresh, parent=self)
        form.show()

    def _abrir_editar(self, pelicula):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=pelicula, callback=self.refresh, parent=self)
        form.show()

    def _confirmar_eliminar(self, pelicula):
        msg = QMessageBox(self)
        msg.setWindowTitle("Eliminar pelicula")
        msg.setText(
            f"Eliminar \"{pelicula.titulo}\"?\nTambien se borraran sus resenas."
        )
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setStyleSheet(STYLE_MSGBOX)
        if msg.exec() == QMessageBox.StandardButton.Yes:
            _del(pelicula)
            self.refresh()

    def _navigate_to_reviews(self, pelicula):
        self.open_reviews.emit(pelicula)
        try:
            from FormReseñas import FormResenas
            form = FormResenas(
                pelicula_id     = getattr(pelicula, "id", None),
                usuario_id      = self.usuario_id,
                clase_pelicula  = None,
                clase_resena    = None,
                titulo_pelicula = getattr(pelicula, "titulo", "Sin titulo"),
                pelicula_obj    = pelicula,
            )
        except ImportError:
            form = _PlaceholderReviews(pelicula, self.usuario)

        if not hasattr(self, "_ventanas_resenas"):
            self._ventanas_resenas = []
        self._ventanas_resenas.append(form)
        form.destroyed.connect(
            lambda obj=form: self._ventanas_resenas.remove(obj)
            if obj in self._ventanas_resenas else None
        )
        form.destroyed.connect(lambda: self.refresh())
        form.show()
        form.raise_()
        form.activateWindow()

    # ── NAVEGACION SIDEBAR ───────────────────────────────────

    def _ir_a_inicio(self):
        """Marca Inicio como activo y refresca el catálogo."""
        self.btn_inicio.setStyleSheet(STYLE_BTN_NAV_ACTIVE)
        self.btn_inicio.setIcon(_svg_icon(SVG_HOME_ACTIVE, 15))
        self.btn_resenas.setStyleSheet(STYLE_BTN_NAV)
        self.btn_resenas.setIcon(_svg_icon(SVG_STAR, 15))
        self.refresh()

    def _abrir_mis_resenas(self):
        """Abre el formulario de reseñas del usuario actual."""
        # Actualiza estado visual del nav
        self.btn_resenas.setStyleSheet(STYLE_BTN_NAV_ACTIVE)
        self.btn_resenas.setIcon(_svg_icon(SVG_STAR_ACTIVE, 15))
        self.btn_inicio.setStyleSheet(STYLE_BTN_NAV)
        self.btn_inicio.setIcon(_svg_icon(SVG_HOME, 15))

        try:
            from FormReseñas import FormResenas
            form = FormResenas(
                pelicula_id     = None,
                usuario_id      = self.usuario_id,
                clase_pelicula  = None,
                clase_resena    = None,
                titulo_pelicula = "Mis Resenas",
                pelicula_obj    = None,
            )
        except ImportError:
            _fake = type("_P", (), {"titulo": "Mis Resenas"})()
            form  = _PlaceholderReviews(_fake, self.usuario)

        if not hasattr(self, "_ventanas_resenas"):
            self._ventanas_resenas = []
        self._ventanas_resenas.append(form)

        def _on_close():
            if form in self._ventanas_resenas:
                self._ventanas_resenas.remove(form)
            self._restaurar_nav_inicio()

        form.destroyed.connect(_on_close)
        form.show()
        form.raise_()
        form.activateWindow()

    def _restaurar_nav_inicio(self):
        """Restaura Inicio como activo cuando se cierra Mis Reseñas."""
        self.btn_inicio.setStyleSheet(STYLE_BTN_NAV_ACTIVE)
        self.btn_inicio.setIcon(_svg_icon(SVG_HOME_ACTIVE, 15))
        self.btn_resenas.setStyleSheet(STYLE_BTN_NAV)
        self.btn_resenas.setIcon(_svg_icon(SVG_STAR, 15))

    # ── API PUBLICA ──────────────────────────────────────────

    def refresh(self):
        self._cargar_catalogo(self.search_input.text().strip())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cargar_catalogo(self.search_input.text().strip())


# PLACEHOLDER


class _PlaceholderReviews(QWidget):
    closed = pyqtSignal()

    def __init__(self, pelicula, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Resenas - {pelicula.titulo}")
        self.setMinimumSize(900, 620)
        self.setStyleSheet(STYLE_APP)

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(f"{pelicula.titulo}\nFormResenas.py aun no esta disponible.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #6B7280; font-size: 14px; background: transparent;")
        lay.addWidget(lbl)

        btn_back = QPushButton("Volver al catalogo")
        btn_back.setFixedSize(200, 40)
        btn_back.setStyleSheet(STYLE_BTN_ADD)
        btn_back.clicked.connect(self._cerrar)
        lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    def _cerrar(self):
        self.closed.emit()
        self.close()


# ─────────────────────────────────────────────────────────────
# STANDALONE
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    usuario = sys.argv[1] if len(sys.argv) > 1 else "pablo_99"
    rol     = sys.argv[2] if len(sys.argv) > 2 else "lector"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        db = JsonManager()
        if not db.obtener_peliculas():
            demos = [
                ("Inception",         "Un ladron que roba secretos en suenos.",  None, "2010-07-16", 2010, "Christopher Nolan"),
                ("The Matrix",        "Un hacker descubre la verdad del mundo.", None, "1999-03-31", 1999, "Wachowski Sisters"),
                ("Dune",              "La epica batalla por Arrakis.",            None, "2021-10-22", 2021, "Denis Villeneuve"),
                ("Interstellar",      "Viaje por un agujero de gusano.",          None, "2014-11-07", 2014, "Christopher Nolan"),
                ("Blade Runner 2049", "Un blade runner descubre un secreto.",     None, "2017-10-06", 2017, "Denis Villeneuve"),
            ]
            for t, d, img, f, a, dir_ in demos:
                db.agregar_pelicula(t, d, img, f, a, dir_)
    except Exception as e:
        print(f"Demo data skipped: {e}")

    win = CatalogoWindow(usuario=usuario, rol=rol)
    win.open_edit.connect(lambda p: print(f"[open_edit] {p.titulo if p else 'nueva'}"))
    win.open_reviews.connect(lambda p: print(f"[open_reviews] {p.titulo}"))
    win.show()
    sys.exit(app.exec())