from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Escuderia
from schemas import Escuderia as EscuderiaSchema, EscuderiaBase

router = APIRouter(prefix="/escuderias", tags=["Escuderías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[EscuderiaSchema])
def get_escuderias(db: Session = Depends(get_db)):
    return db.query(Escuderia).filter(Escuderia.activo == True).all()

@router.get("/{escuderia_id}", response_model=EscuderiaSchema)
def get_escuderia_by_id(escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id, Escuderia.activo == True).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escudería no encontrada")
    return esc

@router.get("/buscar/", response_model=list[EscuderiaSchema])
def buscar_escuderias(nombre: str = None, db: Session = Depends(get_db)):
    if not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un nombre")
    results = db.query(Escuderia).filter(Escuderia.nombre.ilike(f"%{nombre}%"), Escuderia.activo == True).all()
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron escuderías con ese nombre")
    return results

@router.post("/", response_model=EscuderiaSchema)
def create_escuderia(escuderia: EscuderiaBase, db: Session = Depends(get_db)):
    db_esc = Escuderia(**escuderia.dict())
    db.add(db_esc)
    db.commit()
    db.refresh(db_esc)
    return db_esc

@router.delete("/{escuderia_id}")
def eliminar_escuderia(escuderia_id: int, db: Session = Depends(get_db)):
    esc = db.query(Escuderia).filter(Escuderia.id == escuderia_id).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escudería no encontrada")
    esc.activo = False
    db.commit()
    return {"mensaje": f"Escudería {esc.nombre} fue marcada como eliminada"}

@router.get("/eliminados/", response_model=list[EscuderiaSchema])
def get_eliminadas(db: Session = Depends(get_db)):
    return db.query(Escuderia).filter(Escuderia.activo == False).all()
