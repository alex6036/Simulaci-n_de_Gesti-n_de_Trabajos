import unittest
from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler, GanttEntry

class TestScheduler(unittest.TestCase):
    def setUp(self):
        # Limpiar PIDs usados antes de cada prueba
        Proceso._pids_usados.clear()
        # Crear procesos de prueba
        self.procesos = [
            Proceso("P1", 5, 1),
            Proceso("P2", 3, 2),
            Proceso("P3", 2, 1)
        ]

    def test_fcfs_scheduler(self):
        scheduler = FCFSScheduler()
        gantt = scheduler.planificar(self.procesos)
        esperado = [
            ("P1", 0, 5),   # P1: 0-5
            ("P2", 5, 8),   # P2: 5-8
            ("P3", 8, 10)   # P3: 8-10
        ]
        self.assertEqual(gantt, esperado)
        # Verificar tiempos finales
        self.assertEqual(self.procesos[0].tiempo_fin, 5)
        self.assertEqual(self.procesos[1].tiempo_fin, 8)
        self.assertEqual(self.procesos[2].tiempo_fin, 10)
        # Verificar tiempos restantes
        self.assertEqual(self.procesos[0].tiempo_restante, 0)
        self.assertEqual(self.procesos[1].tiempo_restante, 0)
        self.assertEqual(self.procesos[2].tiempo_restante, 0)

    def test_round_robin_scheduler_quantum_2(self):
        scheduler = RoundRobinScheduler(quantum=2)
        gantt = scheduler.planificar(self.procesos)
        esperado = [
            ("P1", 0, 2),   # P1: 0-2 (resta 2, queda 3)
            ("P2", 2, 4),   # P2: 2-4 (resta 2, queda 1)
            ("P3", 4, 6),   # P3: 4-6 (resta 2, queda 0)
            ("P1", 6, 8),   # P1: 6-8 (resta 2, queda 1)
            ("P2", 8, 9),   # P2: 8-9 (resta 1, queda 0)
            ("P1", 9, 10)   # P1: 9-10 (resta 1, queda 0)
        ]
        self.assertEqual(gantt, esperado)
        # Verificar tiempos finales
        self.assertEqual(self.procesos[0].tiempo_fin, 10)
        self.assertEqual(self.procesos[1].tiempo_fin, 9)
        self.assertEqual(self.procesos[2].tiempo_fin, 6)
        # Verificar tiempos restantes
        self.assertEqual(self.procesos[0].tiempo_restante, 0)
        self.assertEqual(self.procesos[1].tiempo_restante, 0)
        self.assertEqual(self.procesos[2].tiempo_restante, 0)

    def test_invalid_procesos(self):
        fcfs = FCFSScheduler()
        rr = RoundRobinScheduler(quantum=2)
        with self.assertRaises(ValueError):
            fcfs.planificar([])
        with self.assertRaises(ValueError):
            rr.planificar([])
        with self.assertRaises(ValueError):
            fcfs.planificar([None])
        with self.assertRaises(ValueError):
            rr.planificar([None])

    def test_invalid_quantum(self):
        with self.assertRaises(ValueError):
            RoundRobinScheduler(quantum=0)
        with self.assertRaises(ValueError):
            RoundRobinScheduler(quantum=-1)

if __name__ == "__main__":
    unittest.main()