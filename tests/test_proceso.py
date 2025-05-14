# tests/test_proceso.py

import pytest
from src.proceso import Proceso

def test_creacion_proceso_valido():
    proceso = Proceso(pid="P1", duracion=10, prioridad=2)
    assert proceso.pid == "P1"
    assert proceso.duracion == 10
    assert proceso.prioridad == 2

def test_creacion_proceso_pid_duplicado():
    Proceso(pid="P1", duracion=10, prioridad=2)
    with pytest.raises(ValueError):
        Proceso(pid="P1", duracion=5, prioridad=1)
