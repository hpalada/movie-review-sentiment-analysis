# Json.py
import json
import os
from datetime import datetime


class JsonManager:
    def __init__(self):
        self.carpeta           = "data"
        self.archivo_peliculas = f"{self.carpeta}/peliculas.json"
        self.archivo_usuarios  = f"{self.carpeta}/usuarios.json"
        self.archivo_resenas   = f"{self.carpeta}/resenas.json"

        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

        self._inicializar_archivo(self.archivo_peliculas, {"peliculas": []})
        self._inicializar_archivo(self.archivo_usuarios,  {"usuarios": []})
        self._inicializar_archivo(self.archivo_resenas,   {"resenas": []})

        # ── Sincronizar promedios al iniciar ──────────────────────────
        self._sincronizar_promedios()

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

    def _sincronizar_promedios(self):
        """
        Al iniciar, garantiza que TODAS las películas tengan el campo
        promedio_calificacion. Si ya lo tienen, no los toca.
        Si no lo tienen, lo calcula y lo escribe.
        """
        data    = self._cargar(self.archivo_peliculas)
        cambios = False

        for pelicula in data["peliculas"]:
            if "promedio_calificacion" not in pelicula:
                resenas = self.obtener_resenas_por_pelicula(pelicula["id"])
                valoraciones = [
                    r["valoracion_ia"] for r in resenas
                    if isinstance(r.get("valoracion_ia"), (int, float))
                ]
                pelicula["promedio_calificacion"] = (
                    round(sum(valoraciones) / len(valoraciones), 2)
                    if valoraciones else None
                )
                cambios = True

        if cambios:
            self._guardar(self.archivo_peliculas, data)

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
            (u for u in self.obtener_usuarios()
             if u["nombre_usuario"] == nombre_usuario), None
        )

    def obtener_usuario_por_email(self, email):
        return next(
            (u for u in self.obtener_usuarios()
             if u.get("email", "").lower() == email.strip().lower()), None
        )

    def obtener_usuario_por_nombre_o_email(self, credencial):
        credencial = credencial.strip()
        for u in self.obtener_usuarios():
            if u["nombre_usuario"] == credencial:
                return u
            if u.get("email", "").lower() == credencial.lower():
                return u
        return None

    def agregar_usuario(self, nombre_usuario, contrasena_hash,
                        email="", rol="lector"):
        data = self._cargar(self.archivo_usuarios)

        if any(u["nombre_usuario"] == nombre_usuario for u in data["usuarios"]):
            return None

        if email and any(u.get("email", "").lower() == email.strip().lower()
                         for u in data["usuarios"]):
            return None

        rol_norm = "admin" if str(rol).lower().strip() in ("admin", "administrador") \
                   else "lector"

        nuevo_usuario = {
            "id"             : self._generar_id(data["usuarios"]),
            "nombre_usuario" : nombre_usuario,
            "email"          : email.strip().lower(),
            "contrasena_hash": contrasena_hash,
            "rol"            : rol_norm,
            "fecha_registro" : datetime.now().isoformat()
        }

        data["usuarios"].append(nuevo_usuario)
        self._guardar(self.archivo_usuarios, data)
        return nuevo_usuario

    def actualizar_contrasena(self, email, nueva_contrasena_hash):
        data = self._cargar(self.archivo_usuarios)
        for usuario in data["usuarios"]:
            if usuario.get("email", "").lower() == email.strip().lower():
                usuario["contrasena_hash"] = nueva_contrasena_hash
                self._guardar(self.archivo_usuarios, data)
                return True
        return False

    def actualizar_rol(self, email, nuevo_rol):
        rol_norm = "admin" if str(nuevo_rol).lower().strip() in \
                   ("admin", "administrador") else "lector"
        data = self._cargar(self.archivo_usuarios)
        for usuario in data["usuarios"]:
            if usuario.get("email", "").lower() == email.strip().lower():
                usuario["rol"] = rol_norm
                self._guardar(self.archivo_usuarios, data)
                return True
        return False

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

        existente = next(
            (p for p in data["peliculas"]
             if p["titulo"].lower() == titulo.lower()), None
        )
        if existente:
            return existente

        nueva_pelicula = {
            "id"                   : self._generar_id(data["peliculas"]),
            "titulo"               : titulo,
            "descripcion"          : descripcion,
            "imagen"               : imagen,
            "fecha"                : fecha,
            "anio"                 : anio,
            "director"             : director,
            "promedio_calificacion": None          # siempre presente desde el inicio
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

                # Garantiza que el campo siempre esté presente al editar
                if "promedio_calificacion" not in pelicula:
                    pelicula["promedio_calificacion"] = (
                        self.calcular_promedio_pelicula(pelicula_id)
                    )

                self._guardar(self.archivo_peliculas, data)
                return pelicula

        return None

    def eliminar_pelicula(self, pelicula_id):
        data  = self._cargar(self.archivo_peliculas)
        antes = len(data["peliculas"])
        data["peliculas"] = [p for p in data["peliculas"] if p["id"] != pelicula_id]

        if len(data["peliculas"]) < antes:
            self._guardar(self.archivo_peliculas, data)
            self._eliminar_resenas_de_pelicula(pelicula_id)
            return True
        return False

    # ─────────────────────────────────────────
    #  PROMEDIO DE CALIFICACIÓN
    # ─────────────────────────────────────────

    def calcular_promedio_pelicula(self, pelicula_id):
        resenas = self.obtener_resenas_por_pelicula(pelicula_id)
        valoraciones = [
            r["valoracion_ia"] for r in resenas
            if isinstance(r.get("valoracion_ia"), (int, float))
        ]
        if not valoraciones:
            return None
        return round(sum(valoraciones) / len(valoraciones), 2)

    def actualizar_promedio_pelicula(self, pelicula_id):
        data     = self._cargar(self.archivo_peliculas)
        promedio = self.calcular_promedio_pelicula(pelicula_id)

        for pelicula in data["peliculas"]:
            if pelicula["id"] == pelicula_id:
                pelicula["promedio_calificacion"] = promedio
                self._guardar(self.archivo_peliculas, data)
                return promedio

        return None

    def recalcular_todos_los_promedios(self):
        peliculas = self.obtener_peliculas()
        for pelicula in peliculas:
            self.actualizar_promedio_pelicula(pelicula["id"])
        print(f"✅ Promedios actualizados para {len(peliculas)} películas.")

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
        self.actualizar_promedio_pelicula(pelicula_id)
        return nueva_resena

    def editar_resena(self, resena_id, usuario_id, nuevo_texto,
                      nueva_valoracion_ia, nuevas_etiquetas_ia):
        data = self._cargar(self.archivo_resenas)

        for resena in data["resenas"]:
            if resena["id"] == resena_id:
                if resena["usuario_id"] != usuario_id:
                    return None
                resena["texto"]              = nuevo_texto
                resena["valoracion_ia"]      = nueva_valoracion_ia
                resena["etiquetas_ia"]       = nuevas_etiquetas_ia
                resena["fecha_modificacion"] = datetime.now().isoformat()
                self._guardar(self.archivo_resenas, data)
                self.actualizar_promedio_pelicula(resena["pelicula_id"])
                return resena

        return None

    def eliminar_resena(self, resena_id, usuario_id):
        data   = self._cargar(self.archivo_resenas)
        resena = next((r for r in data["resenas"] if r["id"] == resena_id), None)

        if resena is None:
            return False
        if resena["usuario_id"] != usuario_id:
            return False

        pelicula_id = resena["pelicula_id"]
        data["resenas"] = [r for r in data["resenas"] if r["id"] != resena_id]
        self._guardar(self.archivo_resenas, data)
        self.actualizar_promedio_pelicula(pelicula_id)
        return True

    def _eliminar_resenas_de_pelicula(self, pelicula_id):
        data = self._cargar(self.archivo_resenas)
        data["resenas"] = [r for r in data["resenas"]
                           if r["pelicula_id"] != pelicula_id]
        self._guardar(self.archivo_resenas, data)

    # ─────────────────────────────────────────
    #  MIGRACIÓN DEL JSON ANTIGUO
    # ─────────────────────────────────────────

    def migrar_json_antiguo(self, ruta_json_antiguo: str):
        if not os.path.exists(ruta_json_antiguo):
            print(f"❌ No se encontró el archivo: {ruta_json_antiguo}")
            return False

        with open(ruta_json_antiguo, "r", encoding="utf-8") as f:
            datos_antiguos = json.load(f)

        peliculas_antiguas = datos_antiguos.get("peliculas", [])
        data_peliculas = self._cargar(self.archivo_peliculas)
        data_usuarios  = self._cargar(self.archivo_usuarios)
        data_resenas   = self._cargar(self.archivo_resenas)

        if data_peliculas["peliculas"] or data_usuarios["usuarios"] \
                or data_resenas["resenas"]:
            print("⚠ Los archivos destino ya tienen datos. "
                  "Migración cancelada para evitar duplicados.")
            return False

        usuario_migrado = {
            "id"             : 1,
            "nombre_usuario" : "yo",
            "email"          : "",
            "contrasena_hash": "migrado_sin_hash",
            "rol"            : "lector",
            "fecha_registro" : datetime.now().isoformat()
        }
        data_usuarios["usuarios"].append(usuario_migrado)

        id_resena = 1
        for pelicula in peliculas_antiguas:
            nueva_pelicula = {
                "id"                   : pelicula.get("id"),
                "titulo"               : pelicula.get("titulo", ""),
                "descripcion"          : pelicula.get("descripcion", None),
                "imagen"               : pelicula.get("imagen", None),
                "fecha"                : pelicula.get("fecha", None),
                "anio"                 : None,
                "director"             : None,
                "promedio_calificacion": None      # siempre presente desde migración
            }
            data_peliculas["peliculas"].append(nueva_pelicula)

            for resena_antigua in pelicula.get("resenas", []):
                nueva_resena = {
                    "id"                : id_resena,
                    "usuario_id"        : 1,
                    "pelicula_id"       : pelicula["id"],
                    "texto"             : resena_antigua.get("comentario", ""),
                    "valoracion_ia"     : resena_antigua.get(
                        "analisis", {}).get("score", 0.0),
                    "etiquetas_ia"      : [resena_antigua.get(
                        "analisis", {}).get("sentimiento", "neutral")],
                    "fecha_creacion"    : datetime.now().isoformat(),
                    "fecha_modificacion": None
                }
                data_resenas["resenas"].append(nueva_resena)
                id_resena += 1

        self._guardar(self.archivo_peliculas, data_peliculas)
        self._guardar(self.archivo_usuarios,  data_usuarios)
        self._guardar(self.archivo_resenas,   data_resenas)

        self.recalcular_todos_los_promedios()

        print(f"✅ Migración completa:")
        print(f"   • {len(data_peliculas['peliculas'])} películas migradas")
        print(f"   • {len(data_usuarios['usuarios'])} usuario migrado")
        print(f"   • {len(data_resenas['resenas'])} reseñas migradas")
        return True