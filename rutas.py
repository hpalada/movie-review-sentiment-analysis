# rutas.py
import os

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CARPETA_IMGS = os.path.join(BASE_DIR, "Imagenes")

def ruta_imagen(nombre_archivo: str) -> str:
    """
    Dado el valor guardado en el JSON, devuelve la ruta absoluta real.
    - Si es ruta absoluta (datos viejos): la devuelve tal cual.
    - Si es solo nombre de archivo: lo busca en Imagenes/.
    - Si es vacío o None: devuelve cadena vacía.
    """
    if not nombre_archivo:
        return ""
    if os.path.isabs(nombre_archivo):
        return nombre_archivo
    return os.path.join(CARPETA_IMGS, nombre_archivo)
