# PeliculaUI.py
import os
import shutil

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from clasePelicula import Pelicula

# ── Rutas base ────────────────────────────────────────────────────────
# BASE_DIR apunta siempre a la carpeta del proyecto sin importar
# en qué computadora se ejecute el sistema.
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CARPETA_IMGS = os.path.join(BASE_DIR, "Imagenes")

def _ruta_completa(nombre_archivo: str) -> str:
    """Dado el nombre guardado en el JSON, devuelve la ruta absoluta real."""
    if not nombre_archivo:
        return ""
    # Si ya es una ruta absoluta (datos viejos), la devuelve tal cual
    if os.path.isabs(nombre_archivo):
        return nombre_archivo
    return os.path.join(CARPETA_IMGS, nombre_archivo)


class PeliculaUI(QDialog):
    """
    Diálogo para agregar o editar una película.
    - pelicula=None  → modo agregar
    - pelicula=obj   → modo editar (precarga los campos)
    - callback       → función que se llama al guardar para refrescar el catálogo
    """

    def __init__(self, pelicula=None, callback=None, parent=None):
        super().__init__(parent)
        self.pelicula   = pelicula
        self.callback   = callback
        self.es_edicion = pelicula is not None
        # Ruta absoluta temporal de la imagen seleccionada en esta sesión
        self._ruta_imagen_original = None

        self.setWindowTitle("Editar película" if self.es_edicion else "Agregar película")
        self.setFixedSize(420, 640)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        os.makedirs(CARPETA_IMGS, exist_ok=True)

        self._construir_ui()

        if self.es_edicion:
            self._precargar()

    def _construir_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Título:"))
        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Título")
        layout.addWidget(self.input_titulo)

        layout.addWidget(QLabel("Descripción:"))
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Descripción")
        layout.addWidget(self.input_desc)

        layout.addWidget(QLabel("Fecha de publicación:"))
        self.input_fecha = QLineEdit()
        self.input_fecha.setPlaceholderText("Fecha de publicación")
        layout.addWidget(self.input_fecha)

        layout.addWidget(QLabel("Año:"))
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Año (ej. 2021)")
        layout.addWidget(self.input_anio)

        layout.addWidget(QLabel("Director:"))
        self.input_director = QLineEdit()
        self.input_director.setPlaceholderText("Director")
        layout.addWidget(self.input_director)

        layout.addWidget(QLabel("Imagen:"))
        img_layout = QHBoxLayout()
        self.input_imagen = QLineEdit()
        self.input_imagen.setPlaceholderText("Selecciona una imagen...")
        self.input_imagen.setReadOnly(True)
        btn_img = QPushButton("Seleccionar")
        btn_img.clicked.connect(self._seleccionar_imagen)
        img_layout.addWidget(self.input_imagen)
        img_layout.addWidget(btn_img)
        layout.addLayout(img_layout)

        self.label_imagen = QLabel("Sin imagen")
        self.label_imagen.setFixedSize(260, 160)
        self.label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_imagen, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar" if not self.es_edicion else "Actualizar")
        self.btn_guardar.clicked.connect(self._guardar)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)

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
            self.input_imagen.setText(os.path.basename(ruta))
            self._mostrar_imagen(ruta)

    def _mostrar_imagen(self, ruta_absoluta: str):
        if ruta_absoluta and os.path.exists(ruta_absoluta):
            px = QPixmap(ruta_absoluta)
            if not px.isNull():
                self.label_imagen.setPixmap(
                    px.scaled(260, 160,
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
                )
                return
        self.label_imagen.clear()
        self.label_imagen.setText("Sin imagen")

    def _copiar_imagen(self, ruta_origen: str) -> str:
        """
        Copia la imagen a la carpeta Imagenes/ del proyecto.
        Devuelve el nombre del archivo (lo que se guarda en el JSON).
        Si el archivo ya está en Imagenes/, no lo copia de nuevo.
        """
        nombre = os.path.basename(ruta_origen)
        destino = os.path.join(CARPETA_IMGS, nombre)

        if os.path.abspath(ruta_origen) != os.path.abspath(destino):
            # Si ya existe un archivo con el mismo nombre, agrega un sufijo
            base, ext = os.path.splitext(nombre)
            contador = 1
            while os.path.exists(destino):
                nombre  = f"{base}_{contador}{ext}"
                destino = os.path.join(CARPETA_IMGS, nombre)
                contador += 1
            shutil.copy2(ruta_origen, destino)

        return nombre

    def _guardar(self):
        titulo = self.input_titulo.text().strip()
        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio.")
            return

        descripcion = self.input_desc.text().strip() or None
        fecha       = self.input_fecha.text().strip() or None
        director    = self.input_director.text().strip() or None
        anio_txt    = self.input_anio.text().strip()
        anio        = int(anio_txt) if anio_txt.isdigit() else None

        # ── Manejar imagen ────────────────────────────────────────────
        if self._ruta_imagen_original:
            # El usuario seleccionó una imagen nueva → copiarla
            imagen = self._copiar_imagen(self._ruta_imagen_original)
        elif self.es_edicion:
            # Sin cambio de imagen → conservar la que ya tenía
            imagen = self.pelicula.imagen
        else:
            imagen = None

        if self.es_edicion:
            ok = self.pelicula.actualizar(
                titulo=titulo, descripcion=descripcion, imagen=imagen,
                fecha=fecha, anio=anio, director=director
            )
            msg = "Película actualizada." if ok else "No se pudo actualizar."
        else:
            Pelicula.guardar(
                titulo=titulo, descripcion=descripcion, imagen=imagen,
                fecha=fecha, anio=anio, director=director
            )
            msg = "Película guardada."

        QMessageBox.information(self, "Éxito", msg)

        if self.callback:
            self.callback()

        self.close()