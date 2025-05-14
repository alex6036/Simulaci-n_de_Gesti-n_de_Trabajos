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
