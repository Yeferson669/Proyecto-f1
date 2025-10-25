# =====================================
# DATOS BASE DEL PROYECTO FORMULA 1 API
# =====================================

# ESTRUCTURA GENERAL DE EQUIPOS Y PILOTOS
f1_data = {
    "Red Bull": {"pilotos": ["Max Verstappen", "Sergio Pérez"]},
    "Ferrari": {"pilotos": ["Charles Leclerc", "Carlos Sainz"]},
    "Mercedes": {"pilotos": ["Lewis Hamilton", "George Russell"]},
    "McLaren": {"pilotos": ["Lando Norris", "Oscar Piastri"]},
    "Aston Martin": {"pilotos": ["Fernando Alonso", "Lance Stroll"]},
    "Alpine": {"pilotos": ["Esteban Ocon", "Pierre Gasly"]},
    "Williams": {"pilotos": ["Alex Albon", "Logan Sargeant"]},
    "RB": {"pilotos": ["Yuki Tsunoda", "Liam Lawson"]},
    "Kick Sauber": {"pilotos": ["Valtteri Bottas", "Zhou Guanyu"]},
    "Haas": {"pilotos": ["Kevin Magnussen", "Nico Hülkenberg"]},
}

# INFORMACIÓN DETALLADA DE PILOTOS
pilotos_info = {
    "Max Verstappen": {"id": 1, "numero": 1, "pais": "Países Bajos", "edad": 27, "equipo": "Red Bull", "victorias": 61},
    "Sergio Pérez": {"id": 2, "numero": 11, "pais": "México", "edad": 34, "equipo": "Red Bull", "victorias": 6},
    "Charles Leclerc": {"id": 3, "numero": 16, "pais": "Mónaco", "edad": 27, "equipo": "Ferrari", "victorias": 6},
    "Carlos Sainz": {"id": 4, "numero": 55, "pais": "España", "edad": 30, "equipo": "Ferrari", "victorias": 3},
    "Lewis Hamilton": {"id": 5, "numero": 44, "pais": "Reino Unido", "edad": 40, "equipo": "Mercedes", "victorias": 103},
    "George Russell": {"id": 6, "numero": 63, "pais": "Reino Unido", "edad": 27, "equipo": "Mercedes", "victorias": 1},
    "Lando Norris": {"id": 7, "numero": 4, "pais": "Reino Unido", "edad": 25, "equipo": "McLaren", "victorias": 1},
    "Oscar Piastri": {"id": 8, "numero": 81, "pais": "Australia", "edad": 24, "equipo": "McLaren", "victorias": 0},
    "Fernando Alonso": {"id": 9, "numero": 14, "pais": "España", "edad": 44, "equipo": "Aston Martin", "victorias": 32},
    "Lance Stroll": {"id": 10, "numero": 18, "pais": "Canadá", "edad": 27, "equipo": "Aston Martin", "victorias": 0},
    "Esteban Ocon": {"id": 11, "numero": 31, "pais": "Francia", "edad": 29, "equipo": "Alpine", "victorias": 1},
    "Pierre Gasly": {"id": 12, "numero": 10, "pais": "Francia", "edad": 29, "equipo": "Alpine", "victorias": 1},
    "Alex Albon": {"id": 13, "numero": 23, "pais": "Tailandia", "edad": 29, "equipo": "Williams", "victorias": 0},
    "Logan Sargeant": {"id": 14, "numero": 2, "pais": "Estados Unidos", "edad": 25, "equipo": "Williams", "victorias": 0},
    "Yuki Tsunoda": {"id": 15, "numero": 22, "pais": "Japón", "edad": 25, "equipo": "RB", "victorias": 0},
    "Liam Lawson": {"id": 16, "numero": 30, "pais": "Nueva Zelanda", "edad": 24, "equipo": "RB", "victorias": 0},
    "Valtteri Bottas": {"id": 17, "numero": 77, "pais": "Finlandia", "edad": 36, "equipo": "Kick Sauber", "victorias": 10},
    "Zhou Guanyu": {"id": 18, "numero": 24, "pais": "China", "edad": 26, "equipo": "Kick Sauber", "victorias": 0},
    "Kevin Magnussen": {"id": 19, "numero": 20, "pais": "Dinamarca", "edad": 33, "equipo": "Haas", "victorias": 0},
    "Nico Hülkenberg": {"id": 20, "numero": 27, "pais": "Alemania", "edad": 38, "equipo": "Haas", "victorias": 0},
}

