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
