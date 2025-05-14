# src/repositorio.py

import json
import csv
from typing import List, Optional
from src.proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self.procesos: List[Proceso] = []

    def agregar(self, proceso: Proceso):
        if any(p.pid == proceso.pid for p in self.procesos):
            raise ValueError(f"Ya existe un proceso con PID '{proceso.pid}'.")
        self.procesos.append(proceso)

    def listar(self) -> List[Proceso]:
        return list(self.procesos)

    def eliminar(self, pid: str):
        self.procesos = [p for p in self.procesos if p.pid != pid]

    def obtener(self, pid: str) -> Optional[Proceso]:
        for p in self.procesos:
            if p.pid == pid:
                return p
        return None

    def limpiar(self):
        self.procesos.clear()
