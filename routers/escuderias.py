from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models import Escuderia as EscuderiaModel
from schemas import Escuderia as EscuderiaSchema, EscuderiaBase

router = APIRouter(prefix="/escuderias", tags=["Escuderías"])

@router.post("/", response_model=EscuderiaSchema, status_code=status.HTTP_201_CREATED)
def crear_escuderia(escuderia: EscuderiaBase, db: Session = Depends(get_db)):
    existente = db.query(EscuderiaModel).filter(EscuderiaModel.nombre == escuderia.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Escudería ya existente")
    nueva = EscuderiaModel(**escuderia.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[EscuderiaSchema])
def listar_escuderias(db: Session = Depends(get_db)):
    return db.query(EscuderiaModel).filter(EscuderiaModel.activo == True).all()

@router.put("/{id}", response_model=EscuderiaSchema)
def actualizar_escuderia(id: int, datos: EscuderiaBase, db: Session = Depends(get_db)):
    esc = db.query(EscuderiaModel).filter(EscuderiaModel.id == id).first()
    if not esc:
        raise HTTPException(404, detail="Escudería no encontrada")
    for k, v in datos.dict().items():
        setattr(esc, k, v)
    db.commit()
    db.refresh(esc)
    return esc

@router.delete("/{id}")
def eliminar_escuderia(id: int, db: Session = Depends(get_db)):
    esc = db.query(EscuderiaModel).filter(EscuderiaModel.id == id).first()
    if not esc:
        raise HTTPException(404, detail="Escudería no encontrada")
    esc.activo = False
    db.commit()
    return {"mensaje": "Escudería inactivada"}
