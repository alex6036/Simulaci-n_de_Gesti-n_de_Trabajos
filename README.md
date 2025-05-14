# Simulación_de_Gesti-n_de_Trabajos
https://github.com/alex6036/Simulaci-n_de_Gesti-n_de_Trabajos.git

para poder utilizar el main tiene que utilizar el comando:
python -m src.main


# 🧠 Simulador de Planificación de Procesos

Este proyecto simula un sistema operativo simplificado que gestiona procesos y los planifica utilizando algoritmos como **First-Come, First-Served (FCFS)** y **Round-Robin (RR)**. Incluye una interfaz gráfica interactiva desarrollada con [Gradio](https://www.gradio.app/).

## 🚀 Características

- Gestión de procesos personalizados (PID, duración, prioridad).
- Algoritmos de planificación:
  - FCFS (First-Come, First-Served)
  - Round-Robin (con quantum configurable)
- Persistencia de procesos en archivos JSON y CSV.
- Interfaz gráfica amigable con Gradio.
- Código estructurado con orientación a objetos.
- Pruebas unitarias (en desarrollo).

## 📂 Estructura del Proyecto

├── src/
│ ├── main.py # Interfaz gráfica principal
│ ├── proceso.py # Clase Proceso
│ ├── repositorio.py # Repositorio de procesos (con persistencia)
│ └── scheduler.py # Planificadores FCFS y Round-Robin
│
├── tests/
│ └── test_proceso.py # Pruebas unitarias (opcional)
│
├── requirements.txt # Dependencias
└── README.md # Este archivo