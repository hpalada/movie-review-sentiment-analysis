from Json import JsonManager

_db = JsonManager()  # instancia única compartida

class Pelicula:
    def __init__(self, id, titulo, descripcion, imagen, fecha,
                 anio=None, director=None):
        self.id          = id
        self.titulo      = titulo
        self.descripcion = descripcion
        self.imagen      = imagen
        self.fecha       = fecha
        self.anio        = anio
        self.director    = director

    # ── Fábrica: construye un objeto desde el dict del JSON ──
    @classmethod
    def _desde_dict(cls, d):
        return cls(
            id=d["id"], titulo=d["titulo"],
            descripcion=d.get("descripcion"), imagen=d.get("imagen"),
            fecha=d.get("fecha"), anio=d.get("anio"), director=d.get("director")
        )

    # ── CRUD ─────────────────────────────────────────────────

    @classmethod
    def guardar(cls, titulo, descripcion=None, imagen=None,
                fecha=None, anio=None, director=None):
        """Crea y persiste una película nueva. Retorna el objeto."""
        datos = _db.agregar_pelicula(titulo, descripcion, imagen,
                                     fecha, anio, director)
        return cls._desde_dict(datos)

    @classmethod
    def buscar_por_id(cls, pelicula_id):
        datos = _db.obtener_pelicula_por_id(pelicula_id)
        return cls._desde_dict(datos) if datos else None

    @classmethod
    def buscar_por_titulo(cls, titulo):
        datos = _db.obtener_pelicula_por_titulo(titulo)
        return cls._desde_dict(datos) if datos else None

    @classmethod
    def todas(cls):
        return [cls._desde_dict(d) for d in _db.obtener_peliculas()]

    def actualizar(self, titulo=None, descripcion=None, imagen=None,
                   fecha=None, anio=None, director=None):
        """Actualiza en JSON y sincroniza los atributos del objeto."""
        datos = _db.editar_pelicula(
            self.id, titulo, descripcion, imagen, fecha, anio, director
        )
        if datos:
            self.titulo      = datos["titulo"]
            self.descripcion = datos["descripcion"]
            self.imagen      = datos["imagen"]
            self.fecha       = datos["fecha"]
            self.anio        = datos["anio"]
            self.director    = datos["director"]
        return datos is not None

    def eliminar(self):
        return _db.eliminar_pelicula(self.id)

    def to_dict(self):
        return {
            "id": self.id, "titulo": self.titulo,
            "descripcion": self.descripcion, "imagen": self.imagen,
            "fecha": self.fecha, "anio": self.anio, "director": self.director
        }