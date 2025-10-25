from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PerfilPiloto
from schemas import PerfilPiloto as PerfilSchema, PerfilPilotoBase

router = APIRouter(prefix="/perfiles", tags=["Perfiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PerfilSchema])
def get_perfiles(db: Session = Depends(get_db)):
    return db.query(PerfilPiloto).all()

@router.get("/{perfil_id}", response_model=PerfilSchema)
def get_perfil_by_id(perfil_id: int, db: Session = Depends(get_db)):
    perfil = db.query(PerfilPiloto).filter(PerfilPiloto.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

@router.post("/", response_model=PerfilSchema)
def create_perfil(perfil: PerfilPilotoBase, db: Session = Depends(get_db)):
    db_perfil = PerfilPiloto(**perfil.dict())
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

@router.delete("/{perfil_id}")
def eliminar_perfil(perfil_id: int, db: Session = Depends(get_db)):
    perfil = db.query(PerfilPiloto).filter(PerfilPiloto.id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    db.delete(perfil)
    db.commit()
    return {"mensaje": f"Perfil con ID {perfil_id} fue eliminado"}
