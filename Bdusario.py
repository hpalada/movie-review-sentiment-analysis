# =============================================================================
#  BDUsuario.py  –  Base de datos de usuarios (archivo JSON)
# =============================================================================
#
#  Responsabilidades:
#    · Crear el archivo BDUsuario.json si no existe
#    · Leer, escribir, buscar, insertar, actualizar y eliminar usuarios
#
#  NO tiene lógica de negocio, NO envía correos, NO tiene interfaz gráfica.
#  Solo se comunica con BDUsuario.json.
# =============================================================================

import json
import os
from ClaseUsuario import ClaseUsuario


BD_FILE = "BDUsuario.json"


class BDUsuario:
    """
    Clase encargada exclusivamente de la persistencia de usuarios
    en el archivo BDUsuario.json.

    Todos los métodos son estáticos — no necesitas instanciar la clase.

    Métodos
    -------
    cargar_todos()                    → dict { email: dict_datos }
    guardar_todos(datos)              → None
    buscar(email)                     → ClaseUsuario | None
    existe(email)                     → bool
    insertar(usuario: ClaseUsuario)   → tuple (ok, mensaje)
    actualizar(email, nuevos_datos)   → tuple (ok, mensaje)
    eliminar(email)                   → tuple (ok, mensaje)
    listar_todos()                    → list[ClaseUsuario]
    listar_emails()                   → list[str]
    """

    # ── Lectura ───────────────────────────────────────────────────────────────
    @staticmethod
    def cargar_todos() -> dict:
        """
        Lee BDUsuario.json y devuelve { email: dict_datos }.
        Si no existe, lo crea vacío automáticamente.
        """
        if not os.path.exists(BD_FILE):
            BDUsuario._inicializar_archivo()
            return {}

        with open(BD_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                BDUsuario._inicializar_archivo()
                return {}

    # ── Escritura ─────────────────────────────────────────────────────────────
    @staticmethod
    def guardar_todos(datos: dict) -> None:
        """Escribe el diccionario completo en BDUsuario.json."""
        with open(BD_FILE, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    # ── Búsqueda ──────────────────────────────────────────────────────────────
    @staticmethod
    def buscar(email: str) -> "ClaseUsuario | None":
        """
        Busca un usuario por email.
        Devuelve un objeto ClaseUsuario o None si no existe.
        """
        datos = BDUsuario.cargar_todos()
        raw   = datos.get(email.strip().lower())
        return ClaseUsuario.from_dict(raw) if raw else None

    @staticmethod
    def existe(email: str) -> bool:
        """Devuelve True si el email ya está registrado."""
        return email.strip().lower() in BDUsuario.cargar_todos()

    # ── Inserción ─────────────────────────────────────────────────────────────
    @staticmethod
    def insertar(usuario: ClaseUsuario) -> tuple:
        """
        Guarda un nuevo usuario en el JSON.

        Returns
        -------
        (True,  "")        – insertado correctamente
        (False, "mensaje") – el email ya existía
        """
        todos = BDUsuario.cargar_todos()

        if usuario.email in todos:
            return False, "Este correo ya está registrado."

        todos[usuario.email] = usuario.to_dict()
        BDUsuario.guardar_todos(todos)
        return True, ""

    # ── Actualización ─────────────────────────────────────────────────────────
    @staticmethod
    def actualizar(email: str, nuevos_datos: dict) -> tuple:
        """
        Actualiza campos específicos de un usuario existente.

        Returns
        -------
        (True,  "")        – actualizado correctamente
        (False, "mensaje") – el email no existe
        """
        email = email.strip().lower()
        todos = BDUsuario.cargar_todos()

        if email not in todos:
            return False, "Correo no encontrado en la base de datos."

        todos[email].update(nuevos_datos)
        BDUsuario.guardar_todos(todos)
        return True, ""

    # ── Eliminación ───────────────────────────────────────────────────────────
    @staticmethod
    def eliminar(email: str) -> tuple:
        """
        Elimina un usuario del JSON.

        Returns
        -------
        (True,  "")        – eliminado correctamente
        (False, "mensaje") – el email no existía
        """
        email = email.strip().lower()
        todos = BDUsuario.cargar_todos()

        if email not in todos:
            return False, "Correo no encontrado en la base de datos."

        del todos[email]
        BDUsuario.guardar_todos(todos)
        return True, ""

    # ── Listados ──────────────────────────────────────────────────────────────
    @staticmethod
    def listar_todos() -> list:
        """Devuelve lista de objetos ClaseUsuario de todos los registrados."""
        todos = BDUsuario.cargar_todos()
        return [ClaseUsuario.from_dict(datos) for datos in todos.values()]

    @staticmethod
    def listar_emails() -> list:
        """Devuelve lista de todos los correos registrados."""
        return list(BDUsuario.cargar_todos().keys())

    # ── Utilidad interna ──────────────────────────────────────────────────────
    @staticmethod
    def _inicializar_archivo() -> None:
        """Crea BDUsuario.json vacío si no existe o está corrupto."""
        with open(BD_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)
        print(f"✓ Archivo '{BD_FILE}' inicializado correctamente.")