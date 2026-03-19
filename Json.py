import json
import os
from datetime import datetime


class JsonManager:
    def __init__(self):
        self.carpeta          = "data"
        self.archivo_peliculas = f"{self.carpeta}/peliculas.json"
        self.archivo_usuarios  = f"{self.carpeta}/usuarios.json"
        self.archivo_resenas   = f"{self.carpeta}/resenas.json"

        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

        self._inicializar_archivo(self.archivo_peliculas, {"peliculas": []})
        self._inicializar_archivo(self.archivo_usuarios,  {"usuarios": []})
        self._inicializar_archivo(self.archivo_resenas,   {"resenas": []})

    # ─────────────────────────────────────────
    #  UTILIDADES INTERNAS
    # ─────────────────────────────────────────

    def _inicializar_archivo(self, ruta, estructura_base):
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(estructura_base, f, indent=4, ensure_ascii=False)

    def _cargar(self, ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, ruta, data):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _generar_id(self, lista):
        if not lista:
            return 1
        return max(item["id"] for item in lista) + 1

    # ─────────────────────────────────────────
    #  USUARIOS
    # ─────────────────────────────────────────

    def obtener_usuarios(self):
        return self._cargar(self.archivo_usuarios)["usuarios"]

    def obtener_usuario_por_id(self, usuario_id):
        return next(
            (u for u in self.obtener_usuarios() if u["id"] == usuario_id), None
        )

    def obtener_usuario_por_nombre(self, nombre_usuario):
        return next(
            (u for u in self.obtener_usuarios() if u["nombre_usuario"] == nombre_usuario), None
        )

    def agregar_usuario(self, nombre_usuario, contrasena_hash):
        data = self._cargar(self.archivo_usuarios)

        if any(u["nombre_usuario"] == nombre_usuario for u in data["usuarios"]):
            return None  # Ya existe

        nuevo_usuario = {
            "id"             : self._generar_id(data["usuarios"]),
            "nombre_usuario" : nombre_usuario,
            "contrasena_hash": contrasena_hash,
            "fecha_registro" : datetime.now().isoformat()
        }

        data["usuarios"].append(nuevo_usuario)
        self._guardar(self.archivo_usuarios, data)
        return nuevo_usuario

    # ─────────────────────────────────────────
    #  PELÍCULAS
    # ─────────────────────────────────────────

    def obtener_peliculas(self):
        return self._cargar(self.archivo_peliculas)["peliculas"]

    def obtener_pelicula_por_id(self, pelicula_id):
        return next(
            (p for p in self.obtener_peliculas() if p["id"] == pelicula_id), None
        )

    def obtener_pelicula_por_titulo(self, titulo):
        return next(
            (p for p in self.obtener_peliculas()
             if p["titulo"].lower() == titulo.lower()), None
        )

    def agregar_pelicula(self, titulo, descripcion=None, imagen=None,
                         fecha=None, anio=None, director=None):
        data = self._cargar(self.archivo_peliculas)

        # Reutiliza si ya existe con ese título
        existente = next(
            (p for p in data["peliculas"]
             if p["titulo"].lower() == titulo.lower()), None
        )
        if existente:
            return existente

        nueva_pelicula = {
            "id"         : self._generar_id(data["peliculas"]),
            "titulo"     : titulo,
            "descripcion": descripcion,
            "imagen"     : imagen,
            "fecha"      : fecha,
            "anio"       : anio,
            "director"   : director
        }

        data["peliculas"].append(nueva_pelicula)
        self._guardar(self.archivo_peliculas, data)
        return nueva_pelicula

    def editar_pelicula(self, pelicula_id, titulo=None, descripcion=None,
                        imagen=None, fecha=None, anio=None, director=None):
        data = self._cargar(self.archivo_peliculas)

        for pelicula in data["peliculas"]:
            if pelicula["id"] == pelicula_id:
                if titulo      is not None: pelicula["titulo"]      = titulo
                if descripcion is not None: pelicula["descripcion"] = descripcion
                if imagen      is not None: pelicula["imagen"]      = imagen
                if fecha       is not None: pelicula["fecha"]       = fecha
                if anio        is not None: pelicula["anio"]        = anio
                if director    is not None: pelicula["director"]    = director

                self._guardar(self.archivo_peliculas, data)
                return pelicula

        return None  # No encontrada

    def eliminar_pelicula(self, pelicula_id):
        data = self._cargar(self.archivo_peliculas)
        antes = len(data["peliculas"])
        data["peliculas"] = [p for p in data["peliculas"] if p["id"] != pelicula_id]

        if len(data["peliculas"]) < antes:
            self._guardar(self.archivo_peliculas, data)
            # Eliminar también todas sus reseñas
            self._eliminar_resenas_de_pelicula(pelicula_id)
            return True
        return False

    # ─────────────────────────────────────────
    #  RESEÑAS
    # ─────────────────────────────────────────

    def obtener_resenas(self):
        return self._cargar(self.archivo_resenas)["resenas"]

    def obtener_resena_por_id(self, resena_id):
        return next(
            (r for r in self.obtener_resenas() if r["id"] == resena_id), None
        )

    def obtener_resenas_por_usuario(self, usuario_id):
        return [r for r in self.obtener_resenas() if r["usuario_id"] == usuario_id]

    def obtener_resenas_por_pelicula(self, pelicula_id):
        return [r for r in self.obtener_resenas() if r["pelicula_id"] == pelicula_id]

    def agregar_resena(self, usuario_id, pelicula_id, texto,
                       valoracion_ia, etiquetas_ia):
        data = self._cargar(self.archivo_resenas)

        nueva_resena = {
            "id"                : self._generar_id(data["resenas"]),
            "usuario_id"        : usuario_id,
            "pelicula_id"       : pelicula_id,
            "texto"             : texto,
            "valoracion_ia"     : valoracion_ia,
            "etiquetas_ia"      : etiquetas_ia,
            "fecha_creacion"    : datetime.now().isoformat(),
            "fecha_modificacion": None
        }

        data["resenas"].append(nueva_resena)
        self._guardar(self.archivo_resenas, data)
        return nueva_resena

    def editar_resena(self, resena_id, usuario_id, nuevo_texto,
                      nueva_valoracion_ia, nuevas_etiquetas_ia):
        data = self._cargar(self.archivo_resenas)

        for resena in data["resenas"]:
            if resena["id"] == resena_id:
                if resena["usuario_id"] != usuario_id:
                    return None  # No autorizado

                resena["texto"]              = nuevo_texto
                resena["valoracion_ia"]      = nueva_valoracion_ia
                resena["etiquetas_ia"]       = nuevas_etiquetas_ia
                resena["fecha_modificacion"] = datetime.now().isoformat()

                self._guardar(self.archivo_resenas, data)
                return resena

        return None  # No encontrada

    def eliminar_resena(self, resena_id, usuario_id):
        data = self._cargar(self.archivo_resenas)

        resena = next((r for r in data["resenas"] if r["id"] == resena_id), None)

        if resena is None:
            return False
        if resena["usuario_id"] != usuario_id:
            return False

        data["resenas"] = [r for r in data["resenas"] if r["id"] != resena_id]
        self._guardar(self.archivo_resenas, data)
        return True

    def _eliminar_resenas_de_pelicula(self, pelicula_id):
        """Limpia todas las reseñas de una película eliminada."""
        data = self._cargar(self.archivo_resenas)
        data["resenas"] = [r for r in data["resenas"] if r["pelicula_id"] != pelicula_id]
        self._guardar(self.archivo_resenas, data)