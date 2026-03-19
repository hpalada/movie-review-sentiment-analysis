class Pelicula:
    def __init__(self, id, titulo, descripcion, imagen, fecha):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen = imagen
        self.fecha = fecha
        self.resenas = []

    def agregar_resena(self, resena):
        self.resenas.append(resena)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "fecha": self.fecha,
            "resenas": [r.to_dict() for r in self.resenas]
        }