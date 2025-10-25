from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from openpyxl import Workbook
from data import f1_data, pilotos_info, tiempos, circuitos
from database import Base, engine, SessionLocal
from fastapi import APIRouter
import models, schemas, csv, os
from data import tiempos


app = FastAPI(title="Fórmula 1 - Proyecto Integrador")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependencia BD



def _listar_pilotos_desde_data():
    lista = []
    for nombre, info in pilotos_info.items():
        # usar "numero" como id/identificador único
        id_val = info.get("numero") if isinstance(info.get("numero"), int) else None
        lista.append({
            "id": id_val,
            "nombre": nombre,
            "nacionalidad": info.get("pais"),
            "equipo": info.get("equipo"),
            "edad": info.get("edad"),
            "victorias": info.get("victorias"),
        })
    return lista



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pilotos")
def listar_pilotos_data():
    return _listar_pilotos_desde_data()


# GET /pilotos/{id} - buscar por número (id)
@app.get("/pilotos/{id}")
def obtener_piloto_por_id(id: int):
    for nombre, info in pilotos_info.items():
        if info.get("numero") == id:
            return {"id": info.get("numero"), "nombre": nombre, **info}
    raise HTTPException(status_code=404, detail=f"Piloto con id {id} no encontrado")

# ---------------------------------------------------------
# Páginas HTML
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "teams": f1_data})

