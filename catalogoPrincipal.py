from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QGridLayout, QSizePolicy,
    QApplication, QGraphicsDropShadowEffect,
    QStackedWidget, QDialog
)
from PyQt6.QtGui import QPixmap, QCursor, QColor, QIcon, QPainter
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtSvg import QSvgRenderer

import os
import sys

from Json import JsonManager
from rutas import ruta_imagen

try:
    from clasePelicula import Pelicula
    def _get_all(): return Pelicula.todas()
    def _search(q):
        return [p for p in Pelicula.todas() if q.lower() in p.titulo.lower()]
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


# =============================================================================
#  TEMA — paleta centralizada claro / oscuro
# =============================================================================

class Theme:
    LIGHT = {
        "bg_app":             "#F7F8FA",
        "bg_sidebar":         "#FFFFFF",
        "bg_topbar":          "#FFFFFF",
        "bg_card":            "#FFFFFF",
        "bg_search":          "#F9FAFB",
        "bg_hover":           "#F3F4F6",
        "bg_input_focus":     "#FFFFFF",
        "bg_toggle_btn":      "#F3F4F6",
        "bg_toggle_hover":    "#E5E7EB",
        "bg_add_card":        "#FFFFFF",
        "bg_nav_active":      "#F3F4F6",
        "bg_add_card_hover":  "#F9FAFB",
        "bg_avatar":          "#EEF2FF",
        "bg_img_placeholder": "#F3F4F6",
        "bg_titlebar":        "#FFFFFF",
        "border_main":        "#E5E7EB",
        "border_search":      "#E5E7EB",
        "border_card":        "#E5E7EB",
        "border_add":         "#D1D5DB",
        "border_add_hover":   "#9CA3AF",
        "border_edit":        "#E5E7EB",
        "border_edit_hover":  "#D1D5DB",
        "border_del":         "#FCA5A5",
        "border_titlebar":    "#E5E7EB",
        "text_primary":       "#111827",
        "text_secondary":     "#6B7280",
        "text_muted":         "#9CA3AF",
        "text_avatar":        "#4F46E5",
        "text_titlebar":      "#111827",
        "accent_btn":         "#111827",
        "accent_btn_h":       "#1F2937",
        "accent_btn_p":       "#374151",
        "accent_star":        "#F59E0B",
        "accent_del":         "#EF4444",
        "accent_del_bg":      "#FEF2F2",
        "accent_del_border":  "#FCA5A5",
        "icon_nav":           "#6B7280",
        "icon_nav_active":    "#111827",
        "icon_plus":          "#FFFFFF",
        "icon_plus_dark":     "#9CA3AF",
        "icon_search":        "#9CA3AF",
        "icon_star":          "#6B7280",
        "icon_star_active":   "#111827",
        "icon_film":          "#9CA3AF",
        "icon_edit":          "#6B7280",
        "icon_trash":         "#EF4444",
        "icon_theme":         "#6B7280",
        "icon_logout":        "#EF4444",
        "icon_winbtn":        "#6B7280",
        "icon_winbtn_close":  "#EF4444",
        "winbtn_close_hover": "#FEE2E2",
    }

    DARK = {
        "bg_app":             "#0D1117",
        "bg_sidebar":         "#161B22",
        "bg_topbar":          "#161B22",
        "bg_card":            "#1C2128",
        "bg_search":          "#21262D",
        "bg_hover":           "#21262D",
        "bg_input_focus":     "#1C2128",
        "bg_toggle_btn":      "#21262D",
        "bg_toggle_hover":    "#30363D",
        "bg_add_card":        "#1C2128",
        "bg_nav_active":      "#21262D",
        "bg_add_card_hover":  "#21262D",
        "bg_avatar":          "#1F2D45",
        "bg_img_placeholder": "#21262D",
        "bg_titlebar":        "#161B22",
        "border_main":        "#30363D",
        "border_search":      "#30363D",
        "border_card":        "#30363D",
        "border_add":         "#3D444D",
        "border_add_hover":   "#6E7681",
        "border_edit":        "#30363D",
        "border_edit_hover":  "#484F58",
        "border_del":         "#6E1010",
        "border_titlebar":    "#30363D",
        "text_primary":       "#E6EDF3",
        "text_secondary":     "#8B949E",
        "text_muted":         "#6E7681",
        "text_avatar":        "#79C0FF",
        "text_titlebar":      "#E6EDF3",
        "accent_btn":         "#238636",
        "accent_btn_h":       "#2EA043",
        "accent_btn_p":       "#196C2E",
        "accent_star":        "#E3B341",
        "accent_del":         "#F85149",
        "accent_del_bg":      "#1C0B0B",
        "accent_del_border":  "#6E1010",
        "icon_nav":           "#6E7681",
        "icon_nav_active":    "#E6EDF3",
        "icon_plus":          "#FFFFFF",
        "icon_plus_dark":     "#6E7681",
        "icon_search":        "#6E7681",
        "icon_star":          "#6E7681",
        "icon_star_active":   "#E6EDF3",
        "icon_film":          "#6E7681",
        "icon_edit":          "#8B949E",
        "icon_trash":         "#F85149",
        "icon_theme":         "#E3B341",
        "icon_logout":        "#F85149",
        "icon_winbtn":        "#8B949E",
        "icon_winbtn_close":  "#F85149",
        "winbtn_close_hover": "#2D1010",
    }

    _mode = "light"

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


