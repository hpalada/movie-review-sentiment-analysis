from Json import JsonManager
from clasePelicula import Pelicula
from claseResena import Resena

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

    def obtener_peliculas(self):
        return self.json_manager.cargar_datos()["peliculas"]

    def agregar_resena(self, id_pelicula, usuario, comentario):
        data = self.json_manager.cargar_datos()

        sentimiento, score = self.analizar_sentimiento(comentario)

        for peli in data["peliculas"]:
            if peli["id"] == id_pelicula:
                resena = Resena(usuario, comentario, sentimiento, score)
                peli["resenas"].append(resena.to_dict())
                break

        self.json_manager.guardar_datos(data)