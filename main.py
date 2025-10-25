from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import escuderias, pilotos, circuitos, perfiles, tiempos

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# CONFIGURACIÓN FASTAPI
# -------------------------------------------------
app = FastAPI(
    title="API Fórmula 1 (SQLite)",
    version="3.0",
    description="API para gestionar Escuderías, Pilotos, Circuitos, Perfiles y Tiempos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Fórmula 1. Visita /docs para probar los endpoints."}

# -------------------------------------------------
# INCLUIR ROUTERS
# -------------------------------------------------
app.include_router(escuderias.router)
app.include_router(pilotos.router)
app.include_router(circuitos.router)
app.include_router(perfiles.router)
app.include_router(tiempos.router)