# =============================================================================
#  SVG HELPERS
# =============================================================================

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
    for scale in (1, 2):
        px = _svg_pixmap_at_scale(svg_str, size, scale)
        icon.addPixmap(px, QIcon.Mode.Normal, QIcon.State.Off)
    return icon


# =============================================================================
#  SVG ICONS (dinámicos según tema)
# =============================================================================

def _ico_home(active=False):
    c = Theme.get("icon_nav_active") if active else Theme.get("icon_nav")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><polyline points="9 21 9 12 15 12 15 21"/></svg>'

def _ico_star(active=False):
    c = Theme.get("icon_star_active") if active else Theme.get("icon_star")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

def _ico_search():
    c = Theme.get("icon_search")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'

def _ico_grid(active=False):
    c = "#FFFFFF" if active else Theme.get("icon_nav")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>'

def _ico_list(active=False):
    c = "#FFFFFF" if active else Theme.get("icon_nav")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'

def _ico_plus(dark=False):
    c = Theme.get("icon_plus_dark") if dark else Theme.get("icon_plus")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'

def _ico_edit():
    c = Theme.get("icon_edit")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'

def _ico_trash():
    c = Theme.get("icon_trash")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>'

def _ico_film():
    c = Theme.get("icon_film")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="17" y1="7" x2="22" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/></svg>'

def _ico_moon():
    c = Theme.get("icon_theme")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'

def _ico_sun():
    c = Theme.get("icon_theme")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'

def _ico_logout():
    c = Theme.get("icon_logout")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'

def _ico_minimize():
    c = Theme.get("icon_winbtn")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>'

def _ico_maximize():
    c = Theme.get("icon_winbtn")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>'

def _ico_restore():
    c = Theme.get("icon_winbtn")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="12" height="12" rx="1"/><path d="M4 16V4h12"/></svg>'

def _ico_close():
    c = Theme.get("icon_winbtn_close")
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'


# =============================================================================
#  ESTILOS DINÁMICOS
# =============================================================================

def S_APP():
    return f"""
        QWidget {{
            background-color: {Theme.get("bg_app")};
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
            color: {Theme.get("text_primary")};
        }}
    """

def S_SIDEBAR():
    return f"""
        QFrame#sidebar {{
            background-color: {Theme.get("bg_sidebar")};
            border-right: 1px solid {Theme.get("border_main")};
        }}
    """

def S_TOPBAR():
    return f"""
        QFrame#topbar {{
            background-color: {Theme.get("bg_topbar")};
            border-bottom: 1px solid {Theme.get("border_main")};
        }}
    """

def S_SEARCH():
    return f"""
        QLineEdit {{
            background-color: {Theme.get("bg_search")};
            border: 1.5px solid {Theme.get("border_search")};
            border-radius: 9px;
            padding: 8px 14px 8px 36px;
            font-size: 13px;
            color: {Theme.get("text_primary")};
            font-family: 'Segoe UI', sans-serif;
        }}
        QLineEdit:focus {{
            border: 1.5px solid #3B82F6;
            background-color: {Theme.get("bg_input_focus")};
        }}
    """

def S_SCROLL():
    return f"""
        QScrollArea {{ border: none; background: transparent; }}
        QScrollBar:vertical {{ background: transparent; width: 5px; }}
        QScrollBar::handle:vertical {{
            background: {Theme.get("border_main")}; border-radius: 3px; min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{ background: {Theme.get("text_muted")}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """

def S_CARD():
    return f"""
        QFrame#movieCard {{
            background-color: {Theme.get("bg_card")};
            border: 1px solid {Theme.get("border_card")};
            border-radius: 14px;
        }}
    """

def S_ROW():
    return f"""
        QFrame#movieRow {{
            background-color: {Theme.get("bg_card")};
            border: 1px solid {Theme.get("border_card")};
            border-radius: 14px;
        }}
    """

def S_ADD_CARD():
    return f"""
        QFrame#addCard {{
            background-color: {Theme.get("bg_add_card")};
            border: 2px dashed {Theme.get("border_add")};
            border-radius: 14px;
        }}
        QFrame#addCard:hover {{
            border-color: {Theme.get("border_add_hover")};
            background-color: {Theme.get("bg_add_card_hover")};
        }}
    """

def S_BTN_NAV(active=False):
    if active:
        return f"""
            QPushButton {{
                background-color: {Theme.get("bg_nav_active")};
                color: {Theme.get("text_primary")};
                border: none; border-radius: 8px;
                padding: 9px 12px; text-align: left;
                font-size: 13px; font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }}
        """
    return f"""
        QPushButton {{
            background: transparent;
            color: {Theme.get("text_secondary")};
            border: none; border-radius: 8px;
            padding: 9px 12px; text-align: left;
            font-size: 13px; font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {Theme.get("bg_hover")};
            color: {Theme.get("text_primary")};
        }}
    """

def S_BTN_EXPLORE():
    return f"""
        QPushButton {{
            background-color: {Theme.get("accent_btn")};
            color: #FFFFFF; border: none; border-radius: 8px;
            padding: 8px 0px; font-size: 12px; font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{ background-color: {Theme.get("accent_btn_h")}; }}
        QPushButton:pressed {{ background-color: {Theme.get("accent_btn_p")}; }}
    """

def S_BTN_EDIT():
    return f"""
        QPushButton {{
            background: transparent;
            color: {Theme.get("text_secondary")};
            border: 1.5px solid {Theme.get("border_edit")};
            border-radius: 7px; padding: 5px 10px;
            font-size: 11px; font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {Theme.get("bg_hover")};
            border-color: {Theme.get("border_edit_hover")};
            color: {Theme.get("text_primary")};
        }}
    """

