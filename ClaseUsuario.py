# =============================================================================
#  clase_usuario.py  –  Representa a un usuario del sistema
# =============================================================================
#
#  Responsabilidades:
#    · Definir los atributos de un usuario
#    · Cifrar contraseñas con SHA-256
#    · Validar correo electrónico y contraseña
#    · Serializar / deserializar a diccionario (para JSON)
#
#  NO maneja archivos, NO envía correos, NO tiene interfaz gráfica.
# =============================================================================

import hashlib
import re
from datetime import datetime


class ClaseUsuario:
    """
    Representa a un usuario del sistema.

    Atributos
    ----------
    nombre_usuario : str – Nombre de usuario.
    email          : str – Correo electrónico (clave única).
    password       : str – Hash SHA-256 de la contraseña.
    creado         : str – Fecha/hora de creación (ISO 8601).
    """

    def __init__(self, nombre_usuario: str, email: str,
                 password_hash: str, creado: str = None):
        self.nombre_usuario = nombre_usuario.strip()
        self.email          = email.strip().lower()
        self.password       = password_hash
        self.creado         = creado or datetime.now().isoformat(timespec="seconds")

    def __repr__(self):
        return (f"ClaseUsuario("
                f"nombre_usuario={self.nombre_usuario!r}, "
                f"email={self.email!r}, "
                f"creado={self.creado!r})")

    # ── Serialización ─────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para guardarlo en el JSON."""
        return {
            "nombre_usuario": self.nombre_usuario,
            "email":          self.email,
            "password":       self.password,
            "creado":         self.creado,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ClaseUsuario":
        """Crea un objeto ClaseUsuario desde un diccionario leído del JSON."""
        return cls(
            nombre_usuario = data["nombre_usuario"],
            email          = data["email"],
            password_hash  = data["password"],
            creado         = data.get("creado"),
        )

    # ── Utilidades estáticas ──────────────────────────────────────────────────
    @staticmethod
    def hash_password(password: str) -> str:
        """Devuelve el hash SHA-256 de la contraseña en texto plano."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validar_email(email: str) -> tuple:
        """
        Valida el formato del correo electrónico.
        Returns (True, "") o (False, "mensaje de error")
        """
        patron = r'^[\w\.\-\+]+@[\w\.-]+\.\w{2,}$'
        if not email or not email.strip():
            return False, "El correo no puede estar vacío."
        if not re.match(patron, email.strip()):
            return False, "Formato de correo inválido. Ej: usuario@gmail.com"
        return True, ""

    @staticmethod
    def validar_password(password: str) -> tuple:
        """
        Valida la fortaleza de la contraseña.
        Returns (True, "") o (False, "mensaje de error")
        """
        if not password:
            return False, "La contraseña no puede estar vacía."
        if len(password) < 6:
            return False, "Debe tener al menos 6 caracteres."
        return True, ""

    @staticmethod
    def validar_nombre(nombre: str) -> tuple:
        """
        Valida que el nombre de usuario no esté vacío.
        Returns (True, "") o (False, "mensaje de error")
        """
        if not nombre or not nombre.strip():
            return False, "El nombre de usuario no puede estar vacío."
        if len(nombre.strip()) < 3:
            return False, "El nombre debe tener al menos 3 caracteres."
        return True, ""

    def verificar_password(self, password: str) -> bool:
        """Verifica si la contraseña en texto plano coincide con el hash."""
        return self.password == self.hash_password(password)