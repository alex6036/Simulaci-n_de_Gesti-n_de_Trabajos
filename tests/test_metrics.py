import unittest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler
from src.metrics import Metrics

class TestMetrics(unittest.TestCase):
    def setUp(self):
        # Limpiar PIDs usados antes de cada prueba
        Proceso._pids_usados.clear()
        # Crear procesos de prueba
        self.procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2),
            Proceso("P3", 2, 1)
        ]

    def test_metrics_fcfs(self):
        scheduler = FCFSScheduler()
        gantt = scheduler.planificar(self.procesos)
        metrics = Metrics(self.procesos, gantt)

        # Métricas esperadas por proceso
        # P1: inicio=0, fin=5, duración=5, llegada=0
        #   Respuesta = 0 - 0 = 0
        #   Retorno = 5 - 0 = 5
        #   Espera = 5 - 5 = 0
        # P2: inicio=5, fin=8, duración=3, llegada=0
        #   Respuesta = 5 - 0 = 5
        #   Retorno = 8 - 0 = 8
        #   Espera = 8 - 3 = 5
        # P3: inicio=8, fin=10, duración=2, llegada=0
        #   Respuesta = 8 - 0 = 8
        #   Retorno = 10 - 0 = 10
        #   Espera = 10 - 2 = 8
        metricas_por_proceso = metrics.obtener_metricas_por_proceso()
        self.assertEqual(metricas_por_proceso["P1"], {"tiempo_respuesta": 0, "tiempo_retorno": 5, "tiempo_espera": 0})
        self.assertEqual(metricas_por_proceso["P2"], {"tiempo_respuesta": 5, "tiempo_retorno": 8, "tiempo_espera": 5})
        self.assertEqual(metricas_por_proceso["P3"], {"tiempo_respuesta": 8, "tiempo_retorno": 10, "tiempo_espera": 8})

        # Métricas promedio
        # Respuesta = (0 + 5 + 8) / 3 = 4.333
        # Retorno = (5 + 8 + 10) / 3 = 7.667
        # Espera = (0 + 5 + 8) / 3 = 4.333
        metricas_promedio = metrics.obtener_metricas_promedio()
        self.assertAlmostEqual(metricas_promedio["promedio_respuesta"], 4.333, places=3)
        self.assertAlmostEqual(metricas_promedio["promedio_retorno"], 7.667, places=3)
        self.assertAlmostEqual(metricas_promedio["promedio_espera"], 4.333, places=3)

    def test_metrics_round_robin(self):
        scheduler = RoundRobinScheduler(quantum=2)
        gantt = scheduler.planificar(self.procesos)
        metrics = Metrics(self.procesos, gantt)

        # Métricas esperadas por proceso
        # Gantt: P1(0-2), P2(2-4), P3(4-6), P1(6-8), P2(8-9), P1(9-10)
        # P1: inicio=0, fin=10, duración=5, llegada=0
        #   Respuesta = 0 - 0 = 0
        #   Retorno = 10 - 0 = 10
        #   Espera = 10 - 5 = 5
        # P2: inicio=2, fin=9, duración=3, llegada=0
        #   Respuesta = 2 - 0 = 2
        #   Retorno = 9 - 0 = 9
        #   Espera = 9 - 3 = 6
        # P3: inicio=4, fin=6, duración=2, llegada=0
        #   Respuesta = 4 - 0 = 4
        #   Retorno = 6 - 0 = 6
        #   Espera = 6 - 2 = 4
        metricas_por_proceso = metrics.obtener_metricas_por_proceso()
        self.assertEqual(metricas_por_proceso["P1"], {"tiempo_respuesta": 0, "tiempo_retorno": 10, "tiempo_espera": 5})
        self.assertEqual(metricas_por_proceso["P2"], {"tiempo_respuesta": 2, "tiempo_retorno": 9, "tiempo_espera": 6})
        self.assertEqual(metricas_por_proceso["P3"], {"tiempo_respuesta": 4, "tiempo_retorno": 6, "tiempo_espera": 4})

        # Métricas promedio
        # Respuesta = (0 + 2 + 4) / 3 = 2.0
        # Retorno = (10 + 9 + 6) / 3 = 8.333
        # Espera = (5 + 6 + 4) / 3 = 5.0
        metricas_promedio = metrics.obtener_metricas_promedio()
        self.assertAlmostEqual(metricas_promedio["promedio_respuesta"], 2.0, places=3)
        self.assertAlmostEqual(metricas_promedio["promedio_retorno"], 8.333, places=3)
        self.assertAlmostEqual(metricas_promedio["promedio_espera"], 5.0, places=3)

    def test_invalid_input(self):
        scheduler = FCFSScheduler()
        gantt = scheduler.planificar(self.procesos)
        # Lista vacía
        with self.assertRaises(ValueError):
            Metrics([], gantt)
        # Proceso sin tiempos definidos
        proceso_no_planificado = Proceso("P4", 4, 1)
        with self.assertRaises(ValueError):
            Metrics([proceso_no_planificado], gantt)
        # Gantt inválido
        with self.assertRaises(ValueError):
            Metrics(self.procesos, [])
        with self.assertRaises(ValueError):
            Metrics(self.procesos, [("P1", 0)])  # Tupla incompleta

if __name__ == "__main__":
    unittest.main()