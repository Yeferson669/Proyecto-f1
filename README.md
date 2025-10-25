Proyecto F1 Pilotos

Proyecto F1 API es un sistema de gestión de información de Fórmula 1 desarrollado con FastAPI, SQLAlchemy y SQLite.  
Permite administrar **Escuderías, Pilotos, Circuitos, Perfiles y Tiempos, totalmente integrados.

---

Tecnologías principales

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy (ORM)**
- **SQLite (Base de datos local)**
- **Uvicorn (Servidor ASGI)**
- **Pydantic (Validación de datos)**

---

## 📂 Estructura del proyecto
Proyecto-f1/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
│
├── routers/
│ ├── escuderias.py
│ ├── pilotos.py
│ ├── circuitos.py
│ ├── perfiles.py
│ └── tiempos.py
│
├── f1_local.db # Se genera automáticamente al ejecutar
└── README.md


---

Instalación y ejecución

 Clonar el repositorio
bash
git clone https://github.com/Yeferson669/Proyecto-f1.git

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install requirements.txt
fastapi dev

**Diagrama entidad-relacion**
┌────────────┐      1 ────<      ┌────────────┐
│ ESCUDERIA  │──────────────────▶│   PILOTO   │
└────────────┘                   └────────────┘
                                     ││
                                     │└── 1:1 ───▶ PERFILES_PILOTO
                                     │
                                     ├── N:M ───▶ CIRCUITOS
                                     │
                                     └── 1:N ───▶ TIEMPOS


**Edpoints**
<img width="671" height="343" alt="image" src="https://github.com/user-attachments/assets/9cc1f8af-a74a-4801-a83f-4fa898f78cba" />

**Autor**
Yeferson David Guaca Buitron


