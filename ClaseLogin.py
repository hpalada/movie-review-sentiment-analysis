# =============================================================================
#  ClaseLogin.py  –  Lógica de autenticación, registro y cambio de contraseña
# =============================================================================
#
#  Usa:
#    · ClaseUsuario  → validaciones y hash de contraseña
#    · JsonManager   → persistencia en data/usuarios.json
#                      (el JsonManager original no se modifica)
#
#  NO tiene interfaz gráfica.
# =============================================================================

import smtplib
import ssl
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime             import datetime

from ClaseUsuario import ClaseUsuario
from Json  import JsonManager


# ── Configuración Gmail ───────────────────────────────────────────────────────
EMAIL_SENDER   = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 465

# Instancia única del JsonManager original (no modificado)
_db = JsonManager()


# =============================================================================
#  Módulo interno de correo
# =============================================================================

def _construir_html(titulo, saludo, cuerpo, color_header="#6c63ff"):
    return f"""
    <html><body style="margin:0;padding:0;background:#f4f4f8;
                       font-family:Helvetica,Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td align="center" style="padding:40px 20px;">
          <table width="480" cellpadding="0" cellspacing="0"
                 style="background:#fff;border-radius:12px;
                        box-shadow:0 4px 20px rgba(0,0,0,0.08);
                        overflow:hidden;">
            <tr><td style="background:{color_header};padding:32px 40px;
                           text-align:center;">
              <h1 style="margin:0;color:#fff;font-size:22px;
                         letter-spacing:1px;">{titulo}</h1>
            </td></tr>
            <tr><td style="padding:36px 40px;color:#333;font-size:15px;
                           line-height:1.7;">
              <p style="margin:0 0 16px;">Hola, <strong>{saludo}</strong> 👋</p>
              {cuerpo}
              <p style="margin:24px 0 0;font-size:13px;color:#888;">
                Si no realizaste esta acción, ignora este mensaje o
                contacta al administrador de inmediato.
              </p>
            </td></tr>
            <tr><td style="background:#f9f9fb;padding:20px 40px;
                           text-align:center;font-size:12px;color:#aaa;">
              Correo automático · No respondas a este mensaje
            </td></tr>
          </table>
        </td></tr>
      </table>
    </body></html>
    """


def _enviar_correo(destinatario, asunto, html, texto):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = destinatario
        msg.attach(MIMEText(texto, "plain", "utf-8"))
        msg.attach(MIMEText(html,  "html",  "utf-8"))

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        return True, ""

    except smtplib.SMTPAuthenticationError:
        return False, "Error de autenticación Gmail."
    except smtplib.SMTPException as e:
        return False, f"Error SMTP: {e}"
    except Exception as e:
        return False, f"Error inesperado: {e}"


def _plantilla_registro(nombre_usuario, email):
    asunto = "✦ ¡Bienvenido! Tu cuenta ha sido creada"
    cuerpo = f"""
        <p>Tu cuenta fue creada exitosamente con los siguientes datos:</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;">
          <tr>
            <td style="padding:10px;background:#f4f4f8;border-radius:6px;
                       font-weight:bold;width:40%;">Usuario</td>
            <td style="padding:10px;">{nombre_usuario}</td>
          </tr>
          <tr>
            <td style="padding:10px;font-weight:bold;">Correo</td>
            <td style="padding:10px;">{email}</td>
          </tr>
        </table>
        <p>Ya puedes iniciar sesión con tu correo y contraseña.</p>
    """
    html  = _construir_html("✦ Cuenta Creada", nombre_usuario, cuerpo, "#4ade80")
    texto = f"Hola {nombre_usuario},\n\nTu cuenta fue creada.\nCorreo: {email}\n\nYa puedes iniciar sesión."
    return asunto, html, texto


def _plantilla_login(nombre_usuario, email):
    fecha  = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    asunto = "◈ Inicio de sesión detectado en tu cuenta"
    cuerpo = f"""
        <p>Se detectó un inicio de sesión exitoso en tu cuenta.</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;">
          <tr>
            <td style="padding:10px;background:#f4f4f8;border-radius:6px;
                       font-weight:bold;width:40%;">Correo</td>
            <td style="padding:10px;">{email}</td>
          </tr>
          <tr>
            <td style="padding:10px;font-weight:bold;">Fecha y hora</td>
            <td style="padding:10px;">{fecha}</td>
          </tr>
        </table>
        <p>Si <strong>no reconoces</strong> esta actividad,
           cambia tu contraseña de inmediato.</p>
    """
    html  = _construir_html("◈ Inicio de Sesión", nombre_usuario, cuerpo, "#6c63ff")
    texto = f"Hola {nombre_usuario},\n\nInicio de sesión el {fecha}.\nSi no fuiste tú, cambia tu contraseña."
    return asunto, html, texto


def _plantilla_cambio_pass(nombre_usuario, email):
    fecha  = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    asunto = "⟳ Tu contraseña ha sido actualizada"
    cuerpo = f"""
        <p>Tu contraseña fue cambiada exitosamente.</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;">
          <tr>
            <td style="padding:10px;background:#f4f4f8;border-radius:6px;
                       font-weight:bold;width:40%;">Correo</td>
            <td style="padding:10px;">{email}</td>
          </tr>
          <tr>
            <td style="padding:10px;font-weight:bold;">Fecha y hora</td>
            <td style="padding:10px;">{fecha}</td>
          </tr>
        </table>
        <p>Si <strong>no realizaste este cambio</strong>,
           contacta al administrador de inmediato.</p>
    """
    html  = _construir_html("⟳ Contraseña Actualizada", nombre_usuario, cuerpo, "#ff6b9d")
    texto = f"Hola {nombre_usuario},\n\nContraseña cambiada el {fecha}.\nSi no fuiste tú, contacta al administrador."
    return asunto, html, texto


