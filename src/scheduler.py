# src/scheduler.py
from abc import ABC, abstractmethod
from typing import List, Tuple
from proceso import Proceso

GanttEntry = Tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        pass

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo_actual = 0
        gantt = []

        for proceso in procesos:
            proceso.tiempo_inicio = tiempo_actual
            tiempo_fin = tiempo_actual + proceso.duracion
            proceso.tiempo_fin = tiempo_fin
            gantt.append((proceso.pid, proceso.tiempo_inicio, tiempo_fin))
            tiempo_actual = tiempo_fin

        return gantt
class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int):
        if quantum <= 0:
            raise ValueError("El quantum debe ser mayor que 0.")
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo_actual = 0
        gantt = []
        cola = procesos.copy()  # Copia local para no modificar la lista original
        for p in cola:
            p.tiempo_restante = p.duracion
            p.tiempo_inicio = None  # Aún no empieza

        while cola:
            proceso = cola.pop(0)
            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual

            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            tiempo_fin = tiempo_actual + tiempo_ejecucion
            gantt.append((proceso.pid, tiempo_actual, tiempo_fin))

            proceso.tiempo_restante -= tiempo_ejecucion
            tiempo_actual = tiempo_fin

            if proceso.tiempo_restante > 0:
                cola.append(proceso)
            else:
                proceso.tiempo_fin = tiempo_actual

        return gantt
