from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CircuitoBase(BaseModel):
    nombre: str
    pais: Optional[str] = None
    longitud_km: Optional[int] = None
    activo: bool = True


class Circuito(CircuitoBase):
    id: int

    class Config:
        orm_mode = True



class PerfilPilotoBase(BaseModel):
    fecha_nacimiento: Optional[date] = None
    biografia: Optional[str] = None
    twitter: Optional[str] = None


class PerfilPiloto(PerfilPilotoBase):
    id: int
    piloto_id: int

    class Config:
        orm_mode = True



class PilotoBase(BaseModel):
    nombre: str
    nacionalidad: str
    numero: int
    activo: bool = True
    escuderia_id: Optional[int] = None


class Piloto(PilotoBase):
    id: int
    perfil: Optional[PerfilPiloto] = None
    circuitos: List[Circuito] = []

    class Config:
        orm_mode = True



class EscuderiaBase(BaseModel):
    nombre: str
    pais: str
    activo: bool = True


class Escuderia(EscuderiaBase):
    id: int
    pilotos: List[Piloto] = []

    class Config:
        orm_mode = True



class TiempoBase(BaseModel):
    piloto_id: int
    circuito_id: int
    tiempo_vuelta: float
    posicion: Optional[int] = None
    fecha: Optional[date] = None


class Tiempo(TiempoBase):
    id: int
    piloto: Optional[Piloto] = None
    circuito: Optional[Circuito] = None

    class Config:
        orm_mode = True
