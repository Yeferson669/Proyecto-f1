from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Circuito
from schemas import Circuito as CircuitoSchema, CircuitoBase

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])

@router.post("/", response_model=CircuitoSchema, status_code=status.HTTP_201_CREATED)
def crear_circuito(circuito: CircuitoBase, db: Session = Depends(get_db)):
    existente = db.query(Circuito).filter(Circuito.nombre == circuito.nombre).first()
    if existente:
        raise HTTPException(400, "Circuito ya existente")
    nuevo = Circuito(**circuito.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[CircuitoSchema])
def listar_circuitos(db: Session = Depends(get_db)):
    return db.query(Circuito).filter(Circuito.activo == True).all()
