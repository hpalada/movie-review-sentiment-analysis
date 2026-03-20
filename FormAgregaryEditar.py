from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


# ─────────────────────────────────────────
#  HILO PARA NO BLOQUEAR LA UI MIENTRAS LA IA ANALIZA
# ─────────────────────────────────────────

class HiloAnalisis(QThread):
    resultado_listo = pyqtSignal(dict)

    def __init__(self, clase_resena, datos):
        super().__init__()
        self.clase_resena = clase_resena
        self.datos        = datos

    def run(self):
        if self.datos.get("es_edicion"):
            resultado = self.clase_resena.editar_resena(
                resena_id   = self.datos["resena_id"],
                usuario_id  = self.datos["usuario_id"],
                nuevo_texto = self.datos["texto"]
            )
        else:
            resultado = self.clase_resena.procesar_resena(
                usuario_id      = self.datos["usuario_id"],
                titulo_pelicula = self.datos["titulo_pelicula"],
                texto           = self.datos["texto"]
            )
        self.resultado_listo.emit(resultado)


# ─────────────────────────────────────────
#  FORMULARIO AGREGAR / EDITAR
# ─────────────────────────────────────────

class FormAgregaryEditar(QWidget):
    """
    Ventana modal superpuesta para agregar o editar una reseña.
    - resena=None  → modo agregar
    - resena=dict  → modo editar (precarga el texto)
    - callback     → función que llama al cerrar para refrescar FormResenas
    """

    def __init__(self, pelicula_id: int, usuario_id: int,
                 clase_resena, titulo_pelicula: str,
                 resena: dict = None, callback=None):
        super().__init__()

        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_resena    = clase_resena
        self.titulo_pelicula = titulo_pelicula
        self.resena          = resena          # None = agregar, dict = editar
        self.callback        = callback
        self.es_edicion      = resena is not None

        self._configurar_ventana()
        self._construir_ui()

        if self.es_edicion:
            self._precargar_texto()

    # ─────────────────────────────────────────
    #  CONFIGURACIÓN DE VENTANA
    # ─────────────────────────────────────────

    def _configurar_ventana(self):
        titulo = "Editar reseña" if self.es_edicion else "Agregar reseña"
        self.setWindowTitle(titulo)
        self.setFixedSize(750, 420)

        # Superpuesta sobre la ventana padre
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )

    # ─────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA UI
    # ─────────────────────────────────────────

    def _construir_ui(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(16)

        # ── Panel izquierdo: formulario ──
        layout_principal.addLayout(self._panel_formulario(), stretch=3)

        # ── Panel derecho: resultados IA ──
        layout_principal.addLayout(self._panel_resultados(), stretch=2)

    def _panel_formulario(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Contenedor con borde
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout_frame = QVBoxLayout(frame)
        layout_frame.setContentsMargins(12, 12, 12, 12)
        layout_frame.setSpacing(10)

        # Campo nombre película (solo lectura)
        self.campo_pelicula = QLineEdit(self.titulo_pelicula)
        self.campo_pelicula.setReadOnly(True)
        self.campo_pelicula.setPlaceholderText("Nombre película")
        layout_frame.addWidget(self.campo_pelicula)

        # Área de texto de la reseña
        self.campo_resena = QTextEdit()
        self.campo_resena.setPlaceholderText("Escribe tu reseña...")
        layout_frame.addWidget(self.campo_resena)

        # Botón guardar
        self.btn_guardar = QPushButton("GUARDAR")
        self.btn_guardar.setFixedHeight(42)
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guardar.clicked.connect(self._guardar)
        layout_frame.addWidget(self.btn_guardar)

        layout.addWidget(frame)
        return layout

    def _panel_resultados(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Título sección
        lbl_titulo = QLabel("RESULTADOS IA")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setFrameShape(QFrame.Shape.Box)
        lbl_titulo.setFixedHeight(36)
        layout.addWidget(lbl_titulo)

        # Valoración
        self.lbl_valoracion = QLabel("—")
        self.lbl_valoracion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valoracion.setFrameShape(QFrame.Shape.Box)
        self.lbl_valoracion.setFixedHeight(36)
        layout.addWidget(self.lbl_valoracion)

        # Contenedor dinámico de etiquetas
        self.layout_etiquetas = QVBoxLayout()
        self.layout_etiquetas.setSpacing(6)
        layout.addLayout(self.layout_etiquetas)

        layout.addStretch()

        # Botón cerrar
        self.btn_cerrar = QPushButton("CERRAR")
        self.btn_cerrar.setFixedHeight(42)
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.setEnabled(False)   # deshabilitado hasta que lleguen resultados
        self.btn_cerrar.clicked.connect(self._cerrar)
        layout.addWidget(self.btn_cerrar)

        return layout

    # ─────────────────────────────────────────
    #  PRECARGA EN MODO EDICIÓN
    # ─────────────────────────────────────────

    def _precargar_texto(self):
        self.campo_resena.setPlainText(self.resena.get("texto", ""))

    # ─────────────────────────────────────────
    #  GUARDAR — lanza el hilo de análisis
    # ─────────────────────────────────────────

    def _guardar(self):
        texto = self.campo_resena.toPlainText().strip()

        if not texto:
            self.lbl_valoracion.setText("⚠ Escribe una reseña.")
            return

        # Bloquear campos mientras se procesa
        self.btn_guardar.setEnabled(False)
        self.campo_resena.setReadOnly(True)
        self.lbl_valoracion.setText("Analizando...")
        self._limpiar_etiquetas()

        datos = {
            "es_edicion"     : self.es_edicion,
            "usuario_id"     : self.usuario_id,
            "titulo_pelicula": self.titulo_pelicula,
            "texto"          : texto,
            "resena_id"      : self.resena["id"] if self.es_edicion else None
        }

        self.hilo = HiloAnalisis(self.clase_resena, datos)
        self.hilo.resultado_listo.connect(self._mostrar_resultados)
        self.hilo.start()

    # ─────────────────────────────────────────
    #  MOSTRAR RESULTADOS cuando el hilo termina
    # ─────────────────────────────────────────

    def _mostrar_resultados(self, resultado: dict):
        if not resultado.get("exito"):
            self.lbl_valoracion.setText(f"⚠ {resultado.get('mensaje', 'Error')}")
            self.btn_guardar.setEnabled(True)
            self.campo_resena.setReadOnly(False)
            return

        # Mostrar valoración y estrellas
        valoracion = resultado.get("valoracion", "?")
        estrellas  = resultado.get("estrellas", "")
        self.lbl_valoracion.setText(f"{valoracion} / 5  {estrellas}")

        # Mostrar etiquetas dinámicamente
        self._limpiar_etiquetas()
        for etiqueta in resultado.get("etiquetas", []):
            lbl = QLabel(etiqueta)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFrameShape(QFrame.Shape.Box)
            lbl.setFixedHeight(30)
            self.layout_etiquetas.addWidget(lbl)

        # Habilitar cerrar, deshabilitar guardar de nuevo
        self.btn_cerrar.setEnabled(True)
        self.btn_guardar.setEnabled(False)

    # ─────────────────────────────────────────
    #  CERRAR
    # ─────────────────────────────────────────

    def _cerrar(self):
        if self.callback:
            self.callback()     # refresca las tarjetas en FormResenas
        self.close()

    # ─────────────────────────────────────────
    #  UTILIDADES
    # ─────────────────────────────────────────

    def _limpiar_etiquetas(self):
        while self.layout_etiquetas.count():
            item = self.layout_etiquetas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()