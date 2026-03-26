# catalogoPrincipal.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QGridLayout, QSizePolicy,
    QMessageBox, QApplication, QStackedWidget
)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

import os
import sys

from Json import JsonManager
from rutas import ruta_imagen

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
    explore_clicked = pyqtSignal(object)
    edit_clicked    = pyqtSignal(object)
    delete_clicked  = pyqtSignal(object)

    def __init__(self, pelicula, es_admin=False, parent=None):
        super().__init__(parent)
        self.pelicula = pelicula
        self.es_admin = es_admin
        self._db      = JsonManager()
        self._build()

    def _build(self):
        self.setFixedSize(220, 360 if self.es_admin else 310)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 6)
        root.setSpacing(0)

        # ── Imagen ────────────────────────────────────────────────────
        self.img_label = QLabel()
        self.img_label.setFixedSize(220, 200)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._cargar_imagen()
        self.img_label.mousePressEvent = lambda e: (
            self.explore_clicked.emit(self.pelicula)
            if e.button() == Qt.MouseButton.LeftButton else None
        )
        root.addWidget(self.img_label)

        # ── Título ────────────────────────────────────────────────────
        fila = QHBoxLayout()
        fila.setContentsMargins(8, 4, 8, 0)
        titulo = QLabel(self.pelicula.titulo or "Sin título")
        titulo.setWordWrap(False)
        titulo.setMaximumWidth(170)
        titulo.setSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Preferred)
        fila.addWidget(titulo)
        root.addLayout(fila)

        # ── Año / director ────────────────────────────────────────────
        meta = ""
        if hasattr(self.pelicula, "anio") and self.pelicula.anio:
            meta = str(self.pelicula.anio)
        if hasattr(self.pelicula, "director") and self.pelicula.director:
            meta = (meta + "  ·  " + self.pelicula.director) if meta \
                   else self.pelicula.director
        if meta:
            lbl_meta = QLabel(meta)
            lbl_meta.setContentsMargins(8, 0, 8, 0)
            root.addWidget(lbl_meta)

        # ── Promedio ──────────────────────────────────────────────────
        self.lbl_promedio = QLabel()
        self.lbl_promedio.setContentsMargins(8, 0, 8, 2)
        self._actualizar_promedio()
        root.addWidget(self.lbl_promedio)

        root.addStretch()

        # ── Botón Explorar ────────────────────────────────────────────
        btn_exp = QPushButton("Explore & Review")
        btn_exp.setFixedHeight(28)
        btn_exp.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exp.clicked.connect(lambda: self.explore_clicked.emit(self.pelicula))
        root.addWidget(btn_exp)

        # ── Botones CRUD — solo admin ─────────────────────────────────
        if self.es_admin:
            fila_crud = QHBoxLayout()
            fila_crud.setContentsMargins(8, 4, 8, 0)
            fila_crud.setSpacing(6)

            btn_edit = QPushButton("Editar")
            btn_edit.setFixedHeight(26)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda: self.edit_clicked.emit(self.pelicula))

            btn_del = QPushButton("Eliminar")
            btn_del.setFixedHeight(26)
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda: self.delete_clicked.emit(self.pelicula))

            fila_crud.addWidget(btn_edit)
            fila_crud.addWidget(btn_del)
            root.addLayout(fila_crud)

    def _actualizar_promedio(self):
        pelicula_id = getattr(self.pelicula, "id", None)
        if pelicula_id is None:
            self.lbl_promedio.setText("Promedio: —")
            return

        data     = self._db.obtener_pelicula_por_id(pelicula_id)
        promedio = data.get("promedio_calificacion") if data else None

        if promedio is not None:
            self.lbl_promedio.setText(f"Promedio: {promedio} / 5")
        else:
            self.lbl_promedio.setText("Promedio: sin reseñas")

    def _cargar_imagen(self):
        ruta = ruta_imagen(getattr(self.pelicula, "imagen", None))
        if ruta and os.path.exists(ruta):
            px = QPixmap(ruta)
            if not px.isNull():
                self.img_label.setPixmap(
                    px.scaled(220, 200,
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
                )
                return
        self.img_label.setText((self.pelicula.titulo or "?")[:2].upper())
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


# ══════════════════════════════════════════════════════════════════════
#  DIÁLOGO DETALLE
# ══════════════════════════════════════════════════════════════════════
class DetailDialog(QWidget):
    request_edit    = pyqtSignal(object)
    request_delete  = pyqtSignal(object)
    request_reviews = pyqtSignal(object)

    def __init__(self, pelicula, es_admin=False, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog)
        self.pelicula = pelicula
        self.es_admin = es_admin
        self._build()
        self.setFixedSize(460, 480)

    def _build(self):
        self.setWindowTitle(self.pelicula.titulo or "Detalle")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        img = QLabel()
        img.setFixedSize(428, 200)
        img.setScaledContents(True)
        img.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        ruta = ruta_imagen(getattr(self.pelicula, "imagen", None))
        if ruta and os.path.exists(ruta):
            px = QPixmap(ruta)
            if not px.isNull():
                img.setPixmap(px)
        else:
            img.setText((self.pelicula.titulo or "?")[:2].upper())
            img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.mousePressEvent = lambda e: (
            (self.request_reviews.emit(self.pelicula), self.close())
            if e.button() == Qt.MouseButton.LeftButton else None
        )
        layout.addWidget(img)

        titulo = QLabel(self.pelicula.titulo or "Sin título")
        layout.addWidget(titulo)

        metas = []
        if getattr(self.pelicula, "anio",     None): metas.append(str(self.pelicula.anio))
        if getattr(self.pelicula, "director", None): metas.append(self.pelicula.director)
        if getattr(self.pelicula, "fecha",    None): metas.append(self.pelicula.fecha)
        if metas:
            layout.addWidget(QLabel("  ·  ".join(metas)))

        if getattr(self.pelicula, "descripcion", None):
            desc = QLabel(self.pelicula.descripcion)
            desc.setWordWrap(True)
            layout.addWidget(desc)

        layout.addStretch()

        btns = QHBoxLayout()
        btns.setSpacing(8)

        btn_review = QPushButton("Explore & Review")
        btn_review.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_review.clicked.connect(lambda: (
            self.request_reviews.emit(self.pelicula), self.close()
        ))
        btns.addWidget(btn_review)

        if self.es_admin:
            btn_edit = QPushButton("Editar")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda: (
                self.request_edit.emit(self.pelicula), self.close()
            ))

            btn_del = QPushButton("Eliminar")
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda: (
                self.request_delete.emit(self.pelicula), self.close()
            ))

            btns.addWidget(btn_edit)
            btns.addWidget(btn_del)

        btns.addStretch()

        btn_close = QPushButton("Cerrar")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.close)
        btns.addWidget(btn_close)

        layout.addLayout(btns)