def S_BTN_DELETE():
    return f"""
        QPushButton {{
            background: transparent;
            color: {Theme.get("accent_del")};
            border: 1.5px solid {Theme.get("border_del")};
            border-radius: 7px; padding: 5px 10px;
            font-size: 11px; font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {Theme.get("accent_del_bg")};
            border-color: {Theme.get("accent_del")};
        }}
    """

def S_BTN_ADD():
    return f"""
        QPushButton {{
            background-color: {Theme.get("accent_btn")};
            color: #FFFFFF; border: none; border-radius: 10px;
            padding: 9px 16px; font-size: 13px; font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{ background-color: {Theme.get("accent_btn_h")}; }}
        QPushButton:pressed {{ background-color: {Theme.get("accent_btn_p")}; }}
    """

def S_BTN_LOGOUT():
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {Theme.get("accent_del")};
            border: 1.5px solid {Theme.get("accent_del_border")};
            border-radius: 10px;
            padding: 9px 16px; font-size: 13px; font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }}
        QPushButton:hover {{
            background-color: {Theme.get("accent_del_bg")};
            border-color: {Theme.get("accent_del")};
        }}
        QPushButton:pressed {{
            background-color: {Theme.get("accent_del_bg")};
        }}
    """

def S_BTN_TOGGLE():
    return f"""
        QPushButton {{
            background: {Theme.get("bg_toggle_btn")};
            color: {Theme.get("text_secondary")};
            border: none; border-radius: 8px; font-size: 13px;
        }}
        QPushButton:hover {{
            background: {Theme.get("bg_toggle_hover")};
            color: {Theme.get("text_primary")};
        }}
        QPushButton:checked {{
            background: {Theme.get("accent_btn")}; color: #FFFFFF;
        }}
    """

def S_AVATAR():
    return f"""
        QLabel#avatar {{
            background-color: {Theme.get("bg_avatar")};
            color: {Theme.get("text_avatar")};
            border-radius: 22px;
            font-size: 16px; font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
        }}
    """

def S_TITLEBAR():
    return f"""
        QFrame#titlebar {{
            background-color: {Theme.get("bg_titlebar")};
            border-bottom: 1px solid {Theme.get("border_titlebar")};
        }}
    """

def S_WIN_BTN_NORMAL():
    return f"""
        QPushButton {{
            background: transparent;
            border: none; border-radius: 6px; padding: 5px;
        }}
        QPushButton:hover {{ background-color: {Theme.get("bg_hover")}; }}
        QPushButton:pressed {{ background-color: {Theme.get("border_main")}; }}
    """

def S_WIN_BTN_CLOSE():
    return f"""
        QPushButton {{
            background: transparent;
            border: none; border-radius: 6px; padding: 5px;
        }}
        QPushButton:hover {{ background-color: {Theme.get("winbtn_close_hover")}; }}
        QPushButton:pressed {{ background-color: {Theme.get("winbtn_close_hover")}; }}
    """

def S_BTN_THEME():
    return f"""
        QPushButton {{
            background-color: {Theme.get("bg_toggle_btn")};
            border: 1.5px solid {Theme.get("border_main")};
            border-radius: 8px; padding: 6px;
        }}
        QPushButton:hover {{
            background-color: {Theme.get("bg_toggle_hover")};
            border-color: {Theme.get("border_edit_hover")};
        }}
    """


# =============================================================================
#  DIÁLOGO CUSTOM (sin barra del sistema — reemplaza QMessageBox en toda la app)
# =============================================================================

class _CustomDialog(QDialog):
    """
    Ventana emergente personalizada sin barra de título del sistema operativo.
    Respeta el tema activo (Theme.get) en el momento de mostrarse.
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

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(f"""
            color: {Theme.get('text_primary')};
            font-size: 15px; font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            background: transparent;
        """)
        lay.addWidget(lbl_titulo)
        lay.addSpacing(10)

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
        self.setFixedWidth(400)

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


# =============================================================================
#  HELPERS
# =============================================================================

def _sombra(blur=18, dy=4, alpha=10) -> QGraphicsDropShadowEffect:
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(blur)
    s.setOffset(0, dy)
    a = alpha if not Theme.is_dark() else alpha * 5
    s.setColor(QColor(0, 0, 0, a))
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


# =============================================================================
#  TITLE BAR PERSONALIZADA
# =============================================================================

