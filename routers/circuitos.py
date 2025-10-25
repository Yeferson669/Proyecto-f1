from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Circuito
from schemas import Circuito as CircuitoSchema, CircuitoBase

router = APIRouter(prefix="/circuitos", tags=["Circuitos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CircuitoSchema])
def get_circuitos(db: Session = Depends(get_db)):
    return db.query(Circuito).filter(Circuito.activo == True).all()

@router.get("/{circuito_id}", response_model=CircuitoSchema)
def get_circuito_by_id(circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id, Circuito.activo == True).first()
    if not circuito:
        raise HTTPException(status_code=404, detail="Circuito no encontrado")
    return circuito

@router.get("/buscar/", response_model=list[CircuitoSchema])
def buscar_circuitos(nombre: str = None, db: Session = Depends(get_db)):
    if not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un nombre")
    resultados = db.query(Circuito).filter(Circuito.nombre.ilike(f"%{nombre}%"), Circuito.activo == True).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron circuitos con ese nombre")
    return resultados

@router.post("/", response_model=CircuitoSchema)
def create_circuito(circuito: CircuitoBase, db: Session = Depends(get_db)):
    db_circuito = Circuito(**circuito.dict())
    db.add(db_circuito)
    db.commit()
    db.refresh(db_circuito)
    return db_circuito

@router.delete("/{circuito_id}")
def eliminar_circuito(circuito_id: int, db: Session = Depends(get_db)):
    circuito = db.query(Circuito).filter(Circuito.id == circuito_id).first()
    if not circuito:
        raise HTTPException(status_code=404, detail="Circuito no encontrado")
    circuito.activo = False
    db.commit()
    return {"mensaje": f"Circuito {circuito.nombre} fue marcado como eliminado"}

@router.get("/eliminados/", response_model=list[CircuitoSchema])
def get_eliminados(db: Session = Depends(get_db)):
    return db.query(Circuito).filter(Circuito.activo == False).all()