# =============================================================================
#  CLASE LOGIN
# =============================================================================
class ClaseLogin:
    """
    Lógica de autenticación, registro y cambio de contraseña.
    Usa los métodos del JsonManager original para toda la persistencia.

    Métodos del JsonManager que usa esta clase:
    ─────────────────────────────────────────────
    _db.obtener_usuario_por_nombre(nombre) → busca por nombre_usuario
    _db.agregar_usuario(nombre, hash)      → registra usuario nuevo
    """

    # ── Registro ──────────────────────────────────────────────────────────────
    @staticmethod
    def registrar(nombre_usuario, email, password, confirmar):
        """
        Valida los datos, guarda en JsonManager y envía correo.

        Returns  (ok: bool, error: str, aviso_correo: str)
        """
        # Validar campos con ClaseUsuario
        ok, msg = ClaseUsuario.validar_nombre(nombre_usuario)
        if not ok:
            return False, msg, ""

        ok, msg = ClaseUsuario.validar_email(email)
        if not ok:
            return False, msg, ""

        ok, msg = ClaseUsuario.validar_password(password)
        if not ok:
            return False, msg, ""

        if password != confirmar:
            return False, "Las contraseñas no coinciden.", ""

        # Verificar si el nombre_usuario ya existe usando JsonManager
        if _db.obtener_usuario_por_nombre(nombre_usuario) is not None:
            return False, "Este nombre de usuario ya está registrado.", ""

        # Guardar nuevo usuario usando JsonManager.agregar_usuario()
        resultado = _db.agregar_usuario(
            nombre_usuario  = nombre_usuario.strip(),
            contrasena_hash = ClaseUsuario.hash_password(password)
        )

        if resultado is None:
            return False, "No se pudo registrar el usuario.", ""

        # Enviar correo de bienvenida
        asunto, html, texto = _plantilla_registro(nombre_usuario.strip(), email)
        enviado, err = _enviar_correo(email.strip().lower(), asunto, html, texto)
        aviso = "" if enviado else f"Cuenta creada, pero el correo no se envió: {err}"

        return True, "", aviso

    # ── Autenticación ─────────────────────────────────────────────────────────
    @staticmethod
    def autenticar(email, password):
        """
        Busca el usuario por nombre en JsonManager y verifica contraseña.

        En el JsonManager original el campo de búsqueda es nombre_usuario,
        por lo que se usa el email como nombre_usuario para el login.

        Returns  (ok: bool, error: str, usuario: dict|None, aviso_correo: str)
        """
        if not email or not password:
            return False, "Completa todos los campos.", None, ""

        # Buscar en JsonManager por nombre_usuario (que en este sistema es el email)
        usuario = _db.obtener_usuario_por_nombre(email.strip().lower())

        if usuario is None:
            return False, "Correo no registrado.", None, ""

        # Verificar contraseña con ClaseUsuario
        if usuario["contrasena_hash"] != ClaseUsuario.hash_password(password):
            return False, "Contraseña incorrecta.", None, ""

        # Enviar correo de aviso
        asunto, html, texto = _plantilla_login(
            usuario["nombre_usuario"], email.strip().lower())
        enviado, err = _enviar_correo(email.strip().lower(), asunto, html, texto)
        aviso = "" if enviado else f"Sesión iniciada, pero el correo no se envió: {err}"

        return True, "", usuario, aviso

    # ── Cambio de contraseña ──────────────────────────────────────────────────
    @staticmethod
    def cambiar_password(email, nueva, confirmar):
        """
        Verifica que el usuario exista en JsonManager y actualiza su contraseña.

        Returns  (ok: bool, error: str, aviso_correo: str)
        """
        ok, msg = ClaseUsuario.validar_email(email)
        if not ok:
            return False, msg, ""

        ok, msg = ClaseUsuario.validar_password(nueva)
        if not ok:
            return False, msg, ""

        if nueva != confirmar:
            return False, "Las contraseñas no coinciden.", ""

        # Buscar usuario en JsonManager
        usuario = _db.obtener_usuario_por_nombre(email.strip().lower())
        if usuario is None:
            return False, "Correo no encontrado en el sistema.", ""

        # Actualizar contraseña directamente en el JSON via JsonManager
        data = _db._cargar(_db.archivo_usuarios)
        for u in data["usuarios"]:
            if u["nombre_usuario"] == email.strip().lower():
                u["contrasena_hash"] = ClaseUsuario.hash_password(nueva)
                break
        _db._guardar(_db.archivo_usuarios, data)

        # Enviar correo de confirmación
        asunto, html, texto = _plantilla_cambio_pass(
            usuario["nombre_usuario"], email.strip().lower())
        enviado, err = _enviar_correo(email.strip().lower(), asunto, html, texto)
        aviso = "" if enviado else f"Contraseña actualizada, pero el correo no se envió: {err}"

        return True, "", aviso