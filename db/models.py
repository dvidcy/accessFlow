from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

# Tabla intermedia Alumno <-> Tutor
alumno_tutor = Table(
    "alumno_tutor",
    Base.metadata,
    Column("alumno_id", Integer, ForeignKey("alumnos.id", ondelete="CASCADE"), primary_key=True),
    Column("tutor_id",  Integer, ForeignKey("tutores.id", ondelete="CASCADE"), primary_key=True),
    Column("parentesco", String(30), nullable=True),
)

# Tabla intermedia Mensaje <-> Tutor
mensaje_destinatario = Table(
    "mensaje_destinatario",
    Base.metadata,
    Column("mensaje_id", Integer, ForeignKey("mensajes.id", ondelete="CASCADE"), primary_key=True),
    Column("tutor_id",   Integer, ForeignKey("tutores.id", ondelete="CASCADE"), primary_key=True),
)


class Grupo(Base):
    __tablename__ = "grupos"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(10), nullable=False)
    grado  = Column(Integer, nullable=False)
    turno  = Column(Enum("matutino", "vespertino", "nocturno"), nullable=False)

    alumnos = relationship("Alumno", back_populates="grupo")

    def __repr__(self):
        return f"<Grupo {self.grado}° {self.nombre} — {self.turno}>"


class Alumno(Base):
    __tablename__ = "alumnos"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    nombre   = Column(String(100), nullable=False)
    rfid_uid = Column(String(50), unique=True, nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)

    grupo       = relationship("Grupo", back_populates="alumnos")
    tutores     = relationship("Tutor", secondary=alumno_tutor, back_populates="alumnos")
    asistencias = relationship("Asistencia", back_populates="alumno", cascade="all, delete")

    def __repr__(self):
        return f"<Alumno {self.nombre}>"


class Tutor(Base):
    __tablename__ = "tutores"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    nombre    = Column(String(100), nullable=False)
    email     = Column(String(150), nullable=False)
    telefono  = Column(String(20), nullable=True)

    alumnos  = relationship("Alumno", secondary=alumno_tutor, back_populates="tutores")
    mensajes = relationship("Mensaje", secondary=mensaje_destinatario, back_populates="destinatarios")

    def __repr__(self):
        return f"<Tutor {self.nombre}>"


class Admin(Base):
    __tablename__ = "admins"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    nombre        = Column(String(100), nullable=False)
    email         = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    mensajes = relationship("Mensaje", back_populates="admin")

    def __repr__(self):
        return f"<Admin {self.nombre}>"


class Asistencia(Base):
    __tablename__ = "asistencias"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    alumno_id      = Column(Integer, ForeignKey("alumnos.id", ondelete="CASCADE"), nullable=False)
    fecha_entrada  = Column(DateTime, nullable=False, default=datetime.now)
    fecha_salida   = Column(DateTime, nullable=True)

    alumno = relationship("Alumno", back_populates="asistencias")

    def __repr__(self):
        return f"<Asistencia alumno={self.alumno_id} entrada={self.fecha_entrada}>"


class Mensaje(Base):
    __tablename__ = "mensajes"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    admin_id   = Column(Integer, ForeignKey("admins.id"), nullable=False)
    asunto     = Column(String(200), nullable=False)
    cuerpo     = Column(Text, nullable=False)
    tipo       = Column(Enum("individual", "grupal"), nullable=False)
    enviado_en = Column(DateTime, default=datetime.now)

    admin         = relationship("Admin", back_populates="mensajes")
    destinatarios = relationship("Tutor", secondary=mensaje_destinatario, back_populates="mensajes")

    def __repr__(self):
        return f"<Mensaje '{self.asunto}' tipo={self.tipo}>"