class TitleBar(QFrame):
    theme_toggled = pyqtSignal()

    def __init__(self, window: "CatalogoWindow", parent=None):
        super().__init__(parent)
        self._window   = window
        self._drag_pos = None
        self.setObjectName("titlebar")
        self.setFixedHeight(48)
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 0, 12, 0)
        lay.setSpacing(0)

        self._dot = QLabel()
        self._dot.setFixedSize(8, 8)
        lay.addWidget(self._dot)
        lay.addSpacing(8)

        self._lbl_logo = QLabel("Cine AI")
        lay.addWidget(self._lbl_logo)
        lay.addStretch()

        self.btn_theme = QPushButton()
        self.btn_theme.setFixedSize(34, 34)
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setToolTip("Cambiar tema")
        self.btn_theme.clicked.connect(self.theme_toggled.emit)
        lay.addWidget(self.btn_theme)

        lay.addSpacing(14)

        self._sep = QFrame()
        self._sep.setFrameShape(QFrame.Shape.VLine)
        self._sep.setFixedWidth(1)
        lay.addWidget(self._sep)

        lay.addSpacing(12)

        self.btn_min = QPushButton()
        self.btn_min.setFixedSize(30, 30)
        self.btn_min.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_min.setToolTip("Minimizar")
        self.btn_min.clicked.connect(lambda: self._window.showMinimized())

        self.btn_max = QPushButton()
        self.btn_max.setFixedSize(30, 30)
        self.btn_max.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_max.setToolTip("Maximizar / Restaurar")
        self.btn_max.clicked.connect(self._toggle_maximize)

        self.btn_cls = QPushButton()
        self.btn_cls.setFixedSize(30, 30)
        self.btn_cls.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cls.setToolTip("Cerrar")
        self.btn_cls.clicked.connect(self._window.close)

        lay.addWidget(self.btn_min)
        lay.addSpacing(2)
        lay.addWidget(self.btn_max)
        lay.addSpacing(2)
        lay.addWidget(self.btn_cls)

        self.refresh()

    def _toggle_maximize(self):
        if self._window.isMaximized():
            self._window.showNormal()
        else:
            self._window.showMaximized()
        ico = _ico_restore() if self._window.isMaximized() else _ico_maximize()
        self.btn_max.setIcon(_svg_icon(ico, 14))
        self.btn_max.setIconSize(QSize(14, 14))

    def refresh(self):
        self.setStyleSheet(S_TITLEBAR())

        self._dot.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.get("accent_btn")};
                border-radius: 4px;
            }}
        """)
        self._lbl_logo.setStyleSheet(f"""
            color: {Theme.get("text_titlebar")};
            font-size: 15px; font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            background: transparent; letter-spacing: 0.5px;
        """)
        self._sep.setStyleSheet(
            f"background: {Theme.get('border_main')}; border: none;"
        )

        self.btn_theme.setStyleSheet(S_BTN_THEME())
        ico_tema = _ico_sun() if Theme.is_dark() else _ico_moon()
        self.btn_theme.setIcon(_svg_icon(ico_tema, 15))
        self.btn_theme.setIconSize(QSize(15, 15))

        self.btn_min.setStyleSheet(S_WIN_BTN_NORMAL())
        self.btn_min.setIcon(_svg_icon(_ico_minimize(), 14))
        self.btn_min.setIconSize(QSize(14, 14))

        ico_max = _ico_restore() if self._window.isMaximized() else _ico_maximize()
        self.btn_max.setStyleSheet(S_WIN_BTN_NORMAL())
        self.btn_max.setIcon(_svg_icon(ico_max, 14))
        self.btn_max.setIconSize(QSize(14, 14))

        self.btn_cls.setStyleSheet(S_WIN_BTN_CLOSE())
        self.btn_cls.setIcon(_svg_icon(_ico_close(), 14))
        self.btn_cls.setIconSize(QSize(14, 14))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self._window.frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos and (event.buttons() & Qt.MouseButton.LeftButton):
            if not self._window.isMaximized():
                self._window.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._toggle_maximize()
        super().mouseDoubleClickEvent(event)


# =============================================================================
#  MOVIE CARD (grid)
# =============================================================================

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
        self.setStyleSheet(S_CARD())
        self.setFixedWidth(220)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setGraphicsEffect(_sombra())
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        img = QLabel()
        img.setFixedSize(220, 200)
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.get("bg_img_placeholder")};
                border-top-left-radius: 14px; border-top-right-radius: 14px;
                color: {Theme.get("text_muted")}; font-size: 18px; font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }}
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

        pad = QVBoxLayout()
        pad.setContentsMargins(16, 14, 16, 16)
        pad.setSpacing(4)

        lbl_t = QLabel(self.pelicula.titulo or "Sin titulo")
        lbl_t.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 14px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lbl_t.setWordWrap(False)

        meta_parts = []
        if getattr(self.pelicula, "anio", None):
            meta_parts.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None):
            meta_parts.append(self.pelicula.director)
        lbl_m = QLabel("  \u00b7  ".join(meta_parts))
        lbl_m.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 11px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )

        data     = self._db.obtener_pelicula_por_id(getattr(self.pelicula, "id", None))
        promedio = data.get("promedio_calificacion") if data else None
        lbl_s = QLabel(
            _estrellas(promedio) + (f"  {promedio}" if promedio is not None else "  -")
        )
        lbl_s.setStyleSheet(
            f"color: {Theme.get('accent_star')}; font-size: 12px;"
            "background: transparent; font-family: 'Segoe UI', sans-serif;"
        )

        pad.addWidget(lbl_t)
        pad.addWidget(lbl_m)
        pad.addWidget(lbl_s)
        pad.addSpacing(10)

        btn_exp = QPushButton("Explorar y reseñar")
        btn_exp.setFixedHeight(34)
        btn_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exp.setStyleSheet(S_BTN_EXPLORE())
        btn_exp.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        pad.addWidget(btn_exp)

        if self.es_admin:
            fila = QHBoxLayout()
            fila.setSpacing(6)
            fila.setContentsMargins(0, 6, 0, 0)

            btn_edit = QPushButton("Editar")
            btn_edit.setFixedHeight(28)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet(S_BTN_EDIT())
            btn_edit.setIcon(_svg_icon(_ico_edit(), 12))
            btn_edit.setIconSize(QSize(12, 12))
            btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.pelicula))

            btn_del = QPushButton("Eliminar")
            btn_del.setFixedHeight(28)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet(S_BTN_DELETE())
            btn_del.setIcon(_svg_icon(_ico_trash(), 12))
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


# =============================================================================
#  MOVIE ROW (lista)
# =============================================================================

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
        self.setStyleSheet(S_ROW())
        self.setFixedHeight(100)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setGraphicsEffect(_sombra())
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 14, 18, 14)
        layout.setSpacing(16)

        thumb = QLabel()
        thumb.setFixedSize(54, 76)
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.get("bg_img_placeholder")}; border-radius: 8px;
                color: {Theme.get("text_muted")}; font-size: 11px; font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }}
        """)
        px = _cargar_px(self.pelicula, 54, 76)
        if px:
            thumb.setPixmap(px)
        else:
            thumb.setText((self.pelicula.titulo or "?")[:2].upper())
        layout.addWidget(thumb)

        col_info = QVBoxLayout()
        col_info.setSpacing(3)
        col_info.setContentsMargins(0, 0, 0, 0)

        lbl_t = QLabel(self.pelicula.titulo or "Sin titulo")
        lbl_t.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 14px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        meta_parts = []
        if getattr(self.pelicula, "anio", None):
            meta_parts.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None):
            meta_parts.append(self.pelicula.director)
        lbl_m = QLabel("  \u00b7  ".join(meta_parts))
        lbl_m.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 11px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        desc = getattr(self.pelicula, "descripcion", "") or ""
        lbl_d = QLabel(desc[:80] + ("..." if len(desc) > 80 else ""))
        lbl_d.setStyleSheet(
            f"color: {Theme.get('text_secondary')}; font-size: 12px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        col_info.addWidget(lbl_t)
        col_info.addWidget(lbl_m)
        col_info.addWidget(lbl_d)
        col_info.addStretch()
        layout.addLayout(col_info, stretch=1)

        col_right = QVBoxLayout()
        col_right.setSpacing(4)
        col_right.setContentsMargins(0, 0, 0, 0)
        col_right.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        data     = self._db.obtener_pelicula_por_id(getattr(self.pelicula, "id", None))
        promedio = data.get("promedio_calificacion") if data else None
        lbl_s = QLabel(
            _estrellas(promedio) + (f"  {promedio}" if promedio is not None else "  -")
        )
        lbl_s.setStyleSheet(
            f"color: {Theme.get('accent_star')}; font-size: 12px; background: transparent;"
        )
        lbl_s.setAlignment(Qt.AlignmentFlag.AlignRight)
        col_right.addWidget(lbl_s)
        col_right.addSpacing(6)

        fila_btns = QHBoxLayout()
        fila_btns.setSpacing(6)

        btn_exp = QPushButton("Explorar")
        btn_exp.setFixedHeight(30)
        btn_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exp.setStyleSheet(S_BTN_EXPLORE())
        btn_exp.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        fila_btns.addWidget(btn_exp)

        if self.es_admin:
            btn_edit = QPushButton()
            btn_edit.setFixedSize(30, 30)
            btn_edit.setIcon(_svg_icon(_ico_edit(), 14))
            btn_edit.setIconSize(QSize(14, 14))
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet(S_BTN_EDIT())
            btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.pelicula))

            btn_del = QPushButton()
            btn_del.setFixedSize(30, 30)
            btn_del.setIcon(_svg_icon(_ico_trash(), 14))
            btn_del.setIconSize(QSize(14, 14))
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet(S_BTN_DELETE())
            btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.pelicula))

            fila_btns.addWidget(btn_edit)
            fila_btns.addWidget(btn_del)

        col_right.addLayout(fila_btns)
        layout.addLayout(col_right)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.explore_clicked.emit(self.pelicula)
        super().mousePressEvent(event)


