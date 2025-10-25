from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float, Table
from sqlalchemy.orm import relationship
from database import Base

# ==========================================================
# TABLA INTERMEDIA MUCHOS A MUCHOS (Piloto - Circuito)
# ==========================================================
piloto_circuito = Table(
    "piloto_circuito",
    Base.metadata,
    Column("piloto_id", ForeignKey("pilotos.id"), primary_key=True),
    Column("circuito_id", ForeignKey("circuitos.id"), primary_key=True),
)

# ==========================================================
# MODELOS
# ==========================================================

class Escuderia(Base):
    __tablename__ = "escuderias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    pais = Column(String)
    activo = Column(Boolean, default=True)

    # Relación 1:N con pilotos
    pilotos = relationship("Piloto", back_populates="escuderia")


class Piloto(Base):
    __tablename__ = "pilotos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    nacionalidad = Column(String)
    numero = Column(Integer)
    activo = Column(Boolean, default=True)
    escuderia_id = Column(Integer, ForeignKey("escuderias.id"))

    escuderia = relationship("Escuderia", back_populates="pilotos")
    perfil = relationship("PerfilPiloto", back_populates="piloto", uselist=False)
    circuitos = relationship("Circuito", secondary=piloto_circuito, back_populates="pilotos")
    tiempos = relationship("Tiempo", back_populates="piloto")


class PerfilPiloto(Base):
    __tablename__ = "perfiles_piloto"

    id = Column(Integer, primary_key=True, index=True)
    piloto_id = Column(Integer, ForeignKey("pilotos.id"), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    biografia = Column(String, nullable=True)
    twitter = Column(String, nullable=True)

    piloto = relationship("Piloto", back_populates="perfil")


class Circuito(Base):
    __tablename__ = "circuitos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    pais = Column(String)
    longitud_km = Column(Integer)
    activo = Column(Boolean, default=True)

    pilotos = relationship("Piloto", secondary=piloto_circuito, back_populates="circuitos")
    tiempos = relationship("Tiempo", back_populates="circuito")


class Tiempo(Base):
    __tablename__ = "tiempos"

    id = Column(Integer, primary_key=True, index=True)
    piloto_id = Column(Integer, ForeignKey("pilotos.id"))
    circuito_id = Column(Integer, ForeignKey("circuitos.id"))
    tiempo_vuelta = Column(Float)
    posicion = Column(Integer)
    fecha = Column(Date)
    activo = Column(Boolean, default=True)

    piloto = relationship("Piloto", back_populates="tiempos")
    circuito = relationship("Circuito", back_populates="tiempos")
