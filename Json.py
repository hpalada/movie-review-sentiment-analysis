import json
import os

class JsonManager:
    def __init__(self):
        self.carpeta = "data"
        self.archivo = f"{self.carpeta}/peliculas.json"

        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump({"peliculas": []}, f)

    def cargar_datos(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def guardar_datos(self, data):
        with open(self.archivo, "w") as f:
            json.dump(data, f, indent=4)