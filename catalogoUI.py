from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from catalogoLL import ServicioPeliculas

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.servicio = ServicioPeliculas()
        self.setWindowTitle("Catálogo de Películas - Con Imagen")
        self.resize(700, 700)

        layout = QVBoxLayout()

        # ====== Formulario Película ======
        layout.addWidget(QLabel("Agregar / Editar Película"))

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
        self.input_fecha.setPlaceholderText("Fecha")

        # Botones CRUD
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar / Actualizar")
        self.btn_guardar.clicked.connect(self.guardar_pelicula)
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_pelicula)
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_campos)
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_limpiar)

        layout.addWidget(self.input_titulo)
        layout.addWidget(self.input_desc)
        layout.addLayout(img_layout)
        layout.addWidget(self.label_imagen)
        layout.addWidget(self.input_fecha)
        layout.addLayout(btn_layout)

        # ====== Buscar ======
        search_layout = QHBoxLayout()
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Buscar por título")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar_pelicula)
        search_layout.addWidget(self.input_buscar)
        search_layout.addWidget(self.btn_buscar)
        layout.addLayout(search_layout)

        # ====== Lista Películas ======
        layout.addWidget(QLabel("Películas"))
        self.lista = QListWidget()
        self.lista.itemClicked.connect(self.seleccionar_pelicula)
        layout.addWidget(self.lista)

        # ====== Formulario Reseña ======
        layout.addWidget(QLabel("Agregar Reseña"))
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Usuario")
        self.input_comentario = QTextEdit()
        self.input_comentario.setPlaceholderText("Comentario")
        self.btn_agregar_resena = QPushButton("Agregar Reseña")
        self.btn_agregar_resena.clicked.connect(self.agregar_resena)

        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_comentario)
        layout.addWidget(self.btn_agregar_resena)

        self.setLayout(layout)

        self.id_pelicula_seleccionada = None
        self.cargar_peliculas()

    # ==================== Funciones ====================

    def cargar_peliculas(self, peliculas=None):
        self.lista.clear()
        if peliculas is None:
            peliculas = self.servicio.obtener_peliculas()
        for peli in peliculas:
            item = QListWidgetItem(f"{peli['id']} - {peli['titulo']}")
            item.setData(1, peli["id"])
            self.lista.addItem(item)

    def seleccionar_pelicula(self, item):
        self.id_pelicula_seleccionada = item.data(1)
        peliculas = self.servicio.obtener_peliculas()
        for peli in peliculas:
            if peli["id"] == self.id_pelicula_seleccionada:
                self.input_titulo.setText(peli["titulo"])
                self.input_desc.setText(peli["descripcion"])
                self.input_imagen.setText(peli["imagen"])
                self.input_fecha.setText(peli["fecha"])
                self.mostrar_imagen(peli["imagen"])
                break

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
            self.label_imagen.setPixmap(pixmap)
        else:
            self.label_imagen.clear()

    def limpiar_campos(self):
        self.input_titulo.clear()
        self.input_desc.clear()
        self.input_imagen.clear()
        self.label_imagen.clear()
        self.input_fecha.clear()
        self.input_buscar.clear()
        self.id_pelicula_seleccionada = None
        self.cargar_peliculas()

    def guardar_pelicula(self):
        titulo = self.input_titulo.text()
        desc = self.input_desc.text()
        img = self.input_imagen.text()
        fecha = self.input_fecha.text()

        if not titulo:
            QMessageBox.warning(self, "Error", "El título es obligatorio")
            return

        if self.id_pelicula_seleccionada:
            self.servicio.actualizar_pelicula(
                self.id_pelicula_seleccionada, titulo, desc, img, fecha
            )
            QMessageBox.information(self, "Éxito", "Película actualizada")
        else:
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
        termino = self.input_buscar.text().lower()
        if not termino:
            self.cargar_peliculas()
            return
        peliculas = self.servicio.obtener_peliculas()
        filtradas = [p for p in peliculas if termino in p["titulo"].lower()]
        self.cargar_peliculas(filtradas)

    def agregar_resena(self):
        if not self.id_pelicula_seleccionada:
            QMessageBox.warning(self, "Error", "Selecciona una película primero")
            return
        usuario = self.input_usuario.text()
        comentario = self.input_comentario.toPlainText()
        if not usuario or not comentario:
            QMessageBox.warning(self, "Error", "Completa todos los campos")
            return
        self.servicio.agregar_resena(
            self.id_pelicula_seleccionada, usuario, comentario
        )
        QMessageBox.information(self, "Éxito", "Reseña agregada")
        self.input_usuario.clear()
        self.input_comentario.clear()