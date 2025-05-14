# src/scheduler.py

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.proceso import Proceso

# GanttEntry: (pid, tiempo_inicio, tiempo_fin)
GanttEntry = Tuple[str, int, int]

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """Planifica la ejecución de los procesos y devuelve el diagrama de Gantt."""
        pass
# src/scheduler.py (continuación)

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        gantt = []
        tiempo_actual = 0

        for proceso in procesos:
            proceso.tiempo_inicio = tiempo_actual
            tiempo_fin = tiempo_actual + proceso.duracion
            proceso.tiempo_fin = tiempo_fin

            gantt.append((proceso.pid, proceso.tiempo_inicio, proceso.tiempo_fin))
            tiempo_actual = tiempo_fin

        return gantt
# src/scheduler.py (continuación)

class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int):
        if quantum <= 0:
            raise ValueError("El quantum debe ser mayor que cero.")
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        gantt = []
        tiempo_actual = 0
        cola = procesos.copy()

        # Inicializamos los tiempos
        for p in cola:
            p.tiempo_restante = p.duracion
            p.tiempo_inicio = None

        while cola:
            proceso = cola.pop(0)

            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual

            ejecucion = min(self.quantum, proceso.tiempo_restante)
            tiempo_inicio = tiempo_actual
            tiempo_actual += ejecucion
            tiempo_fin = tiempo_actual
            proceso.tiempo_restante -= ejecucion

            gantt.append((proceso.pid, tiempo_inicio, tiempo_fin))

            if proceso.tiempo_restante > 0:
                cola.append(proceso)
            else:
                proceso.tiempo_fin = tiempo_actual

        return gantt