# CIRCUITOS CON ID
circuitos = [
    {"id": 1, "nombre": "Monza", "pais": "Italia"},
    {"id": 2, "nombre": "Silverstone", "pais": "Reino Unido"},
    {"id": 3, "nombre": "Suzuka", "pais": "Japón"},
    {"id": 4, "nombre": "Monaco", "pais": "Mónaco"},
    {"id": 5, "nombre": "Interlagos", "pais": "Brasil"},
    {"id": 6, "nombre": "Spa-Francorchamps", "pais": "Bélgica"},
]

# TIEMPOS SIMULADOS COMPLETOS
tiempos = [
    # Red Bull
    {"piloto": "Max Verstappen", "circuito": "Monza", "tiempo": 78.9},
    {"piloto": "Max Verstappen", "circuito": "Silverstone", "tiempo": 81.1},
    {"piloto": "Sergio Pérez", "circuito": "Monaco", "tiempo": 72.8},
    {"piloto": "Sergio Pérez", "circuito": "Interlagos", "tiempo": 75.3},

    # Ferrari
    {"piloto": "Charles Leclerc", "circuito": "Monaco", "tiempo": 73.4},
    {"piloto": "Charles Leclerc", "circuito": "Spa-Francorchamps", "tiempo": 91.2},
    {"piloto": "Carlos Sainz", "circuito": "Monza", "tiempo": 79.9},
    {"piloto": "Carlos Sainz", "circuito": "Silverstone", "tiempo": 82.4},

    # Mercedes
    {"piloto": "Lewis Hamilton", "circuito": "Silverstone", "tiempo": 79.8},
    {"piloto": "Lewis Hamilton", "circuito": "Suzuka", "tiempo": 80.9},
    {"piloto": "George Russell", "circuito": "Spa-Francorchamps", "tiempo": 92.4},
    {"piloto": "George Russell", "circuito": "Monza", "tiempo": 80.5},

    # McLaren
    {"piloto": "Lando Norris", "circuito": "Suzuka", "tiempo": 81.1},
    {"piloto": "Lando Norris", "circuito": "Interlagos", "tiempo": 76.5},
    {"piloto": "Oscar Piastri", "circuito": "Monaco", "tiempo": 73.9},
    {"piloto": "Oscar Piastri", "circuito": "Interlagos", "tiempo": 75.6},

    # Aston Martin
    {"piloto": "Fernando Alonso", "circuito": "Monaco", "tiempo": 72.5},
    {"piloto": "Fernando Alonso", "circuito": "Silverstone", "tiempo": 81.9},
    {"piloto": "Lance Stroll", "circuito": "Spa-Francorchamps", "tiempo": 93.8},
    {"piloto": "Lance Stroll", "circuito": "Interlagos", "tiempo": 78.1},

    # Alpine
    {"piloto": "Esteban Ocon", "circuito": "Monaco", "tiempo": 74.1},
    {"piloto": "Esteban Ocon", "circuito": "Silverstone", "tiempo": 82.7},
    {"piloto": "Pierre Gasly", "circuito": "Spa-Francorchamps", "tiempo": 93.2},
    {"piloto": "Pierre Gasly", "circuito": "Monza", "tiempo": 81.4},

    # Williams
    {"piloto": "Alex Albon", "circuito": "Silverstone", "tiempo": 83.5},
    {"piloto": "Alex Albon", "circuito": "Monza", "tiempo": 82.2},
    {"piloto": "Logan Sargeant", "circuito": "Suzuka", "tiempo": 84.3},
    {"piloto": "Logan Sargeant", "circuito": "Spa-Francorchamps", "tiempo": 95.1},

    # RB
    {"piloto": "Yuki Tsunoda", "circuito": "Monaco", "tiempo": 74.6},
    {"piloto": "Yuki Tsunoda", "circuito": "Monza", "tiempo": 81.8},
    {"piloto": "Liam Lawson", "circuito": "Silverstone", "tiempo": 83.9},
    {"piloto": "Liam Lawson", "circuito": "Interlagos", "tiempo": 77.2},

    # Kick Sauber
    {"piloto": "Valtteri Bottas", "circuito": "Monza", "tiempo": 80.8},
    {"piloto": "Valtteri Bottas", "circuito": "Spa-Francorchamps", "tiempo": 92.9},
    {"piloto": "Zhou Guanyu", "circuito": "Silverstone", "tiempo": 84.4},
    {"piloto": "Zhou Guanyu", "circuito": "Suzuka", "tiempo": 85.2},

    # Haas
    {"piloto": "Kevin Magnussen", "circuito": "Monza", "tiempo": 82.7},
    {"piloto": "Kevin Magnussen", "circuito": "Interlagos", "tiempo": 79.4},
    {"piloto": "Nico Hülkenberg", "circuito": "Silverstone", "tiempo": 84.1},
    {"piloto": "Nico Hülkenberg", "circuito": "Spa-Francorchamps", "tiempo": 94.8},
]
