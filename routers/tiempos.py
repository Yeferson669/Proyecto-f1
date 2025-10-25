from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Tiempo
from schemas import Tiempo as TiempoSchema, TiempoBase

router = APIRouter(prefix="/tiempos", tags=["Tiempos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TiempoSchema])
def get_tiempos(db: Session = Depends(get_db)):
    return db.query(Tiempo).all()

@router.get("/{tiempo_id}", response_model=TiempoSchema)
def get_tiempo_by_id(tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id).first()
    if not tiempo:
        raise HTTPException(status_code=404, detail="Tiempo no encontrado")
    return tiempo

@router.post("/", response_model=TiempoSchema)
def create_tiempo(tiempo: TiempoBase, db: Session = Depends(get_db)):
    db_tiempo = Tiempo(**tiempo.dict())
    db.add(db_tiempo)
    db.commit()
    db.refresh(db_tiempo)
    return db_tiempo

@router.delete("/{tiempo_id}")
def eliminar_tiempo(tiempo_id: int, db: Session = Depends(get_db)):
    tiempo = db.query(Tiempo).filter(Tiempo.id == tiempo_id).first()
    if not tiempo:
        raise HTTPException(status_code=404, detail="Tiempo no encontrado")
    db.delete(tiempo)
    db.commit()
    return {"mensaje": f"Tiempo con ID {tiempo_id} fue eliminado"}


