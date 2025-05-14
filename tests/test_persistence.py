# tests/test_persistence.py

import os
import pytest
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

@pytest.fixture
def repo():
    repo = RepositorioProcesos()
    repo.limpiar()
    return repo

def test_guardar_y_cargar_json(repo):
    p1 = Proceso(pid="P1", duracion=10, prioridad=2)
    p2 = Proceso(pid="P2", duracion=5, prioridad=1)
    repo.agregar(p1)
    repo.agregar(p2)
    
    repo.guardar_json("procesos_test.json")
    repo.limpiar()
    
    repo.cargar_json("procesos_test.json")
    procesos_cargados = repo.listar()
    
    assert len(procesos_cargados) == 2
    assert procesos_cargados[0].pid == "P1"
    assert procesos_cargados[1].pid == "P2"
    
    os.remove("procesos_test.json")

def test_guardar_y_cargar_csv(repo):
    p1 = Proceso(pid="P1", duracion=10, prioridad=2)
    p2 = Proceso(pid="P2", duracion=5, prioridad=1)
    repo.agregar(p1)
    repo.agregar(p2)
    
    repo.guardar_csv("procesos_test.csv")
    repo.limpiar()
    
    repo.cargar_csv("procesos_test.csv")
    procesos_cargados = repo.listar()
    
    assert len(procesos_cargados) == 2
    assert procesos_cargados[0].pid == "P1"
    assert procesos_cargados[1].pid == "P2"
    
    os.remove("procesos_test.csv")
