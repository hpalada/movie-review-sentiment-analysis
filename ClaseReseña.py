import re
from ComunicacionModelo import ComunicacionModelo
from Json import JsonManager


class Resena:
    """
    Capa de clase para el manejo de reseñas.
    Recibe datos del formulario, los valida, los analiza con IA
    y los persiste en el JSON.
    """

    # Límites de texto
    LONGITUD_MINIMA = 20
    LONGITUD_MAXIMA = 2000

    def __init__(self):
        self.modelo = ComunicacionModelo()
        self.json   = JsonManager()

    # ─────────────────────────────────────────
    #  MÉTODO PRINCIPAL — llamado por el formulario
    # ─────────────────────────────────────────

    def procesar_resena(self, usuario_id: int, titulo_pelicula: str,
                        texto: str, anio: int = None, director: str = None) -> dict:
        """
        Punto de entrada desde el formulario.
        Valida, analiza con IA y guarda la reseña.

        Retorna un dict con:
          - exito      : bool
          - mensaje    : str  (descripción del resultado o error)
          - valoracion : float | None
          - estrellas  : str  | None
          - etiquetas  : list | None
          - resena_id  : int  | None
        """

        # 1. Validar texto de la reseña
        validacion = self._validar_texto(texto)
        if not validacion["valido"]:
            return self._respuesta_error(validacion["mensaje"])

        # 2. Verificar que el usuario existe
        usuario = self.json.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return self._respuesta_error("El usuario no existe.")

        # 3. Registrar la película si no existe aún
        pelicula = self.json.agregar_pelicula(titulo_pelicula, anio, director)

        # 4. Enviar reseña al modelo de IA
        try:
            resultado_ia = self.modelo.analizar_resena(texto)
        except Exception as e:
            return self._respuesta_error(f"Error al analizar con IA: {str(e)}")

        valoracion = resultado_ia["valoracion"]
        etiquetas  = resultado_ia["etiquetas"]

        # 5. Guardar reseña en el JSON
        resena_guardada = self.json.agregar_resena(
            usuario_id  = usuario_id,
            pelicula_id = pelicula["id"],
            texto       = texto.strip(),
            valoracion_ia = valoracion,
            etiquetas_ia  = etiquetas
        )

        # 6. Devolver resultado al formulario
        return {
            "exito"     : True,
            "mensaje"   : "Reseña guardada correctamente.",
            "valoracion": valoracion,
            "estrellas" : self._a_estrellas(valoracion),
            "etiquetas" : etiquetas,
            "resena_id" : resena_guardada["id"]
        }

    # ─────────────────────────────────────────
    #  EDITAR RESEÑA — llamado por el formulario
    # ─────────────────────────────────────────

    def editar_resena(self, resena_id: int, usuario_id: int, nuevo_texto: str) -> dict:
        """
        Edita una reseña existente si pertenece al usuario.
        Vuelve a analizarla con IA para actualizar valoración y etiquetas.
        """

        # 1. Validar nuevo texto
        validacion = self._validar_texto(nuevo_texto)
        if not validacion["valido"]:
            return self._respuesta_error(validacion["mensaje"])

        # 2. Verificar que la reseña existe
        resena = self.json.obtener_resena_por_id(resena_id)
        if not resena:
            return self._respuesta_error("La reseña no existe.")

        # 3. Verificar que pertenece al usuario
        if resena["usuario_id"] != usuario_id:
            return self._respuesta_error("No tienes permiso para editar esta reseña.")

        # 4. Re-analizar con IA
        try:
            resultado_ia = self.modelo.analizar_resena(nuevo_texto)
        except Exception as e:
            return self._respuesta_error(f"Error al analizar con IA: {str(e)}")

        valoracion = resultado_ia["valoracion"]
        etiquetas  = resultado_ia["etiquetas"]

        # 5. Guardar cambios en el JSON
        self.json.editar_resena(
            resena_id          = resena_id,
            usuario_id         = usuario_id,
            nuevo_texto        = nuevo_texto.strip(),
            nueva_valoracion_ia = valoracion,
            nuevas_etiquetas_ia = etiquetas
        )

        return {
            "exito"     : True,
            "mensaje"   : "Reseña actualizada correctamente.",
            "valoracion": valoracion,
            "estrellas" : self._a_estrellas(valoracion),
            "etiquetas" : etiquetas,
            "resena_id" : resena_id
        }

    # ─────────────────────────────────────────
    #  ELIMINAR RESEÑA — llamado por el formulario
    # ─────────────────────────────────────────

    def eliminar_resena(self, resena_id: int, usuario_id: int) -> dict:
        """
        Elimina una reseña si pertenece al usuario.
        """
        eliminado = self.json.eliminar_resena(resena_id, usuario_id)

        if not eliminado:
            return self._respuesta_error(
                "No se pudo eliminar. La reseña no existe o no te pertenece."
            )

        return {
            "exito"  : True,
            "mensaje": "Reseña eliminada correctamente."
        }

    # ─────────────────────────────────────────
    #  CONSULTAS — llamado por el formulario
    # ─────────────────────────────────────────

    def obtener_resenas_usuario(self, usuario_id: int) -> list:
        """Retorna todas las reseñas de un usuario para mostrarlas en el formulario."""
        return self.json.obtener_resenas_por_usuario(usuario_id)

    def obtener_resenas_pelicula(self, pelicula_id: int) -> list:
        """Retorna todas las reseñas de una película para mostrarlas en el formulario."""
        return self.json.obtener_resenas_por_pelicula(pelicula_id)

    # ─────────────────────────────────────────
    #  VALIDACIÓN INTERNA
    # ─────────────────────────────────────────

    def _validar_texto(self, texto: str) -> dict:
        """
        Verifica que el texto sea seguro y cumpla los requisitos mínimos.
        Retorna dict con 'valido' (bool) y 'mensaje' (str).
        """
        if not texto or not texto.strip():
            return {"valido": False, "mensaje": "La reseña no puede estar vacía."}

        texto = texto.strip()

        # Longitud mínima y máxima
        if len(texto) < self.LONGITUD_MINIMA:
            return {"valido": False,
                    "mensaje": f"La reseña debe tener al menos {self.LONGITUD_MINIMA} caracteres."}

        if len(texto) > self.LONGITUD_MAXIMA:
            return {"valido": False,
                    "mensaje": f"La reseña no puede superar los {self.LONGITUD_MAXIMA} caracteres."}

        # Detectar inyección de código — HTML / scripts
        if re.search(r'<.*?>', texto):
            return {"valido": False, "mensaje": "La reseña contiene etiquetas HTML no permitidas."}

        # Detectar inyección SQL básica
        patrones_sql = [
            r"(--|;|/\*|\*/)",
            r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|UNION)\b"
        ]
        for patron in patrones_sql:
            if re.search(patron, texto, re.IGNORECASE):
                return {"valido": False, "mensaje": "La reseña contiene caracteres no permitidos."}

        # Detectar código Python / JS
        patrones_codigo = [
            r"(import\s+\w+|from\s+\w+\s+import)",   # imports Python
            r"(__import__|eval\s*\(|exec\s*\()",       # ejecución dinámica
            r"(document\.|window\.|alert\s*\()",       # JS
        ]
        for patron in patrones_codigo:
            if re.search(patron, texto, re.IGNORECASE):
                return {"valido": False, "mensaje": "La reseña contiene código no permitido."}

        return {"valido": True, "mensaje": "OK"}

    # ─────────────────────────────────────────
    #  UTILIDADES INTERNAS
    # ─────────────────────────────────────────

    def _a_estrellas(self, score: float) -> str:
        """Convierte un puntaje 0-5 en representación visual de estrellas."""
        llenas = int(round(score))
        vacias = 5 - llenas
        return "★" * llenas + "☆" * vacias

    def _respuesta_error(self, mensaje: str) -> dict:
        """Estructura de respuesta estándar para errores."""
        return {
            "exito"     : False,
            "mensaje"   : mensaje,
            "valoracion": None,
            "estrellas" : None,
            "etiquetas" : None,
            "resena_id" : None
        }
