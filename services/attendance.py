from datetime import datetime, date
from typing import Optional
from db.database import get_session
from db.models import Alumno, Asistencia


def buscar_alumno_por_id(alumno_id: int) -> Optional[Alumno]:
    session = get_session()
    try:
        return session.query(Alumno).filter_by(id=alumno_id).first()
    finally:
        session.close()


def buscar_alumno_por_rfid(rfid_uid: str) -> Optional[Alumno]:
    session = get_session()
    try:
        return session.query(Alumno).filter_by(rfid_uid=rfid_uid).first()
    finally:
        session.close()


def registrar_asistencia(alumno_id: int) -> tuple[str, Asistencia]:
    """
    Detecta automáticamente si es entrada o salida:
    - Si no hay registro hoy → entrada
    - Si hay entrada pero no salida → salida
    - Si ya tiene entrada y salida → retorna aviso sin duplicar

    Retorna (tipo, registro): tipo es 'entrada', 'salida' o 'completo'
    """
    session = get_session()
    try:
        hoy = date.today()
        registro = (
            session.query(Asistencia)
            .filter(
                Asistencia.alumno_id == alumno_id,
                Asistencia.fecha_entrada >= datetime.combine(hoy, datetime.min.time()),
            )
            .first()
        )

        if registro is None:
            nuevo = Asistencia(alumno_id=alumno_id, fecha_entrada=datetime.now())
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
            return "entrada", nuevo

        if registro.fecha_salida is None:
            registro.fecha_salida = datetime.now()
            session.commit()
            session.refresh(registro)
            return "salida", registro

        return "completo", registro
    finally:
        session.close()


def get_asistencias_hoy() -> list[dict]:
    session = get_session()
    try:
        hoy = date.today()
        registros = (
            session.query(Asistencia)
            .filter(Asistencia.fecha_entrada >= datetime.combine(hoy, datetime.min.time()))
            .order_by(Asistencia.fecha_entrada.desc())
            .all()
        )

        resultado = []
        for r in registros:
            alumno = session.query(Alumno).filter_by(id=r.alumno_id).first()
            resultado.append({
                "alumno":        alumno.nombre if alumno else "—",
                "grupo":         f"{alumno.grupo.grado}° {alumno.grupo.nombre}" if alumno else "—",
                "fecha_entrada": r.fecha_entrada.strftime("%H:%M:%S"),
                "fecha_salida":  r.fecha_salida.strftime("%H:%M:%S") if r.fecha_salida else "—",
            })
        return resultado
    finally:
        session.close()
