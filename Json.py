import json
import os


#  Configuración fdfsdfg
carpeta = "data"
archivo = f"{carpeta}/peliculas.json"



#  Leer datos
def cargar_datos():
    with open(archivo, "r") as f:
        return json.load(f)

#  Guardar datos
def guardar_datos(data):
    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)

#  Agregar película
def agregar_pelicula(titulo, descripcion, imagen, fecha):
    data = cargar_datos()

    nueva_pelicula = {
        "id": len(data["peliculas"]) + 1,
        "titulo": titulo,
        "descripcion": descripcion,
        "imagen": imagen,
        "fecha": fecha,
        "resenas": []
    }

    data["peliculas"].append(nueva_pelicula)
    guardar_datos(data)

    print(" Película agregada")

#  Simulación de modelo ML
def analizar_sentimiento(comentario):
    comentario = comentario.lower()

    if "buena" in comentario or "excelente" in comentario:
        return "positivo", 0.9
    elif "mala" in comentario or "horrible" in comentario:
        return "negativo", 0.2
    else:
        return "neutral", 0.5

#  Agregar reseña
def agregar_resena(id_pelicula, usuario, comentario):
    data = cargar_datos()

    sentimiento, score = analizar_sentimiento(comentario)

    for peli in data["peliculas"]:
        if peli["id"] == id_pelicula:
            peli["resenas"].append({
                "usuario": usuario,
                "comentario": comentario,
                "analisis": {
                    "sentimiento": sentimiento,
                    "score": score
                }
            })
            print("Reseña agregada")
            break
    else:
        print(" Película no encontrada")
        return

    guardar_datos(data)

#  Mostrar películas
def mostrar_peliculas():
    data = cargar_datos()

    if not data["peliculas"]:
        print("No hay películas")
        return

    for peli in data["peliculas"]:
        print(f"\nID: {peli['id']}")
        print(f"Título: {peli['titulo']}")
        print(f"Reseñas: {len(peli['resenas'])}")

#  MENÚ
while True:
    print("\n--- MENÚ ---")
    print("1. Agregar película")
    print("2. Agregar reseña")
    print("3. Ver películas")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        titulo = input("Título: ")
        descripcion = input("Descripción: ")
        imagen = input("Ruta de imagen: ")
        fecha = input("Fecha: ")

        agregar_pelicula(titulo, descripcion, imagen, fecha)

    elif opcion == "2":
        mostrar_peliculas()
        id_pelicula = int(input("ID de la película: "))
        usuario = input("Usuario: ")
        comentario = input("Comentario: ")

        agregar_resena(id_pelicula, usuario, comentario)

    elif opcion == "3":
        mostrar_peliculas()

    elif opcion == "4":
        print(" Saliendo...")
        break

    else:
        print(" Opción inválida")