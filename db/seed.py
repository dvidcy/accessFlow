"""
Script de datos de prueba. Ejecutar una sola vez:
  python db/seed.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import bcrypt
from db.database import engine, Base, get_session
from db.models import Grupo, Alumno, Tutor, Admin, alumno_tutor

def seed():
    Base.metadata.create_all(engine)
    session = get_session()

    if session.query(Admin).count() > 0:
        print("La BD ya tiene datos, omitiendo seed.")
        session.close()
        return

    # --- Grupos ---
    g1 = Grupo(nombre="1A", grado=1, turno="matutino")
    g2 = Grupo(nombre="2B", grado=2, turno="vespertino")
    session.add_all([g1, g2])
    session.flush()

    # --- Alumnos ---
    alumnos = [
        Alumno(nombre="Carlos Méndez",   grupo_id=g1.id),
        Alumno(nombre="Sofía Ramos",     grupo_id=g1.id),
        Alumno(nombre="Luis Herrera",    grupo_id=g1.id),
        Alumno(nombre="Valeria Torres",  grupo_id=g2.id),
        Alumno(nombre="Diego Morales",   grupo_id=g2.id),
    ]
    session.add_all(alumnos)
    session.flush()

    # --- Tutores ---
    t1 = Tutor(nombre="Ana Méndez",    email="ana@ejemplo.com",    telefono="555-0001")
    t2 = Tutor(nombre="Roberto Ramos", email="roberto@ejemplo.com", telefono="555-0002")
    t3 = Tutor(nombre="Lucía Torres",  email="lucia@ejemplo.com",  telefono="555-0003")
    session.add_all([t1, t2, t3])
    session.flush()

    # --- Relaciones alumno-tutor ---
    # Carlos tiene dos tutores (Ana y Roberto)
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[0].id, tutor_id=t1.id, parentesco="madre"))
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[0].id, tutor_id=t2.id, parentesco="padre"))
    # Sofía → Ana
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[1].id, tutor_id=t1.id, parentesco="madre"))
    # Luis → Roberto
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[2].id, tutor_id=t2.id, parentesco="padre"))
    # Valeria → Lucía
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[3].id, tutor_id=t3.id, parentesco="madre"))
    # Diego → Lucía
    session.execute(alumno_tutor.insert().values(alumno_id=alumnos[4].id, tutor_id=t3.id, parentesco="madre"))

    # --- Admin ---
    password_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
    admin = Admin(nombre="Administrador", email="admin@accessflow.com", password_hash=password_hash)
    session.add(admin)

    session.commit()
    session.close()
    print("Seed completado:")
    print("  2 grupos, 5 alumnos, 3 tutores, 1 admin")
    print("  Admin → admin@accessflow.com / admin123")

if __name__ == "__main__":
    seed()
