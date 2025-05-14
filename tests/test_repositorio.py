import unittest
import os
import json
import csv
from src.proceso import Proceso
from src.repositorio import RepositorioProcesos

class TestRepositorioProcesos(unittest.TestCase):
    def setUp(self):
        # Limpiar PIDs usados antes de cada prueba
        Proceso._pids_usados.clear()
        self.repositorio = RepositorioProcesos()
        self.proceso1 = Proceso("P1", 5, 1)
        self.proceso2 = Proceso("P2", 3, 2)

    def test_agregar_proceso(self):
        self.repositorio.agregar(self.proceso1)
        self.assertEqual(len(self.repositorio.listar()), 1)
        self.assertEqual(self.repositorio.obtener("P1"), self.proceso1)
        with self.assertRaises(ValueError):
            self.repositorio.agregar(self.proceso1)  # PID duplicado
        with self.assertRaises(ValueError):
            self.repositorio.agregar(None)  # Argumento inválido

    def test_listar_procesos(self):
        self.repositorio.agregar(self.proceso1)
        self.repositorio.agregar(self.proceso2)
        procesos = self.repositorio.listar()
        self.assertEqual(len(procesos), 2)
        self.assertIn(self.proceso1, procesos)
        self.assertIn(self.proceso2, procesos)

    def test_eliminar_proceso(self):
        self.repositorio.agregar(self.proceso1)
        self.repositorio.eliminar("P1")
        self.assertEqual(len(self.repositorio.listar()), 0)
        self.assertIsNone(self.repositorio.obtener("P1"))
        with self.assertRaises(ValueError):
            self.repositorio.eliminar("P1")  # PID no existe

    def test_obtener_proceso(self):
        self.repositorio.agregar(self.proceso1)
        self.assertEqual(self.repositorio.obtener("P1"), self.proceso1)
        self.assertIsNone(self.repositorio.obtener("P2"))

    def test_guardar_cargar_json(self):
        self.repositorio.agregar(self.proceso1)
        self.repositorio.agregar(self.proceso2)
        archivo = "test_procesos.json"
        self.repositorio.guardar_json(archivo)
        
        # Crear un nuevo repositorio y cargar
        nuevo_repositorio = RepositorioProcesos()
        nuevo_repositorio.cargar_json(archivo)
        procesos = nuevo_repositorio.listar()
        self.assertEqual(len(procesos), 2)
        p1 = nuevo_repositorio.obtener("P1")
        self.assertEqual(p1.duracion, 5)
        self.assertEqual(p1.prioridad, 1)
        
        # Limpiar archivo
        os.remove(archivo)

    def test_guardar_cargar_csv(self):
        self.repositorio.agregar(self.proceso1)
        self.repositorio.agregar(self.proceso2)
        archivo = "test_procesos.csv"
        self.repositorio.guardar_csv(archivo)
        
        # Crear un nuevo repositorio y cargar
        nuevo_repositorio = RepositorioProcesos()
        nuevo_repositorio.cargar_csv(archivo)
        procesos = nuevo_repositorio.listar()
        self.assertEqual(len(procesos), 2)
        p1 = nuevo_repositorio.obtener("P1")
        self.assertEqual(p1.duracion, 5)
        self.assertEqual(p1.prioridad, 1)
        
        # Limpiar archivo
        os.remove(archivo)

    def test_cargar_json_invalido(self):
        archivo = "test_invalido.json"
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("invalid json")
        with self.assertRaises(ValueError):
            self.repositorio.cargar_json(archivo)
        os.remove(archivo)

    def test_cargar_csv_invalido(self):
        archivo = "test_invalido.csv"
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("pid;duracion\nP1;5")  # Encabezado incompleto
        with self.assertRaises(ValueError):
            self.repositorio.cargar_csv(archivo)
        os.remove(archivo)

if __name__ == "__main__":
    unittest.main()