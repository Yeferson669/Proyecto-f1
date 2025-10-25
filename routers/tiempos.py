from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Tiempo, Piloto, Circuito
from schemas import Tiempo as TiempoSchema, TiempoBase

router = APIRouter(prefix="/tiempos", tags=["Tiempos"])

@router.post("/", response_model=TiempoSchema, status_code=status.HTTP_201_CREATED)
def crear_tiempo(tiempo: TiempoBase, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == tiempo.piloto_id).first()
    circuito = db.query(Circuito).filter(Circuito.id == tiempo.circuito_id).first()
    if not piloto or not circuito:
        raise HTTPException(400, "Piloto o circuito inválido")
    nuevo = Tiempo(**tiempo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[TiempoSchema])
def listar_tiempos(db: Session = Depends(get_db)):
    return db.query(Tiempo).options(joinedload(Tiempo.piloto), joinedload(Tiempo.circuito)).filter(Tiempo.activo == True).all()
