import json
import csv
from typing import List, Optional
from src.proceso import Proceso

class RepositorioProcesos:
    """Clase que gestiona un conjunto de procesos activos con persistencia."""

    def __init__(self):
        """Inicializa un repositorio vacío."""
        self._procesos = {}  # Diccionario: pid -> Proceso

    def agregar(self, proceso: Proceso) -> None:
        """
        Agrega un proceso al repositorio.
        
        Args:
            proceso: Instancia de Proceso a agregar.
            
        Raises:
            ValueError: Si el proceso no es válido o el pid ya existe.
        """
        if not isinstance(proceso, Proceso):
            raise ValueError("El argumento debe ser una instancia de Proceso")
        if proceso.pid in self._procesos:
            raise ValueError(f"El PID '{proceso.pid}' ya existe en el repositorio")
        self._procesos[proceso.pid] = proceso

    def listar(self) -> List[Proceso]:
        """
        Devuelve una lista de todos los procesos registrados.
        
        Returns:
            Lista de procesos.
        """
        return list(self._procesos.values())

    def eliminar(self, pid: str) -> None:
        """
        Elimina un proceso dado su PID.
        
        Args:
            pid: Identificador del proceso.
            
        Raises:
            ValueError: Si el PID no existe.
        """
        if pid not in self._procesos:
            raise ValueError(f"El PID '{pid}' no existe en el repositorio")
        del self._procesos[pid]

    def obtener(self, pid: str) -> Optional[Proceso]:
        """
        Obtiene un proceso dado su PID.
        
        Args:
            pid: Identificador del proceso.
            
        Returns:
            El proceso si existe, None en caso contrario.
        """
        return self._procesos.get(pid)

    def guardar_json(self, archivo: str) -> None:
        """
        Guarda los procesos en un archivo JSON.
        
        Args:
            archivo: Ruta del archivo.
            
        Raises:
            IOError: Si no se puede escribir en el archivo.
        """
        try:
            datos = [
                {
                    "pid": p.pid,
                    "duracion": p.duracion,
                    "prioridad": p.prioridad,
                    "tiempo_restante": p.tiempo_restante,
                    "tiempo_llegada": p.tiempo_llegada,
                    "tiempo_inicio": p.tiempo_inicio,
                    "tiempo_fin": p.tiempo_fin
                }
                for p in self._procesos.values()
            ]
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        except IOError as e:
            raise IOError(f"Error al guardar en JSON: {e}")

    def cargar_json(self, archivo: str) -> None:
        """
        Carga procesos desde un archivo JSON, reemplazando los existentes.
        
        Args:
            archivo: Ruta del archivo.
            
        Raises:
            IOError: Si no se puede leer el archivo.
            ValueError: Si el formato es inválido o los datos son incorrectos.
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            if not isinstance(datos, list):
                raise ValueError("El archivo JSON debe contener una lista de procesos")
                
            # Limpiar procesos existentes
            self._procesos.clear()
            Proceso._pids_usados.clear()
            
            for item in datos:
                if not isinstance(item, dict):
                    raise ValueError("Cada proceso debe ser un diccionario")
                proceso = Proceso(
                    pid=item["pid"],
                    duracion=item["duracion"],
                    prioridad=item["prioridad"]
                )
                # Restaurar atributos adicionales
                proceso._tiempo_restante = item["tiempo_restante"]
                proceso._tiempo_llegada = item["tiempo_llegada"]
                proceso._tiempo_inicio = item["tiempo_inicio"]
                proceso._tiempo_fin = item["tiempo_fin"]
                self._procesos[proceso.pid] = proceso
        except IOError as e:
            raise IOError(f"Error al cargar desde JSON: {e}")
        except KeyError as e:
            raise ValueError(f"Falta un campo requerido en el JSON: {e}")
        except ValueError as e:
            raise ValueError(f"Error en los datos del JSON: {e}")

    def guardar_csv(self, archivo: str) -> None:
        """
        Guarda los procesos en un archivo CSV (separador: ;).
        
        Args:
            archivo: Ruta del archivo.
            
        Raises:
            IOError: Si no se puede escribir en el archivo.
        """
        try:
            with open(archivo, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                # Escribir encabezado
                writer.writerow([
                    "pid", "duracion", "prioridad", "tiempo_restante",
                    "tiempo_llegada", "tiempo_inicio", "tiempo_fin"
                ])
                # Escribir datos
                for p in self._procesos.values():
                    writer.writerow([
                        p.pid, p.duracion, p.prioridad, p.tiempo_restante,
                        p.tiempo_llegada, p.tiempo_inicio, p.tiempo_fin
                    ])
        except IOError as e:
            raise IOError(f"Error al guardar en CSV: {e}")

    def cargar_csv(self, archivo: str) -> None:
        """
        Carga procesos desde un archivo CSV, reemplazando los existentes.
        
        Args:
            archivo: Ruta del archivo.
            
        Raises:
            IOError: Si no se puede leer el archivo.
            ValueError: Si el formato es inválido o los datos son incorrectos.
        """
        try:
            with open(archivo, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f, delimiter=';')
                if not all(field in reader.fieldnames for field in [
                    "pid", "duracion", "prioridad", "tiempo_restante",
                    "tiempo_llegada", "tiempo_inicio", "tiempo_fin"
                ]):
                    raise ValueError("El CSV debe contener todas las columnas requeridas")
                
                # Limpiar procesos existentes
                self._procesos.clear()
                Proceso._pids_usados.clear()
                
                for row in reader:
                    # Convertir tipos
                    duracion = int(row["duracion"])
                    prioridad = int(row["prioridad"])
                    tiempo_restante = int(row["tiempo_restante"])
                    tiempo_llegada = int(row["tiempo_llegada"])
                    tiempo_inicio = None if row["tiempo_inicio"] == '' else int(row["tiempo_inicio"])
                    tiempo_fin = None if row["tiempo_fin"] == '' else int(row["tiempo_fin"])
                    
                    proceso = Proceso(
                        pid=row["pid"],
                        duracion=duracion,
                        prioridad=prioridad
                    )
                    # Restaurar atributos adicionales
                    proceso._tiempo_restante = tiempo_restante
                    proceso._tiempo_llegada = tiempo_llegada
                    proceso._tiempo_inicio = tiempo_inicio
                    proceso._tiempo_fin = tiempo_fin
                    self._procesos[proceso.pid] = proceso
        except IOError as e:
            raise IOError(f"Error al cargar desde CSV: {e}")
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error en los datos del CSV: {e}")