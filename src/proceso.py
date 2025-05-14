# src/proceso.py

class Proceso:
    _pids_registrados = set()  # Clase mantiene un registro global de PIDs

    def __init__(self, pid: str, duracion: int, prioridad: int):
        if not pid or not isinstance(pid, str):
            raise ValueError("El PID debe ser una cadena no vacía.")
        if pid in Proceso._pids_registrados:
            raise ValueError(f"El PID '{pid}' ya está registrado.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise ValueError("La duración debe ser un entero positivo.")
        if not isinstance(prioridad, int) or prioridad < 0:
            raise ValueError("La prioridad debe ser un entero no negativo.")

        self.pid = pid
        self.duracion = duracion
        self.prioridad = prioridad

        # Campos usados por el planificador
        self.tiempo_restante = duracion
        self.tiempo_llegada = 0  # simplificación
        self.tiempo_inicio = None
        self.tiempo_fin = None

        # Registrar el PID
        Proceso._pids_registrados.add(pid)

    def __repr__(self):
        return (f"Proceso(pid='{self.pid}', duracion={self.duracion}, "
                f"prioridad={self.prioridad})")

    def to_dict(self):
        return {
            "pid": self.pid,
            "duracion": self.duracion,
            "prioridad": self.prioridad
        }

    @staticmethod
    def from_dict(data: dict):
        return Proceso(
            pid=data["pid"],
            duracion=int(data["duracion"]),
            prioridad=int(data["prioridad"])
        )

    @classmethod
    def reset_registro(cls):
        """Permite limpiar el registro de PIDs (útil en pruebas o recarga desde archivo)."""
        cls._pids_registrados.clear()
