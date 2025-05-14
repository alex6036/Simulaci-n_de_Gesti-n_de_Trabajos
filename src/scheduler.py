from abc import ABC, abstractmethod
from typing import List, Tuple
from src.proceso import Proceso

# Definición de GanttEntry como una tupla
GanttEntry = Tuple[str, int, int]  # (pid, tiempo_inicio, tiempo_fin)

class Scheduler(ABC):
    """Clase abstracta que define la interfaz de un planificador."""
    
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica los procesos y devuelve un diagrama de Gantt.
        
        Args:
            procesos: Lista de procesos a planificar.
            
        Returns:
            Lista de entradas GanttEntry (pid, tiempo_inicio, tiempo_fin).
        """
        pass

class FCFSScheduler(Scheduler):
    """Planificador First-Come, First-Served (FCFS)."""
    
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica procesos en orden de llegada.
        
        Args:
            procesos: Lista de procesos a planificar.
            
        Returns:
            Lista de entradas GanttEntry.
            
        Raises:
            ValueError: Si la lista de procesos es inválida.
        """
        if not procesos or not all(isinstance(p, Proceso) for p in procesos):
            raise ValueError("Se requiere una lista no vacía de instancias de Proceso")

        gantt: List[GanttEntry] = []
        tiempo_actual = 0

        for proceso in procesos:
            # Establecer tiempo de inicio
            proceso.establecer_tiempo_inicio(tiempo_actual)
            # El proceso se ejecuta completamente
            tiempo_actual += proceso.duracion
            # Establecer tiempo de fin
            proceso.establecer_tiempo_fin(tiempo_actual)
            # Reducir tiempo restante a 0
            proceso.reducir_tiempo_restante(proceso.tiempo_restante)
            # Agregar entrada al diagrama de Gantt
            gantt.append((proceso.pid, proceso.tiempo_inicio, proceso.tiempo_fin))

        return gantt

class RoundRobinScheduler(Scheduler):
    """Planificador Round-Robin con quantum configurable."""
    
    def __init__(self, quantum: int):
        """
        Inicializa el planificador con un quantum específico.
        
        Args:
            quantum: Tiempo máximo de ejecución por ciclo.
            
        Raises:
            ValueError: Si el quantum no es positivo.
        """
        if not isinstance(quantum, int) or quantum <= 0:
            raise ValueError("El quantum debe ser un entero positivo")
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        """
        Planifica procesos usando Round-Robin.
        
        Args:
            procesos: Lista de procesos a planificar.
            
        Returns:
            Lista de entradas GanttEntry.
            
        Raises:
            ValueError: Si la lista de procesos es inválida.
        """
        if not procesos or not all(isinstance(p, Proceso) for p in procesos):
            raise ValueError("Se requiere una lista no vacía de instancias de Proceso")

        gantt: List[GanttEntry] = []
        tiempo_actual = 0
        cola = procesos.copy()  # Copia de la lista para no modificar la original
        procesos_pendientes = len(cola)

        while procesos_pendientes > 0:
            proceso = cola.pop(0)  # Tomar el primer proceso de la cola
            if proceso.tiempo_inicio is None:
                proceso.establecer_tiempo_inicio(tiempo_actual)

            # Determinar cuánto tiempo ejecutar
            tiempo_ejecucion = min(self.quantum, proceso.tiempo_restante)
            tiempo_inicio = tiempo_actual
            tiempo_actual += tiempo_ejecucion
            proceso.reducir_tiempo_restante(tiempo_ejecucion)

            # Agregar entrada al diagrama de Gantt
            gantt.append((proceso.pid, tiempo_inicio, tiempo_actual))

            if proceso.tiempo_restante > 0:
                # El proceso no ha terminado, vuelve a la cola
                cola.append(proceso)
            else:
                # El proceso ha terminado, establecer tiempo de fin
                proceso.establecer_tiempo_fin(tiempo_actual)
                procesos