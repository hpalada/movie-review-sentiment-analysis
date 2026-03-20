from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from clasePelicula import Pelicula


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._pelicula_seleccionada = None   # objeto Pelicula o None
        self._construir_ui()

    # ── UI ───────────────────────────────────────────────────

    def _construir_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Película"))
        self.input_titulo = QLineEdit(placeholderText="Título")
        self.input_desc   = QLineEdit(placeholderText="Descripción")
        self.input_fecha  = QLineEdit(placeholderText="Fecha de publicación")

        img_layout = QHBoxLayout()
        self.input_imagen = QLineEdit(placeholderText="Ruta de imagen")
        btn_img = QPushButton("Seleccionar imagen")
        btn_img.clicked.connect(self._seleccionar_imagen)
        img_layout.addWidget(self.input_imagen)
        img_layout.addWidget(btn_img)

        self.label_imagen = QLabel()
        self.label_imagen.setFixedSize(200, 200)
        self.label_imagen.setStyleSheet("border: 1px solid black")
        self.label_imagen.setScaledContents(True)

        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self._guardar_o_actualizar)
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self._eliminar)
        btn_limpiar  = QPushButton("Limpiar")
        btn_limpiar.clicked.connect(self._limpiar)
        btn_buscar   = QPushButton("Buscar película")
        btn_buscar.clicked.connect(self._buscar)
        for b in (self.btn_guardar, btn_eliminar, btn_limpiar, btn_buscar):
            btn_layout.addWidget(b)

        for w in (self.input_titulo, self.input_desc):
            layout.addWidget(w)
        layout.addLayout(img_layout)
        layout.addWidget(self.label_imagen)
        layout.addWidget(self.input_fecha)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    # ── Slots ────────────────────────────────────────────────

    def _seleccionar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )
        if ruta:
            self.input_imagen.setText(ruta)
            self._mostrar_imagen(ruta)

    def _mostrar_imagen(self, ruta):
        px = QPixmap(ruta)
        if not px.isNull():
            self.label_imagen.setPixmap(px.scaled(
                self.label_imagen.width(), self.label_imagen.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.label_imagen.clear()

    def _guardar_o_actualizar(self):
        titulo = self.input_titulo.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return

        if self._pelicula_seleccionada:          # ── actualizar ──
            ok = self._pelicula_seleccionada.actualizar(
                titulo      = titulo,
                descripcion = self.input_desc.text(),
                imagen      = self.input_imagen.text(),
                fecha       = self.input_fecha.text(),
            )
            msg = "Película actualizada" if ok else "No se pudo actualizar"
        else:                                     # ── crear nueva ──
            Pelicula.guardar(
                titulo      = titulo,
                descripcion = self.input_desc.text(),
                imagen      = self.input_imagen.text(),
                fecha       = self.input_fecha.text(),
            )
            msg = "Película guardada"

        QMessageBox.information(self, "Éxito", msg)
        self._limpiar()

    def _eliminar(self):
        if not self._pelicula_seleccionada:
            QMessageBox.warning(self, "Error", "Selecciona una película primero")
            return
        if QMessageBox.question(
            self, "Confirmar", "¿Eliminar esta película?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self._pelicula_seleccionada.eliminar()
            QMessageBox.information(self, "Éxito", "Película eliminada")
            self._limpiar()

    def _buscar(self):
        peliculas = Pelicula.todas()
        if not peliculas:
            QMessageBox.information(self, "Info", "No hay películas guardadas")
            return

        opciones = [f"{p.id} - {p.titulo}" for p in peliculas]
        item, ok = QInputDialog.getItem(
            self, "Seleccionar película", "Películas:", opciones, 0, False
        )
        if ok and item:
            id_sel = int(item.split(" - ")[0])
            peli   = Pelicula.buscar_por_id(id_sel)
            if peli:
                self._cargar_en_form(peli)

    def _cargar_en_form(self, peli: Pelicula):
        self._pelicula_seleccionada = peli
        self.input_titulo.setText(peli.titulo or "")
        self.input_desc.setText(peli.descripcion or "")
        self.input_imagen.setText(peli.imagen or "")
        self.input_fecha.setText(peli.fecha or "")
        if peli.imagen:
            self._mostrar_imagen(peli.imagen)
        self.btn_guardar.setText("Actualizar")

    def _limpiar(self):
        for w in (self.input_titulo, self.input_desc,
                  self.input_imagen, self.input_fecha):
            w.clear()
        self.label_imagen.clear()
        self._pelicula_seleccionada = None
        self.btn_guardar.setText("Guardar")