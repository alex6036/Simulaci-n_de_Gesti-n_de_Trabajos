# src/metrics.py

from typing import List
from src.proceso import Proceso

def calcular_metricas(procesos: List[Proceso]) -> dict:
    """
    Calcula las métricas de tiempo para cada proceso y de forma agregada.
    - Tiempo de respuesta = tiempo_inicio - tiempo_llegada
    - Tiempo de retorno = tiempo_fin - tiempo_llegada
    - Tiempo de espera = tiempo_retornado - duracion
    """
    tiempos_respuesta = []
    tiempos_retornado = []
    tiempos_espera = []

    for proceso in procesos:
        tiempo_respuesta = proceso.tiempo_inicio - proceso.tiempo_llegada
        tiempo_retornado = proceso.tiempo_fin - proceso.tiempo_llegada
        tiempo_espera = tiempo_retornado - proceso.duracion

        tiempos_respuesta.append(tiempo_respuesta)
        tiempos_retornado.append(tiempo_retornado)
        tiempos_espera.append(tiempo_espera)

    # Cálculo promedio de las métricas
    promedio_respuesta = sum(tiempos_respuesta) / len(procesos) if procesos else 0
    promedio_retornado = sum(tiempos_retornado) / len(procesos) if procesos else 0
    promedio_espera = sum(tiempos_espera) / len(procesos) if procesos else 0

    return {
        "promedio_respuesta": promedio_respuesta,
        "promedio_retornado": promedio_retornado,
        "promedio_espera": promedio_espera
    }