@app.get("/team/{team_name}", response_class=HTMLResponse)
async def team_page(request: Request, team_name: str, db: Session = Depends(get_db)):
    team = f1_data.get(team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Escudería no encontrada")

    pilotos = [p for p in pilotos_info if p in team["pilotos"]]
    info_pilotos = {p: pilotos_info[p] for p in pilotos}
    return templates.TemplateResponse(
        "team.html",
        {"request": request, "team_name": team_name, "pilotos": info_pilotos},
    )

@app.get("/driver/{driver_name}", response_class=HTMLResponse)
async def driver_info(request: Request, driver_name: str):
    info = pilotos_info.get(driver_name)
    if not info:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return templates.TemplateResponse(
        "driver.html", {"request": request, "driver_name": driver_name, "info": info}
    )

# ---------------------------------------------------------
# API: CRUD ESCUDERÍAS
# ---------------------------------------------------------
@app.post("/escuderias", response_model=schemas.Escuderia)
def crear_escuderia(escuderia: schemas.EscuderiaBase, db: Session = Depends(get_db)):
    nueva = models.Escuderia(**escuderia.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/escuderias", response_model=list[schemas.Escuderia])
def listar_escuderias(db: Session = Depends(get_db)):
    return db.query(models.Escuderia).filter(models.Escuderia.activo == True).all()

@app.put("/escuderias/{id}", response_model=schemas.Escuderia)
def actualizar_escuderia(id: int, datos: schemas.EscuderiaBase, db: Session = Depends(get_db)):
    esc = db.query(models.Escuderia).filter(models.Escuderia.id == id).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escudería no encontrada")
    for key, value in datos.dict().items():
        setattr(esc, key, value)
    db.commit()
    db.refresh(esc)
    return esc

@app.delete("/escuderias/{id}")
def eliminar_escuderia(id: int, db: Session = Depends(get_db)):
    esc = db.query(models.Escuderia).filter(models.Escuderia.id == id).first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escudería no encontrada")
    esc.activo = False  # type: ignore # Borrado lógico
    db.commit()
    return {"mensaje": "Escudería marcada como inactiva"}

# ---------------------------------------------------------
# API: CRUD CIRCUITOS ✅ (nuevo)
# ---------------------------------------------------------
@app.post("/circuitos", response_model=schemas.Circuito)
def crear_circuito(circuito: schemas.CircuitoBase, db: Session = Depends(get_db)):
    nuevo = models.Circuito(**circuito.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/circuitos", response_model=list[schemas.Circuito])
def listar_circuitos(db: Session = Depends(get_db)):
    return db.query(models.Circuito).filter(models.Circuito.activo == True).all()

# ---------------------------------------------------------
# API: CRUD PILOTOS
# ---------------------------------------------------------
@app.post("/perfiles", response_model=schemas.PerfilPiloto)
def crear_perfil(perfil: schemas.PerfilPilotoBase, piloto_id: int, db: Session = Depends(get_db)):
    piloto = db.query(models.Piloto).filter(models.Piloto.id == piloto_id).first()
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    # verificar que no exista perfil
    exist = db.query(models.PerfilPiloto).filter(models.PerfilPiloto.piloto_id == piloto_id).first()
    if exist:
        raise HTTPException(status_code=400, detail="Piloto ya tiene perfil")
    nuevo = models.PerfilPiloto(**perfil.dict(), piloto_id=piloto_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/pilotos", response_model=schemas.Piloto)
def crear_piloto(piloto: schemas.PilotoBase, db: Session = Depends(get_db)):
    if piloto.escuderia_id is not None:
        esc = db.query(models.Escuderia).filter(
            models.Escuderia.id == piloto.escuderia_id,
            models.Escuderia.activo == True
        ).first()
        if not esc:
            raise HTTPException(status_code=400, detail="La escudería no existe o está inactiva")
        
        nro_exist = db.query(models.Piloto).filter(
            models.Piloto.escuderia_id == piloto.escuderia_id,
            models.Piloto.numero == piloto.numero,
            models.Piloto.activo == True
        ).first()
        if nro_exist:
            raise HTTPException(status_code=400, detail="Ya existe un piloto con ese número en la escudería")
    
    nuevo = models.Piloto(**piloto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/pilotos", response_model=list[schemas.Piloto])
def listar_pilotos(db: Session = Depends(get_db)):
    return db.query(models.Piloto).filter(models.Piloto.activo == True).all()

@app.put("/pilotos/{id}", response_model=schemas.Piloto)
def actualizar_piloto(id: int, datos: schemas.PilotoBase, db: Session = Depends(get_db)):
    piloto = db.query(models.Piloto).filter(models.Piloto.id == id).first()
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    for key, value in datos.dict().items():
        setattr(piloto, key, value)
    db.commit()
    db.refresh(piloto)
    return piloto

@app.delete("/pilotos/{id}")
def eliminar_piloto(id: int, db: Session = Depends(get_db)):
    piloto = db.query(models.Piloto).filter(models.Piloto.id == id).first()
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    piloto.activo = False # type: ignore
    db.commit()
    return {"mensaje": "Piloto marcado como inactivo"}

# ---------------------------------------------------------
# Filtros y búsquedas
# ---------------------------------------------------------
@app.get("/pilotos/filtro/{nacionalidad}")
def filtrar_por_nacionalidad(nacionalidad: str):
    try:
        pilotos = _listar_pilotos_desde_data()
        resultado = [
            p for p in pilotos
            if (p.get("nacionalidad") or "").strip().lower() == nacionalidad.strip().lower()
        ]
        if not resultado:
            # devolver mensaje 404 o lista vacía según prefieras; aquí devuelvo 404
            raise HTTPException(status_code=404, detail=f"No se encontraron pilotos con nacionalidad '{nacionalidad}'")
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        # para debug: muestra en consola por qué falló
        print("Error en /pilotos/filtro:", e)
        raise HTTPException(status_code=500, detail="Error interno al filtrar pilotos")


# GET /pilotos/buscar/{nombre}
@app.get("/pilotos/buscar/{nombre}")
def buscar_por_nombre(nombre: str):
    try:
        pilotos = _listar_pilotos_desde_data()
        nombre_norm = nombre.strip().lower()
        resultado = [p for p in pilotos if nombre_norm in (p["nombre"] or "").lower()]
        if not resultado:
            raise HTTPException(status_code=404, detail=f"No se encontraron pilotos con nombre que contenga '{nombre}'")
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        print("Error en /pilotos/buscar:", e)
        raise HTTPException(status_code=500, detail="Error interno al buscar piloto")
# ---------------------------------------------------------
# Reporte CSV
# ---------------------------------------------------------
@app.get("/reporte/pilotos")
def generar_reporte_pilotos():
    try:
        filename = "reporte_pilotos.csv"

        # Abre o crea el archivo CSV
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Escribe encabezados
            writer.writerow(["Piloto", "Escudería", "Circuitos", "Tiempo Promedio"])

            # Ejemplo: puedes obtener datos desde ranking_pilotos()
            from main import ranking_pilotos
            data = ranking_pilotos()

            for d in data:
                piloto = d.get("piloto", "Desconocido")
                circuitos = d.get("circuitos", 0)
                # Si tienes otra fuente de datos, agrega aquí más columnas
                escuderia = "Desconocida"
                tiempo_promedio = d.get("tiempo_promedio", "N/A")

                writer.writerow([piloto, escuderia, circuitos, tiempo_promedio])

        # Devuelve el archivo CSV como descarga
        return FileResponse(
            path=filename,
            filename=filename,
            media_type="text/csv"
        )

    except Exception as e:
        print("❌ Error generando CSV:", e)
        return {"error": str(e)}

@app.post("/pilotos/{piloto_id}/circuitos/{circuito_id}")
def asociar_piloto_circuito(piloto_id: int, circuito_id: int, db: Session = Depends(get_db)):
    piloto = db.query(models.Piloto).get(piloto_id)
    circuito = db.query(models.Circuito).get(circuito_id)
    if not piloto or not circuito:
        raise HTTPException(status_code=404, detail="Piloto o circuito no encontrado")
    piloto.circuitos.append(circuito)
    db.commit()
    return {"mensaje": "Asociación creada"}

# ---------------------------------------------------------
# Reportes
# ---------------------------------------------------------

@app.get("/reporte/pilotos/xlsx")
def reporte_pilotos_xlsx():
    try:
        # Crear archivo Excel en memoria
        wb = Workbook()
        ws = wb.active
        ws.title = "Pilotos"

        # Encabezados
        ws.append(["Piloto", "Escudería", "Circuitos", "Tiempo Promedio"])

        # Simulación de datos (puedes usar tu función ranking_pilotos)
        from main import ranking_pilotos
        data = ranking_pilotos()

        for d in data:
            escuderia = "Desconocida"
            # Si tienes un dict pilotos_info:
            # escuderia = pilotos_info.get(d["piloto"], {}).get("escuderia", "Desconocida")
            ws.append([d["piloto"], escuderia, d["circuitos"], d["tiempo_promedio"]])

        # Guardar archivo temporal
        filename = "reporte_pilotos.xlsx"
        wb.save(filename)

        # Enviar el archivo al navegador
        return FileResponse(
            path=filename,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        print("❌ Error generando reporte:", e)
        return {"error": str(e)}



@app.get("/report/ranking_pilotos")
def ranking_pilotos():
    ranking = {}

    for t in tiempos:
        piloto = t["piloto"]
        tiempo = t["tiempo"]
        circuito = t["circuito"]

        # Si no existe el piloto en el ranking, lo creamos
        if piloto not in ranking:
            ranking[piloto] = {"circuitos": set(), "tiempos": []}

        ranking[piloto]["circuitos"].add(circuito)
        ranking[piloto]["tiempos"].append(tiempo)

    # Creamos la lista final con promedios
    data = []
    for piloto, datos in ranking.items():
        promedio = sum(datos["tiempos"]) / len(datos["tiempos"])
        data.append({
            "piloto": piloto,
            "circuitos": len(datos["circuitos"]),
            "tiempo_promedio": round(promedio, 3)
        })

    # Agregar pilotos que no tienen tiempos (opcional)
    for piloto in pilotos_info.keys():
        if piloto not in ranking:
            data.append({
                "piloto": piloto,
                "circuitos": 0,
                "tiempo_promedio": None
            })

    # Ordenar por cantidad de circuitos y luego por tiempo promedio
    data_sorted = sorted(
        data,
        key=lambda x: (x["circuitos"], -x["tiempo_promedio"] if x["tiempo_promedio"] else float("inf")),
        reverse=True
    )

    return data_sorted