# =============================================================================
#  ADD CARD (solo admin)
# =============================================================================

class AddMovieCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, modo_lista=False, parent=None):
        super().__init__(parent)
        self.setObjectName("addCard")
        self.setStyleSheet(S_ADD_CARD())
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if not modo_lista:
            self.setFixedWidth(220)
        else:
            self.setFixedHeight(100)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(_svg_pixmap(_ico_plus(dark=True), 28))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent;")

        text = QLabel("Agregar pelicula")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 12px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        layout.addWidget(icon_lbl)
        layout.addWidget(text)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


# =============================================================================
#  USER BADGE
# =============================================================================

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
        avatar.setStyleSheet(S_AVATAR())

        lbl_n = QLabel(nombre)
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_n.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 13px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lbl_r = QLabel("Administrador" if rol == "admin" else "Lector")
        lbl_r.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_r.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 11px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_n)
        layout.addWidget(lbl_r)


# =============================================================================
#  PÁGINA — CATÁLOGO
# =============================================================================

class _PaginaCatalogo(QWidget):
    navigate_to_reviews = pyqtSignal(object)

    def __init__(self, es_admin: bool, parent=None):
        super().__init__(parent)
        self.es_admin = es_admin
        self._vista   = "grid"
        self._build()

    def _build(self):
        ml = QVBoxLayout(self)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        self._topbar = QFrame()
        self._topbar.setObjectName("topbar")
        self._topbar.setStyleSheet(S_TOPBAR())
        self._topbar.setFixedHeight(64)
        tb = QHBoxLayout(self._topbar)
        tb.setContentsMargins(28, 0, 28, 0)
        tb.setSpacing(12)

        self._lbl_titulo = QLabel("Lista de peliculas")
        self._lbl_titulo.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 20px; font-weight: 700;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        tb.addWidget(self._lbl_titulo)
        tb.addStretch()

        search_wrap = QWidget()
        search_wrap.setFixedSize(230, 36)
        search_wrap.setStyleSheet("background: transparent;")

        self.search_input = QLineEdit(search_wrap)
        self.search_input.setPlaceholderText("Buscar peliculas...")
        self.search_input.setFixedSize(230, 36)
        self.search_input.setStyleSheet(S_SEARCH())
        self.search_input.textChanged.connect(self._on_search)

        self._search_icon_lbl = QLabel(search_wrap)
        self._search_icon_lbl.setPixmap(_svg_pixmap(_ico_search(), 15))
        self._search_icon_lbl.setFixedSize(15, 15)
        self._search_icon_lbl.move(11, 10)
        self._search_icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._search_icon_lbl.setStyleSheet("background: transparent;")
        self._search_icon_lbl.raise_()
        tb.addWidget(search_wrap)

        self.btn_grid_t = QPushButton()
        self.btn_list_t = QPushButton()
        for b in (self.btn_grid_t, self.btn_list_t):
            b.setFixedSize(36, 36)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setCheckable(True)
            b.setStyleSheet(S_BTN_TOGGLE())
            b.setIconSize(QSize(16, 16))

        self.btn_grid_t.setChecked(True)
        self.btn_grid_t.setIcon(_svg_icon(_ico_grid(active=True), 16))
        self.btn_list_t.setIcon(_svg_icon(_ico_list(active=False), 16))
        self.btn_grid_t.clicked.connect(lambda: self._cambiar_vista("grid"))
        self.btn_list_t.clicked.connect(lambda: self._cambiar_vista("lista"))
        tb.addWidget(self.btn_grid_t)
        tb.addWidget(self.btn_list_t)
        ml.addWidget(self._topbar)

        bar = QWidget()
        bar.setStyleSheet("background: transparent;")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setContentsMargins(28, 12, 28, 8)
        self.count_label = QLabel()
        self.count_label.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 12px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        bar_lay.addWidget(self.count_label)
        bar_lay.addStretch()
        ml.addWidget(bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(S_SCROLL())
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.inner = QVBoxLayout(self.container)
        self.inner.setContentsMargins(28, 4, 28, 28)
        self.inner.setSpacing(10)
        self.scroll.setWidget(self.container)
        ml.addWidget(self.scroll, stretch=1)

    def _cambiar_vista(self, vista: str):
        self._vista = vista
        self.btn_grid_t.setChecked(vista == "grid")
        self.btn_list_t.setChecked(vista == "lista")
        self.btn_grid_t.setIcon(_svg_icon(_ico_grid(active=(vista == "grid")), 16))
        self.btn_list_t.setIcon(_svg_icon(_ico_list(active=(vista == "lista")), 16))
        self.cargar(self.search_input.text().strip())

    def _on_search(self, text):
        self.cargar(text.strip())

    def cargar(self, query=""):
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
            card.explore_clicked.connect(self.navigate_to_reviews)
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
            row.explore_clicked.connect(self.navigate_to_reviews)
            row.edit_clicked.connect(self._abrir_editar)
            row.delete_clicked.connect(self._confirmar_eliminar)
            self.inner.addWidget(row)

        if self.es_admin:
            add = AddMovieCard(modo_lista=True)
            add.clicked.connect(self._abrir_agregar)
            self.inner.addWidget(add)

    def _abrir_agregar(self):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=None, callback=lambda: self.cargar(), parent=self)
        form.show()

    def _abrir_editar(self, pelicula):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=pelicula, callback=lambda: self.cargar(), parent=self)
        form.show()

    def _confirmar_eliminar(self, pelicula):
        confirmado = _CustomDialog.preguntar(
            "Eliminar película",
            f'¿Eliminar "{pelicula.titulo}"?\nTambién se borrarán sus reseñas.',
            btn_si="Eliminar",
            btn_no="Cancelar",
            parent=self
        )
        if confirmado:
            _del(pelicula)
            self.cargar()

    def refresh_theme(self):
        self.setStyleSheet(f"background: {Theme.get('bg_app')};")
        self._topbar.setStyleSheet(S_TOPBAR())
        self._lbl_titulo.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 20px; font-weight: 700;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        self.search_input.setStyleSheet(S_SEARCH())
        self._search_icon_lbl.setPixmap(_svg_pixmap(_ico_search(), 15))
        self.btn_grid_t.setStyleSheet(S_BTN_TOGGLE())
        self.btn_list_t.setStyleSheet(S_BTN_TOGGLE())
        self.btn_grid_t.setIcon(_svg_icon(_ico_grid(active=(self._vista == "grid")), 16))
        self.btn_list_t.setIcon(_svg_icon(_ico_list(active=(self._vista == "lista")), 16))
        self.count_label.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 12px;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        self.scroll.setStyleSheet(S_SCROLL())
        self.container.setStyleSheet("background: transparent;")
        self.cargar(self.search_input.text().strip())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cargar(self.search_input.text().strip())


