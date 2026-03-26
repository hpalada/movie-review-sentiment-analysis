# FormAgregaryEditar.py
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
                nuevo_texto = self.datos["texto"],
                idioma      = self.datos["idioma"]        # ← nuevo
            )
        else:
            resultado = self.clase_resena.procesar_resena(
                usuario_id      = self.datos["usuario_id"],
                titulo_pelicula = self.datos["titulo_pelicula"],
                texto           = self.datos["texto"],
                idioma          = self.datos["idioma"]    # ← nuevo
            )
        self.resultado_listo.emit(resultado)


# ─────────────────────────────────────────
#  SWITCH DE IDIOMA
# ─────────────────────────────────────────

class LanguageSwitch(QWidget):
    """Toggle compacto ES ↔ EN."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._idioma = "es"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.lbl_es = QLabel("ES")
        self.btn    = QPushButton()
        self.btn.setFixedSize(48, 24)
        self.btn.setCheckable(True)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setToolTip("Cambiar idioma de análisis")
        self.btn.clicked.connect(self._toggle)
        self.lbl_en = QLabel("EN")

        layout.addWidget(self.lbl_es)
        layout.addWidget(self.btn)
        layout.addWidget(self.lbl_en)

        self._actualizar_estilo()

    def _toggle(self):
        self._idioma = "en" if self._idioma == "es" else "es"
        self._actualizar_estilo()

    def _actualizar_estilo(self):
        es_activo = self._idioma == "es"
        self.lbl_es.setStyleSheet("font-weight: bold;" if es_activo  else "color: gray;")
        self.lbl_en.setStyleSheet("font-weight: bold;" if not es_activo else "color: gray;")
        self.btn.setChecked(not es_activo)
        color = "#4CAF50" if es_activo else "#2196F3"
        self.btn.setStyleSheet(
            f"QPushButton {{ border-radius: 12px; background-color: {color}; }}"
        )

    @property
    def idioma(self) -> str:
        return self._idioma


# ─────────────────────────────────────────
#  FORMULARIO AGREGAR / EDITAR
# ─────────────────────────────────────────

class FormAgregaryEditar(QWidget):
    def __init__(self, pelicula_id: int, usuario_id: int,
                 clase_resena, titulo_pelicula: str,
                 resena: dict = None, callback=None):
        super().__init__()

        self.pelicula_id     = pelicula_id
        self.usuario_id      = usuario_id
        self.clase_resena    = clase_resena
        self.titulo_pelicula = titulo_pelicula
        self.resena          = resena
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
        self.setFixedSize(750, 460)   # un poco más alto para el switch

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

        layout_principal.addLayout(self._panel_formulario(), stretch=3)
        layout_principal.addLayout(self._panel_resultados(), stretch=2)

    def _panel_formulario(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout_frame = QVBoxLayout(frame)
        layout_frame.setContentsMargins(12, 12, 12, 12)
        layout_frame.setSpacing(10)

        # Campo película (solo lectura)
        self.campo_pelicula = QLineEdit(self.titulo_pelicula)
        self.campo_pelicula.setReadOnly(True)
        self.campo_pelicula.setPlaceholderText("Nombre película")
        layout_frame.addWidget(self.campo_pelicula)

        # Área de texto
        self.campo_resena = QTextEdit()
        self.campo_resena.setPlaceholderText("Escribe tu reseña...")
        layout_frame.addWidget(self.campo_resena)

        # ── Switch de idioma debajo del texto ──
        layout_switch = QHBoxLayout()
        lbl_idioma = QLabel("Idioma de la reseña:")
        self.switch_idioma = LanguageSwitch()
        layout_switch.addWidget(lbl_idioma)
        layout_switch.addWidget(self.switch_idioma)
        layout_switch.addStretch()
        layout_frame.addLayout(layout_switch)

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

        lbl_titulo = QLabel("RESULTADOS IA")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setFrameShape(QFrame.Shape.Box)
        lbl_titulo.setFixedHeight(36)
        layout.addWidget(lbl_titulo)

        self.lbl_valoracion = QLabel("—")
        self.lbl_valoracion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valoracion.setFrameShape(QFrame.Shape.Box)
        self.lbl_valoracion.setFixedHeight(36)
        layout.addWidget(self.lbl_valoracion)

        self.layout_etiquetas = QVBoxLayout()
        self.layout_etiquetas.setSpacing(6)
        layout.addLayout(self.layout_etiquetas)

        layout.addStretch()

        self.btn_cerrar = QPushButton("CERRAR")
        self.btn_cerrar.setFixedHeight(42)
        self.btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar.setEnabled(False)
        self.btn_cerrar.clicked.connect(self._cerrar)
        layout.addWidget(self.btn_cerrar)

        return layout

    # ─────────────────────────────────────────
    #  PRECARGA EN MODO EDICIÓN
    # ─────────────────────────────────────────

    def _precargar_texto(self):
        self.campo_resena.setPlainText(self.resena.get("texto", ""))

    # ─────────────────────────────────────────
    #  GUARDAR
    # ─────────────────────────────────────────

    def _guardar(self):
        texto = self.campo_resena.toPlainText().strip()

        if not texto:
            self.lbl_valoracion.setText("⚠ Escribe una reseña.")
            return

        self.btn_guardar.setEnabled(False)
        self.campo_resena.setReadOnly(True)
        self.switch_idioma.btn.setEnabled(False)   # bloquear switch mientras procesa
        self.lbl_valoracion.setText("Analizando...")
        self._limpiar_etiquetas()

        datos = {
            "es_edicion"     : self.es_edicion,
            "usuario_id"     : self.usuario_id,
            "titulo_pelicula": self.titulo_pelicula,
            "texto"          : texto,
            "resena_id"      : self.resena["id"] if self.es_edicion else None,
            "idioma"         : self.switch_idioma.idioma   # ← "es" | "en"
        }

        self.hilo = HiloAnalisis(self.clase_resena, datos)
        self.hilo.resultado_listo.connect(self._mostrar_resultados)
        self.hilo.start()

    # ─────────────────────────────────────────
    #  MOSTRAR RESULTADOS
    # ─────────────────────────────────────────

    def _mostrar_resultados(self, resultado: dict):
        self.switch_idioma.btn.setEnabled(True)   # re-habilitar switch

        if not resultado.get("exito"):
            self.lbl_valoracion.setText(f"⚠ {resultado.get('mensaje', 'Error')}")
            self.btn_guardar.setEnabled(True)
            self.campo_resena.setReadOnly(False)
            return

        valoracion = resultado.get("valoracion", "?")
        estrellas  = resultado.get("estrellas", "")
        self.lbl_valoracion.setText(f"{valoracion} / 5  {estrellas}")

        self._limpiar_etiquetas()
        for etiqueta in resultado.get("etiquetas", []):
            lbl = QLabel(etiqueta)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFrameShape(QFrame.Shape.Box)
            lbl.setFixedHeight(30)
            self.layout_etiquetas.addWidget(lbl)

        self.btn_cerrar.setEnabled(True)
        self.btn_guardar.setEnabled(False)

    # ─────────────────────────────────────────
    #  CERRAR
    # ─────────────────────────────────────────

    def _cerrar(self):
        if self.callback:
            self.callback()
        self.close()

    # ─────────────────────────────────────────
    #  UTILIDADES
    # ─────────────────────────────────────────

    def _limpiar_etiquetas(self):
        while self.layout_etiquetas.count():
            item = self.layout_etiquetas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()