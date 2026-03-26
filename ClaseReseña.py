# ClaseReseña.py
import re
from Json import JsonManager


class Resena:

    LONGITUD_MINIMA = 20
    LONGITUD_MAXIMA = 2000

    def __init__(self):
        self.json    = JsonManager()
        self._modelo = None

    def _obtener_modelo(self):
        if self._modelo is not None:
            return self._modelo
        try:
            from ComunicacionModelo import ComunicacionModelo
            self._modelo = ComunicacionModelo()
        except Exception as e:
            print(f"[Aviso] ComunicacionModelo no disponible: {e}")
            self._modelo = None
        return self._modelo

    # ─────────────────────────────────────────
    #  TRADUCCIÓN ES → EN
    # ─────────────────────────────────────────

    def _traducir_al_ingles(self, texto: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": (
                        "Translate the following movie review from Spanish to English. "
                        "Return ONLY the translated text, no explanations or extra content.\n\n"
                        f"{texto}"
                    )
                }]
            )
            traduccion = response.content[0].text.strip()

            # ── DEBUG ──────────────────────────────────────
            print("=" * 60)
            print(f"[TRADUCCIÓN] Original:\n{texto}")
            print("-" * 60)
            print(f"[TRADUCCIÓN] Resultado:\n{traduccion}")
            print("=" * 60)
            # ───────────────────────────────────────────────

            return traduccion
        except Exception as e:
            print(f"[Aviso] Error al traducir: {e}")
            return texto

    # ─────────────────────────────────────────
    #  MÉTODO PRINCIPAL
    # ─────────────────────────────────────────

    def procesar_resena(self, usuario_id: int, titulo_pelicula: str,
                        texto: str, anio: int = None, director: str = None,
                        idioma: str = "es") -> dict:

        validacion = self._validar_texto(texto)
        if not validacion["valido"]:
            return self._respuesta_error(validacion["mensaje"])

        usuario = self.json.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return self._respuesta_error("El usuario no existe.")

        pelicula = self.json.agregar_pelicula(titulo_pelicula, anio=anio, director=director)

        # Traducir si el idioma es español
        texto_para_ia = self._traducir_al_ingles(texto) if idioma == "es" else texto

        modelo = self._obtener_modelo()
        if modelo:
            try:
                resultado_ia = modelo.analizar_resena(texto_para_ia)
                valoracion   = resultado_ia["valoracion"]
                etiquetas    = resultado_ia["etiquetas"]
            except Exception as e:
                print(f"[Aviso] Error en análisis IA: {e}")
                valoracion = 0.0
                etiquetas  = ["neutral"]
        else:
            valoracion = 0.0
            etiquetas  = ["neutral"]

        resena_guardada = self.json.agregar_resena(
            usuario_id    = usuario_id,
            pelicula_id   = pelicula["id"],
            texto         = texto.strip(),        # se guarda el texto original
            valoracion_ia = valoracion,
            etiquetas_ia  = etiquetas
        )

        return {
            "exito"     : True,
            "mensaje"   : "Reseña guardada correctamente.",
            "valoracion": valoracion,
            "estrellas" : self._a_estrellas(valoracion),
            "etiquetas" : etiquetas,
            "resena_id" : resena_guardada["id"]
        }

    # ─────────────────────────────────────────
    #  EDITAR RESEÑA
    # ─────────────────────────────────────────

    def editar_resena(self, resena_id: int, usuario_id: int,
                      nuevo_texto: str, idioma: str = "es") -> dict:

        validacion = self._validar_texto(nuevo_texto)
        if not validacion["valido"]:
            return self._respuesta_error(validacion["mensaje"])

        resena = self.json.obtener_resena_por_id(resena_id)
        if not resena:
            return self._respuesta_error("La reseña no existe.")

        if resena["usuario_id"] != usuario_id:
            return self._respuesta_error("No tienes permiso para editar esta reseña.")

        # Traducir si el idioma es español
        texto_para_ia = self._traducir_al_ingles(nuevo_texto) if idioma == "es" else nuevo_texto

        modelo = self._obtener_modelo()
        if modelo:
            try:
                resultado_ia = modelo.analizar_resena(texto_para_ia)
                valoracion   = resultado_ia["valoracion"]
                etiquetas    = resultado_ia["etiquetas"]
            except Exception as e:
                print(f"[Aviso] Error en análisis IA: {e}")
                valoracion = 0.0
                etiquetas  = ["neutral"]
        else:
            valoracion = 0.0
            etiquetas  = ["neutral"]

        self.json.editar_resena(
            resena_id           = resena_id,
            usuario_id          = usuario_id,
            nuevo_texto         = nuevo_texto.strip(),   # original
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
    #  ELIMINAR RESEÑA
    # ─────────────────────────────────────────

    def eliminar_resena(self, resena_id: int, usuario_id: int) -> dict:
        eliminado = self.json.eliminar_resena(resena_id, usuario_id)
        if not eliminado:
            return self._respuesta_error(
                "No se pudo eliminar. La reseña no existe o no te pertenece."
            )
        return {"exito": True, "mensaje": "Reseña eliminada correctamente."}

    # ─────────────────────────────────────────
    #  CONSULTAS
    # ─────────────────────────────────────────

    def obtener_resenas_usuario(self, usuario_id: int) -> list:
        return self.json.obtener_resenas_por_usuario(usuario_id)

    def obtener_resenas_pelicula(self, pelicula_id: int) -> list:
        return self.json.obtener_resenas_por_pelicula(pelicula_id)

    # ─────────────────────────────────────────
    #  VALIDACIÓN
    # ─────────────────────────────────────────

    def _validar_texto(self, texto: str) -> dict:
        if not texto or not texto.strip():
            return {"valido": False, "mensaje": "La reseña no puede estar vacía."}

        texto = texto.strip()

        if len(texto) < self.LONGITUD_MINIMA:
            return {"valido": False,
                    "mensaje": f"La reseña debe tener al menos {self.LONGITUD_MINIMA} caracteres."}

        if len(texto) > self.LONGITUD_MAXIMA:
            return {"valido": False,
                    "mensaje": f"La reseña no puede superar los {self.LONGITUD_MAXIMA} caracteres."}

        if re.search(r'<.*?>', texto):
            return {"valido": False, "mensaje": "La reseña contiene etiquetas HTML no permitidas."}

        patrones_sql = [
            r"(--|;|/\*|\*/)",
            r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|UNION)\b"
        ]
        for patron in patrones_sql:
            if re.search(patron, texto, re.IGNORECASE):
                return {"valido": False, "mensaje": "La reseña contiene caracteres no permitidos."}

        patrones_codigo = [
            r"(import\s+\w+|from\s+\w+\s+import)",
            r"(__import__|eval\s*\(|exec\s*\()",
            r"(document\.|window\.|alert\s*\()",
        ]
        for patron in patrones_codigo:
            if re.search(patron, texto, re.IGNORECASE):
                return {"valido": False, "mensaje": "La reseña contiene código no permitido."}

        return {"valido": True, "mensaje": "OK"}

    # ─────────────────────────────────────────
    #  UTILIDADES
    # ─────────────────────────────────────────

    def _a_estrellas(self, score: float) -> str:
        llenas = int(round(score))
        vacias = 5 - llenas
        return "★" * llenas + "☆" * vacias

    def _respuesta_error(self, mensaje: str) -> dict:
        return {
            "exito"     : False,
            "mensaje"   : mensaje,
            "valoracion": None,
            "estrellas" : None,
            "etiquetas" : None,
            "resena_id" : None
        }