# =============================================================================
#  PÁGINA — RESEÑAS
# =============================================================================

class _PaginaResenas(QWidget):
    def __init__(self, pelicula, usuario_id: int, titulo: str, on_back, parent=None):
        super().__init__(parent)
        self._body = None
        self.setStyleSheet(f"background: {Theme.get('bg_app')};")

        ml = QVBoxLayout(self)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        # Cuerpo: FormReseñas embebido con on_back
        # SIN topbar propio — el título lo muestra la cabecera de FormReseñas
        try:
            from FormReseñas import FormReseñas
            body = FormReseñas(
                pelicula_id     = getattr(pelicula, "id", None) if pelicula else None,
                usuario_id      = usuario_id,
                clase_pelicula  = None,
                clase_resena    = None,
                titulo_pelicula = titulo,
                pelicula_obj    = pelicula,
                on_back         = on_back,
            )
            body.setWindowFlags(Qt.WindowType.Widget)
        except ImportError:
            body = _CuerpoPlaceholder(titulo)

        self._body = body
        body.setStyleSheet(f"background: {Theme.get('bg_app')};")
        ml.addWidget(body, stretch=1)

    def refresh_theme(self):
        self.setStyleSheet(f"background: {Theme.get('bg_app')};")
        if self._body is not None and hasattr(self._body, "refresh_theme"):
            self._body.refresh_theme()


