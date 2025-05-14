# tests/test_repositorio.py

import os
import pytest
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

@pytest.fixture
def repo():
    return RepositorioProcesos()

def test_agregar_y_listar_proceso(repo):
    p1 = Proceso("P1", 5, 1)
    repo.agregar_proceso(p1)
    procesos = repo.listar_procesos()
    assert len(procesos) == 1
    assert procesos[0].pid == "P1"

def test_pid_duplicado(repo):
    p1 = Proceso("P1", 5, 1)
    repo.agregar_proceso(p1)
    with pytest.raises(ValueError):
        repo.agregar_proceso(Proceso("P1", 3, 2))  # mismo PID

def test_eliminar_proceso(repo):
    p1 = Proceso("P1", 5, 1)
    repo.agregar_proceso(p1)
    repo.eliminar_proceso("P1")
    assert len(repo.listar_procesos()) == 0

def test_obtener_proceso(repo):
    p1 = Proceso("P1", 5, 1)
    repo.agregar_proceso(p1)
    p = repo.obtener_proceso("P1")
    assert p.duracion == 5

def test_guardar_y_cargar_json(tmp_path):
    repo = RepositorioProcesos()
    repo.agregar_proceso(Proceso("P1", 4, 2))
    ruta = tmp_path / "procesos.json"
    repo.guardar_en_json(ruta)

    nuevo_repo = RepositorioProcesos()
    nuevo_repo.cargar_desde_json(ruta)
    p = nuevo_repo.obtener_proceso("P1")
    assert p.duracion == 4
    assert p.prioridad == 2

def test_guardar_y_cargar_csv(tmp_path):
    repo = RepositorioProcesos()
    repo.agregar_proceso(Proceso("P1", 6, 0))
    ruta = tmp_path / "procesos.csv"
    repo.guardar_en_csv(ruta)

    nuevo_repo = RepositorioProcesos()
    nuevo_repo.cargar_desde_csv(ruta)
    p = nuevo_repo.obtener_proceso("P1")
    assert p.duracion == 6
    assert p.prioridad == 0
