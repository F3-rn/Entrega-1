import csv
from entrega3.ENTREGA3 import Grafo
from typing import Set, Dict
import networkx as nx
import matplotlib.pyplot as plt

#EJERCICIO 1
class Gen:
    def __init__(self, nombre, tipo, num_mutaciones, loc_cromosoma):
        if num_mutaciones < 0:
            raise ValueError("El número de mutaciones debe ser mayor o igual que cero")
        
        self._nombre = nombre
        self._tipo = tipo
        self._num_mutaciones = num_mutaciones
        self._loc_cromosoma = loc_cromosoma

    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

    @property
    def num_mutaciones(self):
        return self._num_mutaciones

    @property
    def loc_cromosoma(self):
        return self._loc_cromosoma

    @staticmethod
    def of(nombre, tipo, num_mutaciones, loc_cromosoma):
        if not isinstance(num_mutaciones, int) or num_mutaciones < 0:
            raise ValueError("num_mutaciones debe ser un entero mayor o igual a 0")
        return Gen(nombre, tipo, num_mutaciones, loc_cromosoma)

    @staticmethod
    def parse(file_path):
        genes = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    raise ValueError(f"La línea no tiene el formato correcto: {line.strip()}")
                
                nombre, tipo, num_mutaciones_str, loc_cromosoma = parts
                try:
                    num_mutaciones = int(num_mutaciones_str)
                except ValueError:
                    raise ValueError(f"El valor de num_mutaciones ('{num_mutaciones_str}') no es un entero válido")
                
                genes.append(Gen.of(nombre, tipo, num_mutaciones, loc_cromosoma))
        
        return genes

    def __repr__(self):
        return f"Gen(nombre='{self.nombre}', tipo='{self.tipo}', num_mutaciones={self.num_mutaciones}, loc_cromosoma='{self.loc_cromosoma}')"

#EJERCICIO 2
class RelacionGenAGen:
    def __init__(self, nombre_gen1: str, nombre_gen2: str, conexion: float):
        if not (-1 <= conexion <= 1):
            raise ValueError("La conexión debe estar entre -1 y 1.")
        self._nombre_gen1 = nombre_gen1
        self._nombre_gen2 = nombre_gen2
        self._conexion = conexion
    
    @property
    def nombre_gen1(self):
        return self._nombre_gen1
    
    @property
    def nombre_gen2(self):
        return self._nombre_gen2
    
    @property
    def conexion(self):
        return self._conexion
    
    @property
    def coexpresados(self):
        return self._conexion > 0.7
    
    @property
    def antiexpresados(self):
        return self._conexion < 0.7

    @staticmethod
    def of(nombre_gen1: str, nombre_gen2: str, conexion: float):
        return RelacionGenAGen(nombre_gen1, nombre_gen2, conexion)
    
    @staticmethod
    def parse(fichero: str):
        relaciones = []
        with open(fichero, 'r') as file:
            lector = csv.reader(file)
            for fila in lector:
                if len(fila) == 3:
                    nombre_gen1, nombre_gen2, conexion = fila
                    try:
                        conexion = float(conexion)
                        relaciones.append(RelacionGenAGen.of(nombre_gen1, nombre_gen2, conexion))
                    except ValueError:
                        print(f"Error al convertir la conexión en la línea: {fila}")
        return relaciones

#EJERCICIO 3
class RedGenica(Grafo[Gen, RelacionGenAGen]):
    def __init__(self, es_dirigido: bool = False) -> None:
        super().__init__(es_dirigido)
        self.genes_por_nombre: Dict[str, Gen] = {}

    @staticmethod
    def of(es_dirigido: bool = False):
        return RedGenica(es_dirigido)

    @staticmethod
    def parse(f1: str, f2: str, es_dirigido: bool = False):
        red_genica = RedGenica(es_dirigido)

        genes = Gen.parse(f1)
        for gen in genes:
            red_genica.genes_por_nombre[gen.nombre] = gen
            red_genica.add_vertex(gen)

        with open(f2, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    raise ValueError(f"La línea no tiene el formato correcto: {line.strip()}")
                
                nombre_gen1, nombre_gen2, conexion_str = parts
                try:
                    conexion = float(conexion_str)
                except ValueError:
                    raise ValueError(f"El valor de conexión ('{conexion_str}') no es un número válido")

                gen1 = red_genica.genes_por_nombre.get(nombre_gen1)
                gen2 = red_genica.genes_por_nombre.get(nombre_gen2)

                if gen1 and gen2:
                    relacion = RelacionGenAGen.of(nombre_gen1, nombre_gen2, conexion)
                    red_genica.add_edge(gen1, gen2, relacion)

        return red_genica

    def __repr__(self):
        return f"RedGenica(es_dirigido={self.es_dirigido}, genes={list(self.genes_por_nombre.values())}, adyacencias={self.adyacencias})"


#TESTS

def test_parse1():
    try:
        genes = Gen.parse("genes.csv")
        for gen in genes:
            print(gen)

    except FileNotFoundError as e:
        print(f"Error: {e}")

def test_parse2():
    relaciones = RelacionGenAGen.parse('red_genes.csv')
    for rel in relaciones:
        print(f"{rel.nombre_gen1} - {rel.nombre_gen2}: conexión = {rel.conexion}")
        print(f"Coexpresados: {rel.coexpresados}")
        print(f"Antiexpresados: {rel.antiexpresados}")
        print(" ")

if __name__ == "__main__":
    test_parse1()
    print(" ")
    test_parse2()
    
red_genica = RedGenica.parse("genes.csv", "red_genes.csv", es_dirigido=False)
kras = red_genica.genes_por_nombre.get("KRAS")
pik3ca = red_genica.genes_por_nombre.get("PIK3CA")

def dfs(graph, start, goal, path=None):
    if path is None:
        path = []
    path.append(start)

    if start == goal:
        return path
    
    for neighbor in graph.successors(start):
        if neighbor not in path:
            new_path = dfs(graph, neighbor, goal, path)
            if new_path:
                return new_path
    return None
    dfs_path = dfs(red_genica, kras, pik3ca)
    print(f"Recorrido DFS desde KRAS hasta PIK3CA: {dfs_path}")

    