import sys
from PyQt6.QtWidgets import QApplication
from Json import JsonManager
from ClaseReseña import Resena
from FormReseñas import FormResenas


if __name__ == "__main__":
    app = QApplication(sys.argv)

    jm           = JsonManager()
    clase_resena = Resena()

    # Tomamos el primer usuario y la primera película del JSON
    usuario  = jm.obtener_usuarios()[0]
    pelicula = jm.obtener_peliculas()[0]
    print("USUARIO:", usuario)
    print("PELÍCULA:", pelicula)

    form = FormResenas(
        pelicula_id     = pelicula["id"],
        usuario_id      = usuario["id"],
        clase_pelicula  = None,               # aún no está implementada
        clase_resena    = clase_resena,
        titulo_pelicula = pelicula["titulo"]
    )
    form.show()

    sys.exit(app.exec())