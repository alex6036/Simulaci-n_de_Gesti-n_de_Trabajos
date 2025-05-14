import unittest
from src.proceso import Proceso

class TestProceso(unittest.TestCase):
    def tearDown(self):
        # Limpiar los PIDs usados después de cada prueba
        Proceso._pids_usados.clear()

    def test_crear_proceso_valido(self):
        proceso = Proceso("P1", 10, 1)
        self.assertEqual(proceso.pid, "P1")
        self.assertEqual(proceso.duracion, 10)
        self.assertEqual(proceso.prioridad, 1)
        self.assertEqual(proceso.tiempo_restante, 10)
        self.assertEqual(proceso.tiempo_llegada, 0)
        self.assertIsNone(proceso.tiempo_inicio)
        self.assertIsNone(proceso.tiempo_fin)

    def test_pid_duplicado(self):
        Proceso("P1", 10, 1)
        with self.assertRaises(ValueError):
            Proceso("P1", 5, 2)

    def test_pid_invalido(self):
        with self.assertRaises(ValueError):
            Proceso("", 10, 1)
        with self.assertRaises(ValueError):
            Proceso(None, 10, 1)

    def test_duracion_invalida(self):
        with self.assertRaises(ValueError):
            Proceso("P1", 0, 1)
        with self.assertRaises(ValueError):
            Proceso("P1", -5, 1)

    def test_prioridad_invalida(self):
        with self.assertRaises(ValueError):
            Proceso("P1", 10, -1)

    def test_reducir_tiempo_restante(self):
        proceso = Proceso("P1", 10, 1)
        procedimiento.reducir_tiempo_restante(3)
        self.assertEqual(proceso.tiempo_restante, 7)
        with self.assertRaises(ValueError):
            proceso.reducir_tiempo_restante(8)  # Excede tiempo restante
        with self.assertRaises(ValueError):
            proceso.reducir_tiempo_restante(0)  # Tiempo inválido

    def test_establecer_tiempos(self):
        proceso = Proceso("P1", 10, 1)
        proceso.establecer_tiempo_inicio(5)
        self.assertEqual(proceso.tiempo_inicio, 5)
        with self.assertRaises(ValueError):
            proceso.establecer_tiempo_inicio(10)  # Ya establecido
        proceso.establecer_tiempo_fin(15)
        self.assertEqual(proceso.tiempo_fin, 15)
        with self.assertRaises(ValueError):
            proceso.establecer_tiempo_fin(20)  # Ya establecido

if __name__ == "__main__":
    unittest.main()