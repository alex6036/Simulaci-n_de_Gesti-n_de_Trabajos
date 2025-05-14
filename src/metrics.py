# src/metrics.py
from typing import List, Dict
from proceso import Proceso

def calcular_metricas(procesos: List[Proceso]) -> Dict[str, float]:
    tiempos_respuesta = []
    tiempos_retorno = []
    tiempos_espera = []

    for p in procesos:
        tr = p.tiempo_inicio - p.tiempo_llegada
        tt = p.tiempo_fin - p.tiempo_llegada
        te = tt - p.duracion

        tiempos_respuesta.append(tr)
        tiempos_retorno.append(tt)
        tiempos_espera.append(te)

    return {
        "respuesta_media": sum(tiempos_respuesta) / len(procesos),
        "retorno_media": sum(tiempos_retorno) / len(procesos),
        "espera_media": sum(tiempos_espera) / len(procesos)
    }
