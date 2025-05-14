# tests/test_scheduler.py

import pytest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

def test_fcfs_scheduler():
    procesos = [
        Proceso(pid="P1", duracion=10, prioridad=2),
        Proceso(pid="P2", duracion=5, prioridad=1),
        Proceso(pid="P3", duracion=8, prioridad=3),
    ]
    scheduler = FCFSScheduler()
    gantt = scheduler.planificar(procesos)
    
    assert gantt[0] == ("P1", 0, 10)
    assert gantt[1] == ("P2", 10, 15)
    assert gantt[2] == ("P3", 15, 23)

def test_round_robin_scheduler():
    procesos = [
        Proceso(pid="P1", duracion=10, prioridad=2),
        Proceso(pid="P2", duracion=5, prioridad=1),
        Proceso(pid="P3", duracion=8, prioridad=3),
    ]
    scheduler = RoundRobinScheduler(quantum=5)
    gantt = scheduler.planificar(procesos)
    
    assert gantt[0] == ("P1", 0, 5)
    assert gantt[1] == ("P2", 5, 10)
    assert gantt[2] == ("P3", 10, 15)
    assert gantt[3] == ("P1", 15, 20)
    assert gantt[4] == ("P3", 20, 23)
