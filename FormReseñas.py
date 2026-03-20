from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class FormResenas(QWidget):
    def __init__(self, pelicula_id: int, usuario_id: int, clase_pelicula,
                 clase_resena, titulo_pelicula: str = ""):
        super().__init__()
        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_pelicula  = clase_pelicula
        self.clase_resena    = clase_resena
        self.titulo_pelicula = titulo_pelicula

        self.setWindowTitle("Reseñas")
        self.resize(1100, 750)
        self._construir_ui()
        self._cargar_datos()

    # ─────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA UI
    # ─────────────────────────────────────────

    def _construir_ui(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.contenido_scroll = QWidget()
        self.layout_scroll    = QVBoxLayout(self.contenido_scroll)
        self.layout_scroll.setContentsMargins(20, 20, 20, 20)
        self.layout_scroll.setSpacing(16)

        self.widget_cabecera = self._crear_cabecera()
        self.layout_scroll.addWidget(self.widget_cabecera)

        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        self.layout_scroll.addWidget(separador)

        self.layout_resenas = QVBoxLayout()
        self.layout_resenas.setSpacing(12)
        self.layout_scroll.addLayout(self.layout_resenas)

        self.layout_scroll.addStretch()

        self.scroll_area.setWidget(self.contenido_scroll)
        layout_raiz.addWidget(self.scroll_area)

        self.btn_agregar = QPushButton("AGREGAR RESEÑA")
        self.btn_agregar.setFixedHeight(55)
        self.btn_agregar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_agregar.clicked.connect(self._abrir_form_agregar)
        layout_raiz.addWidget(self.btn_agregar)

    def _crear_cabecera(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        self.lbl_poster = QLabel("POSTER")
        self.lbl_poster.setFixedSize(190, 270)
        self.lbl_poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_poster.setFrameShape(QFrame.Shape.Box)
        layout.addWidget(self.lbl_poster)

        layout_info = QVBoxLayout()
        layout_info.setSpacing(8)

        self.lbl_nombre    = QLabel(self.titulo_pelicula or "NOMBRE PELÍCULA")
        self.lbl_promedio  = QLabel("RESEÑA AVERAGE")
        self.lbl_etiquetas = QLabel("ETIQUETA AVERAGE")

        layout_info.addWidget(self.lbl_nombre)
        layout_info.addWidget(self.lbl_promedio)
        layout_info.addWidget(self.lbl_etiquetas)
        layout_info.addStretch()

        layout.addLayout(layout_info)
        layout.addStretch()

        return widget

    # ─────────────────────────────────────────
    #  CARGA DE DATOS
    # ─────────────────────────────────────────

    def _cargar_datos(self):
        self._cargar_info_pelicula()
        self._cargar_resenas()

    def _cargar_info_pelicula(self):
        # Si no hay capa intermedia aún, usamos el título que llegó por parámetro
        if not self.clase_pelicula:
            self.lbl_nombre.setText(self.titulo_pelicula or "Sin título")
            return

        info = self.clase_pelicula.obtener_info_pelicula(self.pelicula_id)
        if not info:
            return

        self.lbl_nombre.setText(info.get("titulo", "Sin título"))
        self.lbl_promedio.setText(f"Valoración promedio: {info.get('promedio', 'N/A')} / 5")
        self.lbl_etiquetas.setText(f"Etiquetas: {', '.join(info.get('etiquetas_frecuentes', []))}")

        ruta_poster = info.get("poster", None)
        if ruta_poster:
            pixmap = QPixmap(ruta_poster)
            if not pixmap.isNull():
                self.lbl_poster.setPixmap(
                    pixmap.scaled(190, 270, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
                )

    def _cargar_resenas(self):
        while self.layout_resenas.count():
            item = self.layout_resenas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        resenas = self.clase_resena.obtener_resenas_pelicula(self.pelicula_id)

        if not resenas:
            lbl_vacio = QLabel("Aún no hay reseñas para esta película.")
            lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout_resenas.addWidget(lbl_vacio)
            return

        for resena in resenas:
            tarjeta = self._crear_tarjeta(resena)
            self.layout_resenas.addWidget(tarjeta)

    # ─────────────────────────────────────────
    #  TARJETA DE RESEÑA
    # ─────────────────────────────────────────

    def _crear_tarjeta(self, resena: dict) -> QFrame:
        tarjeta = QFrame()
        tarjeta.setFrameShape(QFrame.Shape.StyledPanel)

        layout_tarjeta = QHBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(12, 12, 12, 12)
        layout_tarjeta.setSpacing(12)

        # ── Columna izquierda: usuario + texto ──
        layout_texto = QVBoxLayout()
        layout_texto.setSpacing(4)

        lbl_usuario = QLabel(resena.get("nombre_usuario", f"Usuario {resena['usuario_id']}"))
        lbl_texto   = QLabel(resena.get("texto", "")[:120] + "...")
        lbl_texto.setWordWrap(True)
        lbl_leer    = QLabel("leer más...")
        lbl_leer.setCursor(Qt.CursorShape.PointingHandCursor)

        layout_texto.addWidget(lbl_usuario)
        layout_texto.addWidget(lbl_texto)
        layout_texto.addWidget(lbl_leer)
        layout_tarjeta.addLayout(layout_texto, stretch=5)

        # ── Columna central: etiquetas ──
        layout_etiquetas = QVBoxLayout()
        layout_etiquetas.setSpacing(4)

        for etiqueta in resena.get("etiquetas_ia", []):
            lbl_etiqueta = QLabel(etiqueta)
            lbl_etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_etiqueta.setFrameShape(QFrame.Shape.Box)
            lbl_etiqueta.setFixedHeight(28)
            layout_etiquetas.addWidget(lbl_etiqueta)

        layout_etiquetas.addStretch()
        layout_tarjeta.addLayout(layout_etiquetas, stretch=2)

        # ── Columna derecha: valoración + botón editar ──
        layout_derecha = QVBoxLayout()
        layout_derecha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_valoracion = QLabel(f"{resena.get('valoracion_ia', '?')} / 5")
        lbl_valoracion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecha.addWidget(lbl_valoracion)

        if resena.get("usuario_id") == self.usuario_id:
            btn_editar = QPushButton("✏ Editar")
            btn_editar.setFixedHeight(28)
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.clicked.connect(
                lambda _, r=resena: self._abrir_form_editar(r)
            )
            layout_derecha.addWidget(btn_editar)

            btn_eliminar = QPushButton("🗑 Eliminar")
            btn_eliminar.setFixedHeight(28)
            btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_eliminar.clicked.connect(
                lambda _, r=resena: self._eliminar_resena(r)
            )
            layout_derecha.addWidget(btn_eliminar)

        layout_tarjeta.addLayout(layout_derecha, stretch=1)

        return tarjeta

    # ─────────────────────────────────────────
    #  ACCIONES DE BOTONES
    # ─────────────────────────────────────────

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
                self._cargar_resenas()   # refresca las tarjetas
            else:
                QMessageBox.warning(self, "Error", resultado["mensaje"])