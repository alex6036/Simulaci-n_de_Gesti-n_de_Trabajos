import click
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.metrics import Metrics

@click.group()
@click.pass_context
def cli(ctx):
    """CLI para gestionar y planificar procesos."""
    ctx.obj = {"repositorio": RepositorioProcesos()}

@cli.command()
@click.argument("pid")
@click.argument("duracion", type=int)
@click.argument("prioridad", type=int)
@click.pass_context
def add(ctx, pid, duracion, prioridad):
    """Agrega un proceso al repositorio."""
    try:
        proceso = Proceso(pid, duracion, prioridad)
        ctx.obj["repositorio"].agregar(proceso)
        click.echo(f"Proceso {pid} agregado exitosamente.")
    except ValueError as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.pass_context
def list(ctx):
    """Lista todos los procesos registrados."""
    procesos = ctx.obj["repositorio"].listar()
    if not procesos:
        click.echo("No hay procesos registrados.")
        return
    for proceso in procesos:
        click.echo(str(proceso))

@cli.command()
@click.argument("algoritmo", type=click.Choice(["fcfs", "rr"]))
@click.option("--quantum", type=int, default=2, help="Quantum para Round-Robin")
@click.pass_context
def plan(ctx, algoritmo, quantum):
    """Planifica los procesos usando el algoritmo especificado."""
    procesos = ctx.obj["repositorio"].listar()
    if not procesos:
        click.echo("No hay procesos para planificar.")
        return
    try:
        if algoritmo == "fcfs":
            scheduler = FCFSScheduler()
        else:
            scheduler = RoundRobinScheduler(quantum=quantum)
        gantt = scheduler.planificar(procesos)
        click.echo("Diagrama de Gantt:")
        for entry in gantt:
            click.echo(f"  {entry[0]}: {entry[1]} -> {entry[2]}")
        # Almacenar Gantt para métricas
        ctx.obj["gantt"] = gantt
    except ValueError as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.pass_context
def metrics(ctx):
    """Muestra las métricas de los procesos planificados."""
    procesos = ctx.obj["repositorio"].listar()
    gantt = ctx.obj.get("gantt")
    if not procesos or not gantt:
        click.echo("Primero debes planificar los procesos con 'plan'.")
        return
    try:
        metrics = Metrics(procesos, gantt)
        click.echo(metrics)
    except ValueError as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("formato", type=click.Choice(["json", "csv"]))
@click.argument("archivo")
@click.pass_context
def save(ctx, formato, archivo):
    """Guarda los procesos en un archivo."""
    try:
        if formato == "json":
            ctx.obj["repositorio"].guardar_json(archivo)
        else:
            ctx.obj["repositorio"].guardar_csv(archivo)
        click.echo(f"Procesos guardados en {archivo} ({formato}).")
    except (ValueError, IOError) as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("formato", type=click.Choice(["json", "csv"]))
@click.argument("archivo")
@click.pass_context
def load(ctx, formato, archivo):
    """Carga procesos desde un archivo."""
    try:
        if formato == "json":
            ctx.obj["repositorio"].cargar_json(archivo)
        else:
            ctx.obj["repositorio"].cargar_csv(archivo)
        click.echo(f"Procesos cargados desde {archivo} ({formato}).")
    except (ValueError, IOError) as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    cli()