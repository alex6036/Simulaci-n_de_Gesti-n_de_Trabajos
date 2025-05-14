from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
from src.scheduler import FCFSScheduler, RoundRobinScheduler
import gradio as gr

# Instancia global del repositorio
repositorio = RepositorioProcesos()

# ---------- Funciones de la interfaz ----------

def agregar_proceso(pid: str, duracion: int, prioridad: int):
    try:
        proceso = Proceso(pid, duracion, prioridad)
        repositorio.agregar(proceso)
        return f"✅ Proceso '{pid}' agregado correctamente", listar_procesos()
    except Exception as e:
        return f"❌ Error: {str(e)}", listar_procesos()

def listar_procesos():
    procesos = repositorio.listar()
    return [
        [p.pid, p.duracion, p.prioridad, p.tiempo_restante]
        for p in procesos
    ]

def planificar_fcfs():
    procesos = repositorio.listar()
    if not procesos:
        return [["(sin procesos)", 0, 0]]
    planificador = FCFSScheduler()
    gantt = planificador.planificar(procesos)
    return gantt

def planificar_rr(quantum: int):
    procesos = repositorio.listar()
    if not procesos:
        return [["(sin procesos)", 0, 0]]
    planificador = RoundRobinScheduler(quantum)
    gantt = planificador.planificar(procesos)
    return gantt

# ---------- Interfaz Gradio ----------

with gr.Blocks(title="Planificador de Procesos") as demo:
    gr.Markdown("# ⚙️ Simulador de Planificación de Procesos")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ➕ Agregar Proceso")
            pid = gr.Text(label="PID")
            duracion = gr.Number(label="Duración", precision=0)
            prioridad = gr.Number(label="Prioridad", precision=0)
            agregar_btn = gr.Button("Agregar")
            estado = gr.Textbox(label="Estado")

        with gr.Column():
            gr.Markdown("### 📋 Procesos Actuales")
            tabla_procesos = gr.Dataframe(headers=["PID", "Duración", "Prioridad", "Tiempo Restante"], interactive=False)

    agregar_btn.click(fn=agregar_proceso, inputs=[pid, duracion, prioridad], outputs=[estado, tabla_procesos])

    with gr.Row():
        gr.Markdown("## 📊 Planificación")

    with gr.Row():
        btn_fcfs = gr.Button("Planificar FCFS")
        btn_rr = gr.Button("Planificar Round-Robin")
        quantum = gr.Number(label="Quantum RR", value=2, precision=0)

    tabla_gantt = gr.Dataframe(headers=["PID", "Inicio", "Fin"], interactive=False)

    btn_fcfs.click(fn=planificar_fcfs, inputs=[], outputs=tabla_gantt)
    btn_rr.click(fn=planificar_rr, inputs=[quantum], outputs=tabla_gantt)

if __name__ == "__main__":
    demo.launch()
