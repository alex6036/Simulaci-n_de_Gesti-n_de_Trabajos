# tests/test_scheduler.py
import pytest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

def test_fcfs_scheduler():
    procesos = [
        Proceso("P1", 5, 1),
        Proceso("P2", 3, 2),
        Proceso("P3", 2, 3)
    ]
    scheduler = FCFSScheduler()
    gantt = scheduler.planificar(procesos)
    assert gantt == [("P1", 0, 5), ("P2", 5, 8), ("P3", 8, 10)]
    assert procesos[0].tiempo_inicio == 0
    assert procesos[1].tiempo_inicio == 5
    assert procesos[2].tiempo_fin == 10

def test_round_robin_scheduler():
    procesos = [
        Proceso("P1", 4, 1),
        Proceso("P2", 3, 1)
    ]
    scheduler = RoundRobinScheduler(quantum=2)
    gantt = scheduler.planificar(procesos)

    assert gantt == [
        ("P1", 0, 2), ("P2", 2, 4),
        ("P1", 4, 6), ("P2", 6, 7)
    ]
