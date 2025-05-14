from typing import List, Dict, Tuple
from src.proceso import Proceso
from src.scheduler import GanttEntry

class Metrics:
    """Clase para calcular métricas de planificación de procesos."""

    def __init__(self, procesos: List[Proceso], gantt: List[GanttEntry]):
        """
        Inicializa las métricas con los procesos y el diagrama de Gantt.
        
        Args:
            procesos: Lista de procesos planificados.
            gantt: Lista de entradas GanttEntry (pid, tiempo_inicio, tiempo_fin).
            
        Raises:
            ValueError: Si los procesos o el diagrama de Gantt son inválidos.
        """
        if not procesos or not all(isinstance(p, Proceso) for p in procesos):
            raise ValueError("Se requiere una lista no vacía de instancias de Proceso")
        if not gantt or not all(isinstance(entry, tuple) and len(entry) == 3 for entry in gantt):
            raise ValueError("El diagrama de Gantt debe ser una lista no vacía de tuplas (pid, inicio, fin)")
        for proceso in procesos:
            if proceso.tiempo_inicio is None or proceso.tiempo_fin is None:
                raise ValueError(f"El proceso {proceso.pid} no tiene tiempos de inicio o fin definidos")
        
        self.procesos = procesos
        self.gantt = gantt
        self._metricas_por_proceso = None
        self._metricas_promedio = None
        self._calcular_metricas()

    def _calcular_metricas(self) -> None:
        """
        Calcula las métricas individuales y agregadas para los procesos.
        """
        self._metricas_por_proceso = {}
        suma_respuesta = 0
        suma_retorno = 0
        suma_espera = 0
        num_procesos = len(self.procesos)

        for proceso in self.procesos:
            # Tiempo de respuesta = tiempo_inicio - tiempo_llegada
            tiempo_respuesta = proceso.tiempo_inicio - proceso.tiempo_llegada
            # Tiempo de retorno = tiempo_fin - tiempo_llegada
            tiempo_retorno = proceso.tiempo_fin - proceso.tiempo_llegada
            # Tiempo de espera = tiempo_retorno - duración
            tiempo_espera = tiempo_retorno - proceso.duracion

            self._metricas_por_proceso[proceso.pid] = {
                "tiempo_respuesta": tiempo_respuesta,
                "tiempo_retorno": tiempo_retorno,
                "tiempo_espera": tiempo_espera
            }

            suma_respuesta += tiempo_respuesta
            suma_retorno += tiempo_retorno
            suma_espera += tiempo_espera

        # Calcular promedios
        self._metricas_promedio = {
            "promedio_respuesta": suma_respuesta / num_procesos,
            "promedio_retorno": suma_retorno / num_procesos,
            "promedio_espera": suma_espera / num_procesos
        }

    def obtener_metricas_por_proceso(self) -> Dict[str, Dict[str, float]]:
        """
        Devuelve las métricas individuales para cada proceso.
        
        Returns:
            Diccionario con métricas por PID.
        """
        return self._metricas_por_proceso

    def obtener_metricas_promedio(self) -> Dict[str, float]:
        """
        Devuelve las métricas promedio para el conjunto de procesos.
        
        Returns:
            Diccionario con promedios de tiempo de respuesta, retorno y espera.
        """
        return self._metricas_promedio

    def __str__(self) -> str:
        """
        Representación en cadena de las métricas.
        """
        result = ["Métricas por proceso:"]
        for pid, metricas in self._metricas_por_proceso.items():
            result.append(f"  {pid}:")
            result.append(f"    Tiempo de respuesta: {metricas['tiempo_respuesta']}")
            result.append(f"    Tiempo de retorno: {metricas['tiempo_retorno']}")
            result.append(f"    Tiempo de espera: {metricas['tiempo_espera']}")
        result.append("Métricas promedio:")
        result.append(f"  Tiempo de respuesta: {self._metricas_promedio['promedio_respuesta']:.2f}")
        result.append(f"  Tiempo de retorno: {self._metricas_promedio['promedio_retorno']:.2f}")
        result.append(f"  Tiempo de espera: {self._metricas_promedio['promedio_espera']:.2f}")
        return "\n".join(result)