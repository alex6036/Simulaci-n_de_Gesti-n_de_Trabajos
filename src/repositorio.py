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


# src/repositorio.py (continuación)

    def guardar_json(self, ruta: str):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.procesos], f, indent=4)

    def cargar_json(self, ruta: str):
        from src.proceso import Proceso
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.procesos.clear()
        Proceso.reset_registro()
        for d in datos:
            self.agregar(Proceso.from_dict(d))

    def guardar_csv(self, ruta: str):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["pid", "duracion", "prioridad"])
            for p in self.procesos:
                writer.writerow([p.pid, p.duracion, p.prioridad])

    def cargar_csv(self, ruta: str):
        from src.proceso import Proceso
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            self.procesos.clear()
            Proceso.reset_registro()
            for row in reader:
                self.agregar(Proceso.from_dict(row))
