# tests/test_metrics.py

import pytest
from src.proceso import Proceso
from src.metrics import calcular_metricas

def test_calcular_metricas():
    procesos = [
        Proceso(pid="P1", duracion=10, prioridad=2),
        Proceso(pid="P2", duracion=5, prioridad=1),
        Proceso(pid="P3", duracion=8, prioridad=3),
    ]
    
    # Simulación de tiempos
    procesos[0].tiempo_inicio = 0
    procesos[0].tiempo_fin = 10
    procesos[1].tiempo_inicio = 10
    procesos[1].tiempo_fin = 15
    procesos[2].tiempo_inicio = 15
    procesos[2].tiempo_fin = 23
    
    metrics = calcular_metricas(procesos)
    
    assert metrics['promedio_respuesta'] == 5
    assert metrics['promedio_retornado'] == 12.666666666666666
    assert metrics['promedio_espera'] == 2.6666666666666665