class _CuerpoPlaceholder(QWidget):
    def __init__(self, titulo, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(16)

        icon = QLabel()
        icon.setPixmap(_svg_pixmap(_ico_film(), 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("background: transparent;")
        lay.addWidget(icon)

        lbl = QLabel(f'Reseñas de "{titulo}"')
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(
            f"color: {Theme.get('text_primary')}; font-size: 16px; font-weight: 600;"
            "font-family: 'Segoe UI', sans-serif; background: transparent;"
        )
        lay.addWidget(lbl)

        sub = QLabel("FormResenas.py aún no está disponible.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(
            f"color: {Theme.get('text_muted')}; font-size: 13px; background: transparent;"
        )
        lay.addWidget(sub)


# =============================================================================
#  VENTANA PRINCIPAL
# =============================================================================

class CatalogoWindow(QWidget):
    open_edit    = pyqtSignal(object)
    open_reviews = pyqtSignal(object)

    _IDX_CATALOGO = 0
    _IDX_RESENAS  = 1

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

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setWindowTitle("Cine AI")
        self.setMinimumSize(980, 660)
        self.resize(1200, 720)

        self._build_ui()
        self._pagina_catalogo.cargar()

    def _center(self):
        screen = QApplication.primaryScreen()
        if screen:
            sg = screen.availableGeometry()
            self.move(
                sg.x() + (sg.width()  - self.width())  // 2,
                sg.y() + (sg.height() - self.height()) // 2,
            )

    def _build_ui(self):
        self.setStyleSheet(S_APP())

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._titlebar = TitleBar(window=self)
        self._titlebar.theme_toggled.connect(self._toggle_theme)
        root.addWidget(self._titlebar)

        body = QWidget()
        body.setStyleSheet(f"background: {Theme.get('bg_app')};")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(0, 0, 0, 0)
        body_lay.setSpacing(0)

        # Sidebar
        self._sidebar_frame = QFrame()
        self._sidebar_frame.setObjectName("sidebar")
        self._sidebar_frame.setStyleSheet(S_SIDEBAR())
        self._sidebar_frame.setFixedWidth(220)

        sb = QVBoxLayout(self._sidebar_frame)
        sb.setContentsMargins(12, 0, 12, 20)
        sb.setSpacing(2)

        self._badge = UserBadge(self.usuario, self.rol)
        sb.addWidget(self._badge)

        self._divider = QFrame()
        self._divider.setFrameShape(QFrame.Shape.HLine)
        self._divider.setStyleSheet(
            f"background-color: {Theme.get('border_main')}; border: none; max-height: 1px;"
        )
        sb.addWidget(self._divider)
        sb.addSpacing(10)

        self.btn_inicio  = self._nav_btn(_ico_home(active=True),  "Inicio",      activo=True)
        self.btn_resenas = self._nav_btn(_ico_star(active=False), "Mis Reseñas", activo=False)
        self.btn_inicio.clicked.connect(self._ir_a_inicio)
        self.btn_resenas.clicked.connect(self._abrir_mis_resenas)

        sb.addWidget(self.btn_inicio)
        sb.addWidget(self.btn_resenas)
        sb.addStretch()

        if self.es_admin:
            self.btn_add_sb = QPushButton("  Nueva pelicula")
            self.btn_add_sb.setFixedHeight(40)
            self.btn_add_sb.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_add_sb.setIcon(_svg_icon(_ico_plus(dark=False), 14))
            self.btn_add_sb.setIconSize(QSize(14, 14))
            self.btn_add_sb.setStyleSheet(S_BTN_ADD())
            self.btn_add_sb.clicked.connect(self._abrir_agregar_sidebar)
            sb.addWidget(self.btn_add_sb)
            sb.addSpacing(8)
        else:
            self.btn_add_sb = None

        self.btn_logout = QPushButton("  Cerrar sesión")
        self.btn_logout.setFixedHeight(40)
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.setIcon(_svg_icon(_ico_logout(), 15))
        self.btn_logout.setIconSize(QSize(15, 15))
        self.btn_logout.setStyleSheet(S_BTN_LOGOUT())
        self.btn_logout.clicked.connect(self._logout)
        sb.addWidget(self.btn_logout)

        body_lay.addWidget(self._sidebar_frame)

        # Stack de páginas
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {Theme.get('bg_app')};")

        self._pagina_catalogo = _PaginaCatalogo(es_admin=self.es_admin)
        self._pagina_catalogo.navigate_to_reviews.connect(self._navigate_to_reviews)
        self._stack.addWidget(self._pagina_catalogo)

        self._pagina_resenas_actual = QWidget()
        self._pagina_resenas_actual.setStyleSheet(f"background: {Theme.get('bg_app')};")
        self._stack.addWidget(self._pagina_resenas_actual)

        body_lay.addWidget(self._stack, stretch=1)
        root.addWidget(body, stretch=1)

    def _nav_btn(self, svg: str, texto: str, activo: bool = False) -> QPushButton:
        btn = QPushButton(f"    {texto}")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(40)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setIcon(_svg_icon(svg, 15))
        btn.setIconSize(QSize(15, 15))
        btn.setStyleSheet(S_BTN_NAV(active=activo))
        return btn

    # ── Tema ─────────────────────────────────────────────────────────────────

    def _toggle_theme(self):
        Theme.toggle()
        self._apply_theme_full()

    def _apply_theme_full(self):
        self.setStyleSheet(S_APP())
        self._titlebar.refresh()
        if self.layout() and self.layout().count() > 1:
            body_item = self.layout().itemAt(1)
            if body_item and body_item.widget():
                body_item.widget().setStyleSheet(f"background: {Theme.get('bg_app')};")
        self._sidebar_frame.setStyleSheet(S_SIDEBAR())
        self._divider.setStyleSheet(
            f"background-color: {Theme.get('border_main')}; border: none; max-height: 1px;"
        )
        is_cat = (self._stack.currentIndex() == self._IDX_CATALOGO)
        self.btn_inicio.setStyleSheet(S_BTN_NAV(active=is_cat))
        self.btn_inicio.setIcon(_svg_icon(_ico_home(active=is_cat), 15))
        self.btn_resenas.setStyleSheet(S_BTN_NAV(active=not is_cat))
        self.btn_resenas.setIcon(_svg_icon(_ico_star(active=not is_cat), 15))
        if self.btn_add_sb:
            self.btn_add_sb.setStyleSheet(S_BTN_ADD())
            self.btn_add_sb.setIcon(_svg_icon(_ico_plus(dark=False), 14))
            self.btn_add_sb.setIconSize(QSize(14, 14))
        self.btn_logout.setStyleSheet(S_BTN_LOGOUT())
        self.btn_logout.setIcon(_svg_icon(_ico_logout(), 15))
        self.btn_logout.setIconSize(QSize(15, 15))
        self._stack.setStyleSheet(f"background: {Theme.get('bg_app')};")
        self._pagina_catalogo.refresh_theme()
        curr = self._stack.currentWidget()
        if isinstance(curr, _PaginaResenas):
            curr.refresh_theme()
        self._badge.setStyleSheet("background: transparent;")
        for child in self._badge.findChildren(QLabel):
            if child.objectName() == "avatar":
                child.setStyleSheet(S_AVATAR())

    # ── Navegación ────────────────────────────────────────────────────────────

    def _ir_a_inicio(self):
        self._set_nav("inicio")
        self._pagina_catalogo.cargar()
        self._stack.setCurrentIndex(self._IDX_CATALOGO)

    def _abrir_mis_resenas(self):
        self._set_nav("resenas")
        self._swap_resenas(pelicula=None, titulo="Mis Resenas")

    def _navigate_to_reviews(self, pelicula):
        self.open_reviews.emit(pelicula)
        self._set_nav("resenas")
        titulo = getattr(pelicula, "titulo", "Sin titulo")
        self._swap_resenas(pelicula=pelicula, titulo=titulo)

    def _swap_resenas(self, pelicula, titulo: str):
        old = self._stack.widget(self._IDX_RESENAS)
        if old is not None:
            self._stack.removeWidget(old)
            old.deleteLater()

        nueva = _PaginaResenas(
            pelicula   = pelicula,
            usuario_id = self.usuario_id,
            titulo     = titulo,
            on_back    = self._ir_a_inicio,
        )
        self._stack.insertWidget(self._IDX_RESENAS, nueva)
        self._pagina_resenas_actual = nueva
        self._stack.setCurrentIndex(self._IDX_RESENAS)

    def _set_nav(self, cual: str):
        is_inicio = (cual == "inicio")
        self.btn_inicio.setStyleSheet(S_BTN_NAV(active=is_inicio))
        self.btn_inicio.setIcon(_svg_icon(_ico_home(active=is_inicio), 15))
        self.btn_resenas.setStyleSheet(S_BTN_NAV(active=not is_inicio))
        self.btn_resenas.setIcon(_svg_icon(_ico_star(active=not is_inicio), 15))

    def _abrir_agregar_sidebar(self):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=None, callback=self.refresh, parent=self)
        form.show()

    # ── Logout — diálogo custom sin barra del sistema ─────────────────────────

    def _logout(self):
        confirmado = _CustomDialog.preguntar(
            "Cerrar sesión",
            "¿Deseas cerrar sesión y volver al inicio?",
            btn_si="Sí, salir",
            btn_no="Cancelar",
            parent=self
        )
        if confirmado:
            try:
                from FormLogin import FormLogin
                self._login_win = FormLogin()
                self._login_win.show()
            except ImportError:
                pass
            self.close()

    # ── API pública ───────────────────────────────────────────────────────────

    def refresh(self):
        self._pagina_catalogo.cargar(
            self._pagina_catalogo.search_input.text().strip()
        )

    def showEvent(self, event):
        super().showEvent(event)
        self._center()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._pagina_catalogo.cargar(
            self._pagina_catalogo.search_input.text().strip()
        )


# =============================================================================
#  STANDALONE
# =============================================================================

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