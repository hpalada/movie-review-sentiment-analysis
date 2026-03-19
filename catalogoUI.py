from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from catalogoLL import ServicioPeliculas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.servicio = ServicioPeliculas()
        

        layout = QVBoxLayout()

        # ====== Formulario Película ======
        layout.addWidget(QLabel("Película"))

        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Título")
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Descripción")

        # Imagen
        img_layout = QHBoxLayout()
        self.input_imagen = QLineEdit()
        self.input_imagen.setPlaceholderText("Ruta de imagen")
        self.btn_seleccionar_imagen = QPushButton("Seleccionar Imagen")
        self.btn_seleccionar_imagen.clicked.connect(self.seleccionar_imagen)
        img_layout.addWidget(self.input_imagen)
        img_layout.addWidget(self.btn_seleccionar_imagen)

        # Vista de la imagen
        self.label_imagen = QLabel()
        self.label_imagen.setFixedSize(200, 200)
        self.label_imagen.setStyleSheet("border: 1px solid black")
        self.label_imagen.setScaledContents(True)

        self.input_fecha = QLineEdit()
        self.input_fecha.setPlaceholderText("Fecha de publicacion")

        # Botones CRUD
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")  # Cambia a “Actualizar” al seleccionar
        self.btn_guardar.clicked.connect(self.guardar_o_actualizar)
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_pelicula)
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        self.btn_buscar = QPushButton("Buscar Película")
        self.btn_buscar.clicked.connect(self.buscar_pelicula)

        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_limpiar)
        btn_layout.addWidget(self.btn_buscar)

        # Añadir widgets al layout principal
        layout.addWidget(self.input_titulo)
        layout.addWidget(self.input_desc)
        layout.addLayout(img_layout)
        layout.addWidget(self.label_imagen)
        layout.addWidget(self.input_fecha)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.id_pelicula_seleccionada = None

    # ==================== Funciones ====================

    def seleccionar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )
        if archivo:
            self.input_imagen.setText(archivo)
            self.mostrar_imagen(archivo)

    def mostrar_imagen(self, ruta):
        pixmap = QPixmap(ruta)
        if not pixmap.isNull():
            self.label_imagen.setPixmap(pixmap.scaled(
                self.label_imagen.width(),
                self.label_imagen.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.label_imagen.clear()

    def limpiar_campos(self):
        self.input_titulo.clear()
        self.input_desc.clear()
        self.input_imagen.clear()
        self.label_imagen.clear()
        self.input_fecha.clear()
        self.id_pelicula_seleccionada = None
        self.btn_guardar.setText("Guardar")

    def guardar_o_actualizar(self):
        titulo = self.input_titulo.text()
        desc = self.input_desc.text()
        img = self.input_imagen.text()
        fecha = self.input_fecha.text()

        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return

        if self.id_pelicula_seleccionada:  # Actualizar
            self.servicio.actualizar_pelicula(
                self.id_pelicula_seleccionada, titulo, desc, img, fecha
            )
            QMessageBox.information(self, "Éxito", "Película editada")
        else:  # Guardar nueva
            self.servicio.agregar_pelicula(titulo, desc, img, fecha)
            QMessageBox.information(self, "Éxito", "Película agregada")

        self.limpiar_campos()

    def eliminar_pelicula(self):
        if not self.id_pelicula_seleccionada:
            QMessageBox.warning(self, "Error", "Selecciona una película para eliminar")
            return
        confirm = QMessageBox.question(
            self, "Confirmar", "¿Eliminar película seleccionada?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.servicio.eliminar_pelicula(self.id_pelicula_seleccionada)
            QMessageBox.information(self, "Éxito", "Película eliminada")
            self.limpiar_campos()

    def buscar_pelicula(self):
        peliculas = self.servicio.obtener_peliculas()
        titulos = [f"{p['id']} - {p['titulo']}" for p in peliculas]

        if not titulos:
            QMessageBox.information(self, "Info", "No hay películas guardadas")
            return

        item, ok = QInputDialog.getItem(
            self, "Seleccionar Película", "Películas:", titulos, 0, False
        )

        if ok and item:
            id_sel = int(item.split(" - ")[0])
            self.id_pelicula_seleccionada = id_sel

            for peli in peliculas:
                if peli["id"] == id_sel:
                    self.input_titulo.setText(peli["titulo"])
                    self.input_desc.setText(peli["descripcion"])
                    self.input_imagen.setText(peli["imagen"])
                    self.input_fecha.setText(peli["fecha"])
                    self.mostrar_imagen(peli["imagen"])
                    self.btn_guardar.setText("Actualizar")
                    break