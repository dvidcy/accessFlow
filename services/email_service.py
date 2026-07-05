import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_EMAIL, SMTP_PASSWORD


def _enviar(destinatario: str, asunto: str, cuerpo_html: str) -> bool:
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = SMTP_EMAIL
        msg["To"]      = destinatario
        msg.attach(MIMEText(cuerpo_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.sendmail(SMTP_EMAIL, destinatario, msg.as_string())
        return True
    except Exception as e:
        print(f"[email_service] Error al enviar a {destinatario}: {e}")
        return False


def enviar_notificacion_entrada(tutor_email: str, alumno_nombre: str, hora: str) -> bool:
    asunto = f"✅ {alumno_nombre} llegó a la escuela"
    cuerpo = f"""
    <p>Estimado tutor,</p>
    <p>Le informamos que <strong>{alumno_nombre}</strong> registró su <strong>entrada</strong>
    a las <strong>{hora}</strong>.</p>
    <p>— AccessFlow</p>
    """
    return _enviar(tutor_email, asunto, cuerpo)


def enviar_notificacion_salida(tutor_email: str, alumno_nombre: str, hora: str) -> bool:
    asunto = f"🏠 {alumno_nombre} salió de la escuela"
    cuerpo = f"""
    <p>Estimado tutor,</p>
    <p>Le informamos que <strong>{alumno_nombre}</strong> registró su <strong>salida</strong>
    a las <strong>{hora}</strong>.</p>
    <p>— AccessFlow</p>
    """
    return _enviar(tutor_email, asunto, cuerpo)


def enviar_mensaje_personalizado(tutor_email: str, asunto: str, cuerpo: str) -> bool:
    cuerpo_html = f"<p>{cuerpo.replace(chr(10), '<br>')}</p><p>— AccessFlow</p>"
    return _enviar(tutor_email, asunto, cuerpo_html)
