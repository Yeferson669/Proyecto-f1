from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Piloto, Escuderia
from schemas import Piloto as PilotoSchema, PilotoBase

router = APIRouter(prefix="/pilotos", tags=["Pilotos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[PilotoSchema])
def get_pilotos(db: Session = Depends(get_db)):
    return db.query(Piloto).filter(Piloto.activo == True).all()


@router.get("/{piloto_id}", response_model=PilotoSchema)
def get_piloto_by_id(piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id, Piloto.activo == True).first()
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto


@router.get("/buscar/", response_model=list[PilotoSchema])
def buscar_pilotos(nombre: str = None, db: Session = Depends(get_db)):
    if not nombre:
        raise HTTPException(status_code=400, detail="Debe proporcionar un nombre")
    resultados = db.query(Piloto).filter(Piloto.nombre.ilike(f"%{nombre}%"), Piloto.activo == True).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron pilotos con ese nombre")
    return resultados


@router.post("/", response_model=PilotoSchema)
def create_piloto(piloto: PilotoBase, db: Session = Depends(get_db)):
    db_piloto = Piloto(**piloto.dict())
    db.add(db_piloto)
    db.commit()
    db.refresh(db_piloto)
    return db_piloto


@router.delete("/{piloto_id}")
def eliminar_piloto(piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(Piloto).filter(Piloto.id == piloto_id).first()
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    piloto.activo = False
    db.commit()
    return {"mensaje": f"Piloto {piloto.nombre} fue marcado como eliminado"}


@router.get("/eliminados/", response_model=list[PilotoSchema])
def get_pilotos_eliminados(db: Session = Depends(get_db)):
    return db.query(Piloto).filter(Piloto.activo == False).all()
