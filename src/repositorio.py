# src/repositorio.py
import json
import csv
from proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self._procesos = {}

    def agregar(self, proceso: Proceso):
        if proceso.pid in self._procesos:
            raise ValueError(f"Ya existe un proceso con PID {proceso.pid}.")
        self._procesos[proceso.pid] = proceso

    def listar(self):
        return list(self._procesos.values())

    def eliminar(self, pid: str):
        if pid in self._procesos:
            del self._procesos[pid]

    def obtener(self, pid: str) -> Proceso:
        return self._procesos.get(pid)

    def guardar_json(self, archivo: str):
        with open(archivo, 'w') as f:
            json.dump([vars(p) for p in self._procesos.values()], f, indent=4)

    def cargar_json(self, archivo: str):
        with open(archivo, 'r') as f:
            data = json.load(f)
        self._procesos = {d['pid']: Proceso(**d) for d in data}

    def guardar_csv(self, archivo: str):
        with open(archivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["pid", "duracion", "prioridad"])
            for p in self._procesos.values():
                writer.writerow([p.pid, p.duracion, p.prioridad])

    def cargar_csv(self, archivo: str):
        with open(archivo, newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            self._procesos = {}
            for row in reader:
                self.agregar(Proceso(pid=row["pid"], duracion=int(row["duracion"]), prioridad=int(row["prioridad"])))
