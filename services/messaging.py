from datetime import datetime
from db.database import get_session
from db.models import Tutor, Alumno, Grupo, Mensaje, mensaje_destinatario
from services.email_service import enviar_mensaje_personalizado


def _guardar_mensaje(session, admin_id: int, asunto: str, cuerpo: str, tipo: str, tutores: list[Tutor]) -> Mensaje:
    msg = Mensaje(
        admin_id=admin_id,
        asunto=asunto,
        cuerpo=cuerpo,
        tipo=tipo,
        enviado_en=datetime.now(),
    )
    session.add(msg)
    session.flush()

    for tutor in tutores:
        session.execute(
            mensaje_destinatario.insert().values(mensaje_id=msg.id, tutor_id=tutor.id)
        )
    return msg


def enviar_mensaje_individual(tutor_id: int, asunto: str, cuerpo: str, admin_id: int) -> dict:
    session = get_session()
    try:
        tutor = session.query(Tutor).filter_by(id=tutor_id).first()
        if not tutor:
            return {"ok": False, "error": "Tutor no encontrado"}

        _guardar_mensaje(session, admin_id, asunto, cuerpo, "individual", [tutor])
        session.commit()

        enviado = enviar_mensaje_personalizado(tutor.email, asunto, cuerpo)
        return {"ok": enviado, "destinatarios": 1}
    except Exception as e:
        session.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        session.close()


def enviar_mensaje_grupal(grupo_id: int, asunto: str, cuerpo: str, admin_id: int) -> dict:
    session = get_session()
    try:
        grupo = session.query(Grupo).filter_by(id=grupo_id).first()
        if not grupo:
            return {"ok": False, "error": "Grupo no encontrado"}

        # Obtiene todos los tutores únicos del grupo
        alumnos = session.query(Alumno).filter_by(grupo_id=grupo_id).all()
        tutores_vistos = set()
        tutores = []
        for alumno in alumnos:
            for tutor in alumno.tutores:
                if tutor.id not in tutores_vistos:
                    tutores_vistos.add(tutor.id)
                    tutores.append(tutor)

        if not tutores:
            return {"ok": False, "error": "El grupo no tiene tutores registrados"}

        _guardar_mensaje(session, admin_id, asunto, cuerpo, "grupal", tutores)
        session.commit()

        enviados = sum(
            1 for t in tutores if enviar_mensaje_personalizado(t.email, asunto, cuerpo)
        )
        return {"ok": True, "destinatarios": len(tutores), "enviados": enviados}
    except Exception as e:
        session.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        session.close()


def get_tutores(search: str = "") -> list[Tutor]:
    session = get_session()
    try:
        q = session.query(Tutor)
        if search:
            q = q.filter(Tutor.nombre.ilike(f"%{search}%"))
        return q.order_by(Tutor.nombre).all()
    finally:
        session.close()


def get_grupos() -> list[Grupo]:
    session = get_session()
    try:
        return session.query(Grupo).order_by(Grupo.grado, Grupo.nombre).all()
    finally:
        session.close()
