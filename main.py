from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import escuderias, pilotos, circuitos, perfiles, tiempos


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Fórmula 1 (SQLite)",
    version="3.0",
    description="F1 informacion de pilotos .",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)



app.include_router(escuderias.router)
app.include_router(pilotos.router)
app.include_router(circuitos.router)
app.include_router(perfiles.router)
app.include_router(tiempos.router)
