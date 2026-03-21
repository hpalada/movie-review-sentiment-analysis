#catalogoPrincipal.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QGridLayout, QSizePolicy,
    QMessageBox, QApplication, QGraphicsOpacityEffect, QStackedWidget
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette, QCursor, QIcon
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve, QRect

import os
import sys

# ── Importamos la capa de modelo ──────────────────────────────────────
try:
    from clasePelicula import Pelicula
    def _get_all():  return Pelicula.todas()
    def _search(q):
        return [p for p in Pelicula.todas()
                if q.lower() in p.titulo.lower()]
    def _del(p): p.eliminar()
    USE_MODEL = True
except ImportError:
    from Json import JsonManager
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


# ══════════════════════════════════════════════════════════════════════
#  TARJETA DE PELÍCULA
# ══════════════════════════════════════════════════════════════════════
class MovieCard(QFrame):
    # Emite el objeto pelicula al hacer clic en imagen O en el botón
    explore_clicked = pyqtSignal(object)
    deleted         = pyqtSignal(object)

    def __init__(self, pelicula, parent=None):
        super().__init__(parent)
        self.pelicula = pelicula
        self._build()

    def _build(self):
        self.setFixedSize(220, 280)
        self.setObjectName("MovieCard")
        self.setStyleSheet("""
            QFrame#MovieCard {
                background: #1e2130;
                border-radius: 14px;
                border: 1px solid #2a2f45;
            }
            QFrame#MovieCard:hover {
                border: 1px solid #00c8b4;
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 12)
        root.setSpacing(0)

        # ── Imagen (clicable) ─────────────────────────────────────────
        self.img_label = QLabel()
        self.img_label.setFixedSize(220, 160)
        self.img_label.setScaledContents(True)
        self.img_label.setStyleSheet(
            "border-top-left-radius: 14px;"
            "border-top-right-radius: 14px;"
            "background: #12141f;"
        )
        self.img_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._cargar_imagen()

        # Clic en la imagen → misma señal que el botón
        self.img_label.mousePressEvent = lambda e: (
            self.explore_clicked.emit(self.pelicula)
            if e.button() == Qt.MouseButton.LeftButton else None
        )
        root.addWidget(self.img_label)

        # ── Fila título + estrella ────────────────────────────────────
        fila = QHBoxLayout()
        fila.setContentsMargins(10, 8, 10, 4)

        titulo = QLabel(self.pelicula.titulo or "Sin título")
        titulo.setStyleSheet("color:#e8eaf0; font-size:13px; font-weight:600;")
        titulo.setWordWrap(False)
        titulo.setMaximumWidth(170)
        titulo.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Preferred)

        star = QLabel("★")
        star.setStyleSheet("color:#00c8b4; font-size:16px;")
        star.setFixedWidth(20)

        fila.addWidget(titulo)
        fila.addWidget(star)
        root.addLayout(fila)

        # Año / director (opcional)
        meta = ""
        if hasattr(self.pelicula, "anio") and self.pelicula.anio:
            meta = str(self.pelicula.anio)
        if hasattr(self.pelicula, "director") and self.pelicula.director:
            meta = (meta + "  ·  " + self.pelicula.director) if meta \
                   else self.pelicula.director
        if meta:
            lbl_meta = QLabel(meta)
            lbl_meta.setContentsMargins(10, 0, 10, 2)
            lbl_meta.setStyleSheet("color:#6b7080; font-size:11px;")
            root.addWidget(lbl_meta)

        root.addStretch()

        # ── Botón Explorar ────────────────────────────────────────────
        btn = QPushButton("Explore & Review")
        btn.setFixedHeight(32)
        btn.setStyleSheet("""
            QPushButton {
                background: #00c8b4;
                color: #0d0f1a;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 700;
                margin: 0 10px;
            }
            QPushButton:hover { background: #00e5cf; }
            QPushButton:pressed { background: #009e8d; }
        """)
        btn.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        root.addWidget(btn)

    def _cargar_imagen(self):
        ruta = getattr(self.pelicula, "imagen", None)
        if ruta and os.path.exists(ruta):
            px = QPixmap(ruta)
            if not px.isNull():
                self.img_label.setPixmap(px)
                return
        self.img_label.setText(
            (self.pelicula.titulo or "?")[:2].upper()
        )
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setStyleSheet(
            "border-top-left-radius:14px; border-top-right-radius:14px;"
            "background:#12141f; color:#2a2f45; font-size:40px; font-weight:800;"
        )


# ══════════════════════════════════════════════════════════════════════
#  DIÁLOGO DETALLE
# ══════════════════════════════════════════════════════════════════════
class DetailDialog(QWidget):
    request_edit    = pyqtSignal(object)
    request_delete  = pyqtSignal(object)
    request_reviews = pyqtSignal(object)

    def __init__(self, pelicula, parent=None):
        super().__init__(parent,
            Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.pelicula = pelicula
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build()
        self.setFixedSize(460, 540)

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #1a1d2e;
                border-radius: 18px;
                border: 1px solid #2a2f45;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)

        img = QLabel()
        img.setFixedSize(460, 240)
        img.setScaledContents(True)
        img.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        img.setStyleSheet(
            "border-top-left-radius:18px; border-top-right-radius:18px;"
            "background:#12141f;"
        )
        ruta = getattr(self.pelicula, "imagen", None)
        if ruta and os.path.exists(ruta):
            px = QPixmap(ruta)
            if not px.isNull():
                img.setPixmap(px)
        else:
            img.setText((self.pelicula.titulo or "?")[:2].upper())
            img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img.setStyleSheet(
                "border-top-left-radius:18px; border-top-right-radius:18px;"
                "background:#12141f; color:#2a2f45; font-size:60px; font-weight:900;"
            )

        img.mousePressEvent = lambda e: (
            (self.request_reviews.emit(self.pelicula), self.close())
            if e.button() == Qt.MouseButton.LeftButton else None
        )
        layout.addWidget(img)

        content = QVBoxLayout()
        content.setContentsMargins(24, 16, 24, 0)
        content.setSpacing(8)

        titulo = QLabel(self.pelicula.titulo or "Sin título")
        titulo.setStyleSheet("color:#e8eaf0; font-size:22px; font-weight:800;")
        content.addWidget(titulo)

        metas = []
        if getattr(self.pelicula, "anio", None):
            metas.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None):
            metas.append(self.pelicula.director)
        if getattr(self.pelicula, "fecha", None):
            metas.append(self.pelicula.fecha)
        if metas:
            meta_lbl = QLabel("  ·  ".join(metas))
            meta_lbl.setStyleSheet("color:#00c8b4; font-size:12px;")
            content.addWidget(meta_lbl)

        if getattr(self.pelicula, "descripcion", None):
            desc = QLabel(self.pelicula.descripcion)
            desc.setWordWrap(True)
            desc.setStyleSheet("color:#9097b0; font-size:13px;")
            content.addWidget(desc)

        content.addStretch()

        btns = QHBoxLayout()
        btns.setSpacing(10)

        btn_review = QPushButton("⭐  Explore & Review")
        btn_review.setFixedHeight(36)
        btn_review.setStyleSheet("""
            QPushButton {
                background:#00c8b4; color:#0d0f1a;
                border:none; border-radius:8px;
                font-size:13px; font-weight:700;
            }
            QPushButton:hover { background:#00e5cf; }
        """)
        btn_review.clicked.connect(lambda: (
            self.request_reviews.emit(self.pelicula), self.close()
        ))

        btn_edit = QPushButton("✏  Editar")
        btn_edit.setFixedHeight(36)
        btn_edit.setStyleSheet("""
            QPushButton {
                background:#2a2f45; color:#e8eaf0;
                border:none; border-radius:8px;
                font-size:13px; font-weight:600;
            }
            QPushButton:hover { background:#3a4060; }
        """)
        btn_edit.clicked.connect(lambda: (
            self.request_edit.emit(self.pelicula), self.close()
        ))

        btn_del = QPushButton("🗑  Eliminar")
        btn_del.setFixedHeight(36)
        btn_del.setStyleSheet("""
            QPushButton {
                background:#3d1a1a; color:#e05555;
                border:1px solid #7a2222; border-radius:8px;
                font-size:13px; font-weight:600;
            }
            QPushButton:hover { background:#5a2020; }
        """)
        btn_del.clicked.connect(lambda: (
            self.request_delete.emit(self.pelicula), self.close()
        ))

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(36, 36)
        btn_close.setStyleSheet("""
            QPushButton {
                background:#2a2f45; color:#9097b0;
                border:none; border-radius:8px; font-size:14px;
            }
            QPushButton:hover { background:#3a4060; color:#e8eaf0; }
        """)
        btn_close.clicked.connect(self.close)

        btns.addWidget(btn_review)
        btns.addWidget(btn_edit)
        btns.addWidget(btn_del)
        btns.addStretch()
        btns.addWidget(btn_close)
        content.addLayout(btns)

        layout.addLayout(content)
        outer.addWidget(card)


# ══════════════════════════════════════════════════════════════════════
#  TARJETA "AGREGAR PELÍCULA"  (solo visible para admin)
# ══════════════════════════════════════════════════════════════════════
class AddMovieCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 280)
        self.setObjectName("AddMovieCard")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QFrame#AddMovieCard {
                background: #13162200;
                border-radius: 14px;
                border: 2px dashed #2a2f45;
            }
            QFrame#AddMovieCard:hover {
                background: #1a1f3a;
                border: 2px dashed #00c8b4;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel("＋")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("color:#2a2f45; font-size:52px; font-weight:300; border:none;")
        icon.setObjectName("AddIcon")

        text = QLabel("Agregar película")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet("color:#3a4565; font-size:13px; font-weight:600; border:none;")
        text.setObjectName("AddText")

        layout.addWidget(icon)
        layout.addWidget(text)
        self._icon = icon
        self._text = text

    def enterEvent(self, event):
        self._icon.setStyleSheet("color:#00c8b4; font-size:52px; font-weight:300; border:none;")
        self._text.setStyleSheet("color:#00c8b4; font-size:13px; font-weight:600; border:none;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._icon.setStyleSheet("color:#2a2f45; font-size:52px; font-weight:300; border:none;")
        self._text.setStyleSheet("color:#3a4565; font-size:13px; font-weight:600; border:none;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


# ══════════════════════════════════════════════════════════════════════
#  BADGE DE USUARIO
# ══════════════════════════════════════════════════════════════════════
class UserBadge(QFrame):
    def __init__(self, nombre: str, rol: str, parent=None):
        super().__init__(parent)
        self.setObjectName("UserBadge")
        self.setStyleSheet("""
            QFrame#UserBadge {
                background: #1e2130;
                border-radius: 20px;
                border: 1px solid #2a2f45;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 14, 6)
        layout.setSpacing(8)

        avatar = QLabel(nombre[0].upper() if nombre else "?")
        avatar.setFixedSize(30, 30)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_avatar = "#00c8b4" if rol == "admin" else "#6b7080"
        avatar.setStyleSheet(f"""
            background: {color_avatar};
            color: #0d0f1a;
            border-radius: 15px;
            font-size: 14px;
            font-weight: 800;
        """)

        info = QVBoxLayout()
        info.setSpacing(0)
        info.setContentsMargins(0, 0, 0, 0)

        lbl_nombre = QLabel(nombre)
        lbl_nombre.setStyleSheet(
            "color:#e8eaf0; font-size:12px; font-weight:700;"
            "background:transparent; border:none;"
        )

        rol_display = "Administrador" if rol == "admin" else "Lector"
        rol_color   = "#00c8b4"       if rol == "admin" else "#6b7080"
        lbl_rol = QLabel(rol_display)
        lbl_rol.setStyleSheet(
            f"color:{rol_color}; font-size:10px; font-weight:500;"
            "background:transparent; border:none;"
        )

        info.addWidget(lbl_nombre)
        info.addWidget(lbl_rol)
        layout.addWidget(avatar)
        layout.addLayout(info)


# ══════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL DEL CATÁLOGO
# ══════════════════════════════════════════════════════════════════════
class CatalogoWindow(QWidget):
    """
    Parámetros
    ----------
    usuario : str | dict
        Acepta un string simple ("pablo_99") O el dict completo que
        devuelve ClaseLogin:
            { "nombre_usuario": str, "id": int, "rol": str, ... }
    rol : str
        "admin" o "lector".  Se ignora si usuario es dict y ya tiene "rol".
    """

    open_edit    = pyqtSignal(object)
    open_reviews = pyqtSignal(object)

    def __init__(self, usuario="usuario", rol: str = "lector", parent=None):
        super().__init__(parent)

        # ── Normalizar usuario (str o dict) ───────────────────────────
        if isinstance(usuario, dict):
            self.usuario_dict = usuario
            self.usuario      = usuario.get("nombre_usuario", "usuario")
            rol_raw           = str(usuario.get("rol", rol)).lower().strip()
        else:
            self.usuario_dict = {"nombre_usuario": usuario, "id": None, "rol": rol}
            self.usuario      = usuario
            rol_raw           = str(rol).lower().strip()

        self.rol        = "admin" if rol_raw in ("admin", "administrador") else "lector"
        # ID numérico del usuario activo → FormResenas lo necesita
        self.usuario_id = self.usuario_dict.get("id") or 0

        self.setWindowTitle("CineLog — Catálogo")
        self.setMinimumSize(900, 620)
        self._setup_palette()
        self._build_ui()
        self._cargar_catalogo()

    def _setup_palette(self):
        self.setStyleSheet("background:#0d0f1a;")

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────
        header = QHBoxLayout()

        welcome = QLabel()
        welcome.setText(
            f'<span style="color:#e8eaf0; font-size:22px; font-weight:700;">CineLog — </span>'
            f'<span style="color:#00c8b4; font-size:22px; font-weight:700;">Catálogo</span>'
        )
        header.addWidget(welcome)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search Movies...")
        self.search_input.setFixedSize(240, 38)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background:#1e2130;
                border: 1px solid #2a2f45;
                border-radius: 19px;
                padding: 0 16px;
                color: #e8eaf0;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #00c8b4; }
        """)
        self.search_input.textChanged.connect(self._on_search)
        header.addWidget(self.search_input)

        if self.rol == "admin":
            btn_add = QPushButton("＋ Añadir película")
            btn_add.setFixedHeight(38)
            btn_add.setStyleSheet("""
                QPushButton {
                    background:#00c8b4; color:#0d0f1a;
                    border:none; border-radius:10px;
                    font-size:13px; font-weight:700;
                    padding: 0 18px;
                }
                QPushButton:hover { background:#00e5cf; }
            """)
            btn_add.clicked.connect(lambda: self.open_edit.emit(None))
            header.addSpacing(10)
            header.addWidget(btn_add)

        header.addSpacing(12)
        badge = UserBadge(self.usuario, self.rol)
        header.addWidget(badge)

        root.addLayout(header)

        self.count_label = QLabel()
        self.count_label.setStyleSheet("color:#6b7080; font-size:12px;")
        root.addWidget(self.count_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; }
            QScrollBar:vertical {
                background:#1a1d2e; width:6px; border-radius:3px;
            }
            QScrollBar::handle:vertical {
                background:#2a2f45; border-radius:3px;
            }
            QScrollBar::handle:vertical:hover { background:#00c8b4; }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height:0; }
        """)

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.grid_container)
        root.addWidget(scroll)

        self.empty_label = QLabel("No hay películas.\nUsa '＋ Añadir película' para comenzar.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color:#3a4060; font-size:16px;")
        self.empty_label.hide()
        root.addWidget(self.empty_label)

    # ── Carga del grid ────────────────────────────────────────────────
    def _cargar_catalogo(self, query=""):
        peliculas = _search(query) if query else _get_all()
        self._render_grid(peliculas)

    def _render_grid(self, peliculas):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not peliculas:
            self.empty_label.hide()
            self.count_label.setText("0 películas")
            if self.rol == "admin":
                add_card = AddMovieCard()
                add_card.clicked.connect(lambda: self.open_edit.emit(None))
                self.grid_layout.addWidget(add_card, 0, 0)
            return

        self.empty_label.hide()
        self.count_label.setText(
            f"{len(peliculas)} película{'s' if len(peliculas) != 1 else ''}"
        )

        COLS = max(1, (self.width() - 48) // 240)
        for i, peli in enumerate(peliculas):
            card = MovieCard(peli)
            # imagen Y botón emiten explore_clicked → va a _navigate_to_reviews
            card.explore_clicked.connect(self._navigate_to_reviews)
            self.grid_layout.addWidget(card, i // COLS, i % COLS)

        if self.rol == "admin":
            add_card = AddMovieCard()
            add_card.clicked.connect(lambda: self.open_edit.emit(None))
            next_pos  = len(peliculas)
            self.grid_layout.addWidget(add_card, next_pos // COLS, next_pos % COLS)
            total     = len(peliculas) + 1
            remainder = total % COLS
            if remainder:
                for j in range(COLS - remainder):
                    spacer = QWidget()
                    spacer.setFixedSize(220, 280)
                    spacer.setStyleSheet("background:transparent;")
                    self.grid_layout.addWidget(spacer, total // COLS, remainder + j)
        else:
            remainder = len(peliculas) % COLS
            if remainder:
                for j in range(COLS - remainder):
                    spacer = QWidget()
                    spacer.setFixedSize(220, 280)
                    spacer.setStyleSheet("background:transparent;")
                    self.grid_layout.addWidget(
                        spacer, len(peliculas) // COLS, remainder + j)

    def _on_search(self, text):
        self._cargar_catalogo(text.strip())

    def _show_detail(self, pelicula):
        dlg = DetailDialog(pelicula, self)
        dlg.request_edit.connect(self.open_edit.emit)
        dlg.request_delete.connect(self._confirmar_eliminar)
        dlg.request_reviews.connect(self._navigate_to_reviews)
        geo = self.geometry()
        dlg.move(
            geo.x() + (geo.width()  - dlg.width())  // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.show()

    # ══════════════════════════════════════════════════════════════════
    #  NAVEGACIÓN → FormResenas  (ventana independiente)
    # ══════════════════════════════════════════════════════════════════

    def _navigate_to_reviews(self, pelicula):
        """Abre FormResenas como ventana independiente sin tocar el catálogo."""
        self.open_reviews.emit(pelicula)

        pelicula_id     = getattr(pelicula, "id",     None)
        titulo_pelicula = getattr(pelicula, "titulo", "Sin título")

        try:
            from FormReseñas import FormResenas
            
            form = FormResenas(
                pelicula_id     = pelicula_id,
                usuario_id      = self.usuario_id,   # ← agregar esta línea
                clase_pelicula  = None,
                clase_resena    = None,
                titulo_pelicula = titulo_pelicula,
                pelicula_obj    = pelicula,
            )
        except ImportError:
            form = _PlaceholderReviews(pelicula, self.usuario)

        # Guardar referencia para que Python no destruya la ventana al salir
        # del scope — sin esto la ventana parpadea y desaparece inmediatamente
        if not hasattr(self, "_ventanas_resenas"):
            self._ventanas_resenas = []
        self._ventanas_resenas.append(form)

        # Cuando se cierre, limpiar la referencia de la lista
        form.destroyed.connect(
            lambda obj=form: self._ventanas_resenas.remove(obj)
            if obj in self._ventanas_resenas else None
        )

        form.show()
        form.raise_()
        form.activateWindow()

    # ── Eliminar película ─────────────────────────────────────────────
    def _confirmar_eliminar(self, pelicula):
        r = QMessageBox.question(
            self, "Eliminar",
            f"¿Eliminar «{pelicula.titulo}»?\nTambién se borrarán sus reseñas.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r == QMessageBox.StandardButton.Yes:
            _del(pelicula)
            self.refresh()

    # ── API pública ───────────────────────────────────────────────────
    def refresh(self):
        self._cargar_catalogo(self.search_input.text().strip())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cargar_catalogo(self.search_input.text().strip())


# ══════════════════════════════════════════════════════════════════════
#  PLACEHOLDER  (mientras FormResenas.py no exista)
# ══════════════════════════════════════════════════════════════════════
class _PlaceholderReviews(QWidget):
    closed = pyqtSignal()

    def __init__(self, pelicula, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Reseñas — {pelicula.titulo}")
        self.setStyleSheet("background:#0d0f1a;")
        self.setMinimumSize(900, 620)

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(
            f'<div style="text-align:center;">'
            f'<span style="color:#00c8b4; font-size:28px; font-weight:800;">'
            f'{pelicula.titulo}</span><br>'
            f'<span style="color:#6b7080; font-size:14px;">'
            f'FormResenas.py aún no está disponible.</span>'
            f'</div>'
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl)

        btn_back = QPushButton("← Volver al catálogo")
        btn_back.setFixedSize(220, 40)
        btn_back.setStyleSheet("""
            QPushButton {
                background:#1e2130; color:#00c8b4;
                border:1px solid #00c8b4; border-radius:10px;
                font-size:13px; font-weight:700;
            }
            QPushButton:hover { background:#00c8b4; color:#0d0f1a; }
        """)
        btn_back.clicked.connect(self._cerrar)
        lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    def _cerrar(self):
        self.closed.emit()
        self.close()


# ══════════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA STANDALONE
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    usuario = sys.argv[1] if len(sys.argv) > 1 else "pablo_99"
    rol     = sys.argv[2] if len(sys.argv) > 2 else "lector"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        from Json import JsonManager
        db = JsonManager()
        if not db.obtener_peliculas():
            demos = [
                ("Inception",         "Un ladrón que roba secretos en sueños.",   None, "2010-07-16", 2010, "Christopher Nolan"),
                ("The Matrix",        "Un hacker descubre la verdad del mundo.",   None, "1999-03-31", 1999, "Wachowski Sisters"),
                ("Dune",              "La épica batalla por el planeta Arrakis.",  None, "2021-10-22", 2021, "Denis Villeneuve"),
                ("Interstellar",      "Viaje a través de un agujero de gusano.",   None, "2014-11-07", 2014, "Christopher Nolan"),
                ("Blade Runner 2049", "Un blade runner descubre un secreto.",      None, "2017-10-06", 2017, "Denis Villeneuve"),
            ]
            for t, d, img, f, a, dir_ in demos:
                db.agregar_pelicula(t, d, img, f, a, dir_)
    except Exception as e:
        print(f"Demo data skipped: {e}")

    win = CatalogoWindow(usuario=usuario, rol=rol)
    win.open_edit.connect(lambda p: print(
        f"[open_edit] {'nueva película' if not p else p.titulo}"
    ))
    win.open_reviews.connect(lambda p: print(f"[open_reviews] {p.titulo}"))
    win.show()
    sys.exit(app.exec())