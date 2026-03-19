from Json import JsonManager
from clasePelicula import Pelicula


class ServicioPeliculas:
    def __init__(self):
        self.json_manager = JsonManager()

    def analizar_sentimiento(self, comentario):
        comentario = comentario.lower()
        if "buena" in comentario or "excelente" in comentario:
            return "positivo", 0.9
        elif "mala" in comentario or "horrible" in comentario:
            return "negativo", 0.2
        else:
            return "neutral", 0.5

    def agregar_pelicula(self, titulo, descripcion, imagen, fecha):
        data = self.json_manager.cargar_datos()
        nueva = Pelicula(
            id=len(data["peliculas"]) + 1,
            titulo=titulo,
            descripcion=descripcion,
            imagen=imagen,
            fecha=fecha
        )
        data["peliculas"].append(nueva.to_dict())
        self.json_manager.guardar_datos(data)

    def actualizar_pelicula(self, id_pelicula, titulo, descripcion, imagen, fecha):
        data = self.json_manager.cargar_datos()
        for peli in data["peliculas"]:
            if peli["id"] == id_pelicula:
                peli["titulo"] = titulo
                peli["descripcion"] = descripcion
                peli["imagen"] = imagen
                peli["fecha"] = fecha
                break
        self.json_manager.guardar_datos(data)

    def eliminar_pelicula(self, id_pelicula):
        data = self.json_manager.cargar_datos()
        data["peliculas"] = [p for p in data["peliculas"] if p["id"] != id_pelicula]
        # Reasignar IDs
        for idx, p in enumerate(data["peliculas"], 1):
            p["id"] = idx
        self.json_manager.guardar_datos(data)

    def obtener_peliculas(self):
        return self.json_manager.cargar_datos()["peliculas"]

   