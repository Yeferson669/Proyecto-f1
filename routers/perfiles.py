from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import PerfilPiloto, Piloto
from schemas import PerfilPiloto as PerfilSchema, PerfilPilotoBase

router = APIRouter(prefix="/perfiles", tags=["Perfiles Piloto"])

@router.post("/", response_model=PerfilSchema, status_code=status.HTTP_201_CREATED)
def crear_perfil(perfil: PerfilPilotoBase, piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if not piloto:
        raise HTTPException(404, "Piloto no encontrado")
    existente = db.query(PerfilPiloto).filter(PerfilPiloto.piloto_id == piloto_id).first()
    if existente:
        raise HTTPException(400, "El piloto ya tiene perfil")
    nuevo = PerfilPiloto(**perfil.dict(), piloto_id=piloto_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[PerfilSchema])
def listar_perfiles(db: Session = Depends(get_db)):
    return db.query(PerfilPiloto).all()
