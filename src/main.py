# src/main.py
from proceso import Proceso
from repositorio import RepositorioProcesos
from scheduler import FCFSScheduler, RoundRobinScheduler
from metrics import calcular_metricas

def mostrar_menu():
    print("\nGestor de Planificación de Procesos")
    print("1. Agregar proceso")
    print("2. Listar procesos")
    print("3. Guardar procesos (JSON)")
    print("4. Cargar procesos (JSON)")
    print("5. Guardar procesos (CSV)")
    print("6. Cargar procesos (CSV)")
    print("7. Ejecutar planificación FCFS")
    print("8. Ejecutar planificación Round-Robin")
    print("9. Salir")

def imprimir_gantt(gantt):
    print("\nDiagrama de Gantt:")
    for pid, inicio, fin in gantt:
        print(f"{pid}: {inicio} -> {fin}")

def main():
    repo = RepositorioProcesos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                pid = input("PID: ")
                duracion = int(input("Duración: "))
                prioridad = int(input("Prioridad: "))
                proceso = Proceso(pid, duracion, prioridad)
                repo.agregar(proceso)
                print("Proceso agregado.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "2":
            print("\nProcesos registrados:")
            for p in repo.listar():
                print(f"{p.pid}: duración={p.duracion}, prioridad={p.prioridad}")

        elif opcion == "3":
            archivo = input("Nombre del archivo JSON: ")
            repo.guardar_json(archivo)
            print("Procesos guardados.")

        elif opcion == "4":
            archivo = input("Nombre del archivo JSON: ")
            try:
                repo.cargar_json(archivo)
                print("Procesos cargados.")
            except Exception as e:
                print(f"Error: {e}")