# ══════════════════════════════════════════════════════════════════════
#  TARJETA "AGREGAR PELÍCULA"  (solo admin)
# ══════════════════════════════════════════════════════════════════════
class AddMovieCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 340)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        icon = QLabel("+")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        text = QLabel("Agregar película")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

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
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 12, 4)
        layout.setSpacing(8)

        avatar = QLabel(nombre[0].upper() if nombre else "?")
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(avatar)

        info = QVBoxLayout()
        info.setSpacing(0)
        info.setContentsMargins(0, 0, 0, 0)

        lbl_nombre  = QLabel(nombre)
        rol_display = "Administrador" if rol == "admin" else "Lector"
        lbl_rol     = QLabel(rol_display)

        info.addWidget(lbl_nombre)
        info.addWidget(lbl_rol)
        layout.addLayout(info)


# ══════════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL DEL CATÁLOGO
# ══════════════════════════════════════════════════════════════════════
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

        self.setWindowTitle("CineLog — Catálogo")
        self.setMinimumSize(900, 620)
        self._build_ui()
        self._cargar_catalogo()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        # ── Header ────────────────────────────────────────────────────
        header = QHBoxLayout()

        welcome = QLabel("CineLog — Catálogo")
        header.addWidget(welcome)
        header.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar películas...")
        self.search_input.setFixedSize(220, 28)
        self.search_input.textChanged.connect(self._on_search)
        header.addWidget(self.search_input)

        if self.es_admin:
            btn_add = QPushButton("+ Añadir película")
            btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_add.clicked.connect(self._abrir_agregar)
            header.addSpacing(8)
            header.addWidget(btn_add)

        header.addSpacing(10)
        header.addWidget(UserBadge(self.usuario, self.rol))
        root.addLayout(header)

        self.count_label = QLabel()
        root.addWidget(self.count_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.grid_container)
        root.addWidget(scroll)

        self.empty_label = QLabel("No hay películas.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.hide()
        root.addWidget(self.empty_label)

    # ── Grid ──────────────────────────────────────────────────────────
    def _cargar_catalogo(self, query=""):
        peliculas = _search(query) if query else _get_all()
        self._render_grid(peliculas)

    def _render_grid(self, peliculas):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        COLS = max(1, (self.width() - 48) // 240)

        if not peliculas:
            self.count_label.setText("0 películas")
            if self.es_admin:
                add_card = AddMovieCard()
                add_card.clicked.connect(self._abrir_agregar)
                self.grid_layout.addWidget(add_card, 0, 0)
            return

        self.count_label.setText(
            f"{len(peliculas)} película{'s' if len(peliculas) != 1 else ''}"
        )

        for i, peli in enumerate(peliculas):
            card = MovieCard(peli, es_admin=self.es_admin)
            card.explore_clicked.connect(self._navigate_to_reviews)
            card.edit_clicked.connect(self._abrir_editar)
            card.delete_clicked.connect(self._confirmar_eliminar)
            self.grid_layout.addWidget(card, i // COLS, i % COLS)

        if self.es_admin:
            add_card = AddMovieCard()
            add_card.clicked.connect(self._abrir_agregar)
            next_pos = len(peliculas)
            self.grid_layout.addWidget(add_card, next_pos // COLS, next_pos % COLS)

    def _on_search(self, text):
        self._cargar_catalogo(text.strip())

    # ── Acciones CRUD ─────────────────────────────────────────────────
    def _abrir_agregar(self):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=None, callback=self.refresh, parent=self)
        form.show()

    def _abrir_editar(self, pelicula):
        from peliculaUI import PeliculaUI
        form = PeliculaUI(pelicula=pelicula, callback=self.refresh, parent=self)
        form.show()

    def _confirmar_eliminar(self, pelicula):
        r = QMessageBox.question(
            self, "Eliminar película",
            f"¿Eliminar «{pelicula.titulo}»?\nTambién se borrarán sus reseñas.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r == QMessageBox.StandardButton.Yes:
            _del(pelicula)
            self.refresh()

    # ── Detalle ───────────────────────────────────────────────────────
    def _show_detail(self, pelicula):
        dlg = DetailDialog(pelicula, es_admin=self.es_admin, parent=self)
        dlg.request_edit.connect(self._abrir_editar)
        dlg.request_delete.connect(self._confirmar_eliminar)
        dlg.request_reviews.connect(self._navigate_to_reviews)
        geo = self.geometry()
        dlg.move(
            geo.x() + (geo.width()  - dlg.width())  // 2,
            geo.y() + (geo.height() - dlg.height()) // 2,
        )
        dlg.show()

    # ── Reseñas ───────────────────────────────────────────────────────
    def _navigate_to_reviews(self, pelicula):
        self.open_reviews.emit(pelicula)
        pelicula_id     = getattr(pelicula, "id",     None)
        titulo_pelicula = getattr(pelicula, "titulo", "Sin título")

        try:
            from FormReseñas import FormResenas
            form = FormResenas(
                pelicula_id     = pelicula_id,
                usuario_id      = self.usuario_id,
                clase_pelicula  = None,
                clase_resena    = None,
                titulo_pelicula = titulo_pelicula,
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

        # Al cerrar FormResenas, refrescar catálogo para actualizar promedios
        form.destroyed.connect(lambda: self.refresh())

        form.show()
        form.raise_()
        form.activateWindow()

    # ── API pública ───────────────────────────────────────────────────
    def refresh(self):
        self._cargar_catalogo(self.search_input.text().strip())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cargar_catalogo(self.search_input.text().strip())


# ══════════════════════════════════════════════════════════════════════
#  PLACEHOLDER
# ══════════════════════════════════════════════════════════════════════
class _PlaceholderReviews(QWidget):
    closed = pyqtSignal()

    def __init__(self, pelicula, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Reseñas — {pelicula.titulo}")
        self.setMinimumSize(900, 620)

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(f"{pelicula.titulo}\nFormResenas.py aún no está disponible.")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl)

        btn_back = QPushButton("← Volver al catálogo")
        btn_back.setFixedSize(200, 36)
        btn_back.clicked.connect(self._cerrar)
        lay.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

    def _cerrar(self):
        self.closed.emit()
        self.close()


# ══════════════════════════════════════════════════════════════════════
#  STANDALONE
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    usuario = sys.argv[1] if len(sys.argv) > 1 else "pablo_99"
    rol     = sys.argv[2] if len(sys.argv) > 2 else "lector"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        db = JsonManager()
        if not db.obtener_peliculas():
            demos = [
                ("Inception",         "Un ladrón que roba secretos en sueños.",  None, "2010-07-16", 2010, "Christopher Nolan"),
                ("The Matrix",        "Un hacker descubre la verdad del mundo.", None, "1999-03-31", 1999, "Wachowski Sisters"),
                ("Dune",              "La épica batalla por Arrakis.",            None, "2021-10-22", 2021, "Denis Villeneuve"),
                ("Interstellar",      "Viaje por un agujero de gusano.",          None, "2014-11-07", 2014, "Christopher Nolan"),
                ("Blade Runner 2049", "Un blade runner descubre un secreto.",     None, "2017-10-06", 2017, "Denis Villeneuve"),
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