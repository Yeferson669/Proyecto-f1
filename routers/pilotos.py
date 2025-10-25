from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Piloto, Escuderia, Circuito
from schemas import Piloto as PilotoSchema, PilotoBase

router = APIRouter(prefix="/pilotos", tags=["Pilotos"])

@router.post("/", response_model=PilotoSchema, status_code=status.HTTP_201_CREATED)
def crear_piloto(piloto: PilotoBase, db: Session = Depends(get_db)):
    if piloto.escuderia_id:
        esc = db.query(Escuderia).filter(Escuderia.id == piloto.escuderia_id, Escuderia.activo == True).first()
        if not esc:
            raise HTTPException(400, "Escudería no válida o inactiva")
    nuevo = Piloto(**piloto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[PilotoSchema])
def listar_pilotos(db: Session = Depends(get_db)):
    return db.query(Piloto).options(joinedload(Piloto.escuderia)).filter(Piloto.activo == True).all()

@router.put("/{id}", response_model=PilotoSchema)
def actualizar_piloto(id: int, datos: PilotoBase, db: Session = Depends(get_db)):
    p = db.query(Piloto).filter(Piloto.id == id).first()
    if not p:
        raise HTTPException(404, "Piloto no encontrado")
    for k, v in datos.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{id}")
def eliminar_piloto(id: int, db: Session = Depends(get_db)):
    p = db.query(Piloto).filter(Piloto.id == id).first()
    if not p:
        raise HTTPException(404, "Piloto no encontrado")
    p.activo = False
    db.commit()
    return {"mensaje": "Piloto inactivado"}

@router.post("/{piloto_id}/circuitos/{circuito_id}")
def asociar_piloto_circuito(piloto_id: int, circuito_id: int, db: Session = Depends(get_db)):
    p = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    c = db.query(Circuito).filter(Circuito.id == circuito_id).first()
    if not p or not c:
        raise HTTPException(404, "Piloto o circuito no encontrado")
    if c in p.circuitos:
        return {"mensaje": "Ya estaban asociados"}
    p.circuitos.append(c)
    db.commit()
    return {"mensaje": "Asociación creada correctamente"}
