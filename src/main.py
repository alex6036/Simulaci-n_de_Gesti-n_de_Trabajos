from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.metrics import Metrics

def print_menu():
    """Prints the interactive menu."""
    print("\n=== Scheduler CLI ===")
    print("1. Agregar proceso")
    print("2. Listar procesos")
    print("3. Planificar procesos")
    print("4. Mostrar métricas")
    print("5. Guardar procesos")
    print("6. Cargar procesos")
    print("7. Salir")

def main():
    """Main function for the interactive CLI."""
    repositorio = RepositorioProcesos()
    gantt = None  # Store Gantt diagram for metrics

    while True:
        print_menu()
        opcion = input("Seleccione una opción (1-7): ")

        if opcion == "1":
            # Agregar proceso
            try:
                pid = input("Ingrese PID: ")
                duracion = int(input("Ingrese duración: "))
                prioridad = int(input("Ingrese prioridad: "))
                proceso = Proceso(pid, duracion, prioridad)
                repositorio.agregar(proceso)
                print(f"Proceso {pid} agregado exitosamente.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            # Listar procesos
            procesos = repositorio.listar()
            if not procesos:
                print("No hay procesos registrados.")
            else:
                print("Procesos registrados:")
                for proceso in procesos:
                    print(f"  {proceso}")

        elif opcion == "3":
            # Planificar procesos
            procesos = repositorio.listar()
            if not procesos:
                print("No hay procesos para planificar.")
                continue

            algoritmo = input("Seleccione algoritmo (fcfs/rr): ").lower()
            try:
                if algoritmo == "fcfs":
                    scheduler = FCFSScheduler()
                elif algoritmo == "rr":
                    quantum = int(input("Ingrese quantum: "))
                    scheduler = RoundRobinScheduler(quantum)
                else:
                    print("Algoritmo no válido. Use 'fcfs' o 'rr'.")
                    continue

                gantt = scheduler.planificar(procesos)
                print("Diagrama de Gantt:")
                for entry in gantt:
                    print(f"  {entry[0]}: {entry[1]} -> {entry[2]}")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            # Mostrar métricas
            procesos = repositorio.listar()
            if not procesos or not gantt:
                print("Primero debes planificar los procesos.")
                continue
            try:
                metrics = Metrics(procesos, gantt)
                print(metrics)
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "5":
            # Guardar procesos
            formato = input("Seleccione formato (json/csv): ").lower()
            archivo = input("Ingrese nombre del archivo: ")
            try:
                if formato == "json":
                    repositorio.guardar_json(archivo)
                elif formato == "csv":
                    repositorio.guardar_csv(archivo)
                else:
                    print("Formato no válido. Use 'json' o 'csv'.")
                    continue
                print(f"Procesos guardados en {archivo} ({formato}).")
            except (ValueError, IOError) as e:
                print(f"Error: {e}")

        elif opcion == "6":
            # Cargar procesos
            formato = input("Seleccione formato (json/csv): ").lower()
            archivo = input("Ingrese nombre del archivo: ")
            try:
                if formato == "json":
                    repositorio.cargar_json(archivo)
                elif formato == "csv":
                    repositorio.cargar_csv(archivo)
                else:
                    print("Formato no válido. Use 'json' o 'csv'.")
                    continue
                print(f"Procesos cargados desde {archivo} ({formato}).")
                gantt = None  # Reset Gantt after loading new processes
            except (ValueError, IOError) as e:
                print(f"Error: {e}")

        elif opcion == "7":
            # Salir
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor, seleccione un número entre 1 y 7.")

if __name__ == "__main__":
    main()