from __future__ import annotations
from typing import TypeVar, Generic, Dict, Set, Optional, Callable, Tuple, List, Any
from abc import ABC, abstractmethod
from datetime import date, datetime
import matplotlib.pyplot as plt
import networkx as nx

# Definición de tipos genéricos
V = TypeVar('V')  # Tipo para vértices
E = TypeVar('E')  # Tipo para aristas

class Grafo(Generic[V, E]):
    """
    Representación de un grafo utilizando un diccionario de adyacencia.
    """
    def __init__(self, es_dirigido: bool = True):
        self.es_dirigido: bool = es_dirigido
        self.adyacencias: Dict[V, Dict[V, E]] = {}  # Diccionario de adyacencia
    
    @staticmethod
    def of(es_dirigido: bool = True) -> Grafo[V, E]:
        """
        Método de factoría para crear un nuevo grafo.
        """
        return Grafo(es_dirigido)
    
    def add_vertex(self, vertice: V) -> None:
        """
        Añade un vértice al grafo si no existe.
        """
        if vertice not in self.adyacencias:
            self.adyacencias[vertice] = {}
    
    def add_edge(self, origen: V, destino: V, arista: E) -> None:
        """
        Añade una arista al grafo entre dos vértices.
        """
        self.add_vertex(origen)
        self.add_vertex(destino)
        self.adyacencias[origen][destino] = arista
        if not self.es_dirigido:
            self.adyacencias[destino][origen] = arista

    def successors(self, vertice: V) -> Set[V]:
        """
        Devuelve los sucesores de un vértice.
        """
        return set(self.adyacencias.get(vertice, {}).keys())

    def predecessors(self, vertice: V) -> Set[V]:
        """
        Devuelve los predecesores de un vértice.
        """
        if not self.es_dirigido:
            return self.successors(vertice)
        return {origen for origen, destinos in self.adyacencias.items() if vertice in destinos}

    def edge_weight(self, origen: V, destino: V) -> Optional[E]:
        """
        Devuelve el peso de la arista entre dos vértices.
        """
        return self.adyacencias.get(origen, {}).get(destino)

    def vertices(self) -> Set[V]:
        """
        Devuelve el conjunto de vértices del grafo.
        """
        return set(self.adyacencias.keys())

    def edge_exists(self, origen: V, destino: V) -> bool:
        """
        Verifica si existe una arista entre dos vértices.
        """
        return destino in self.adyacencias.get(origen, {})

    def subgraph(self, vertices: Set[V]) -> Grafo[V, E]:
        """
        Crea un subgrafo basado en un conjunto de vértices.
        """
        subgrafo = Grafo(self.es_dirigido)
        for vertice in vertices:
            if vertice in self.adyacencias:
                for destino, arista in self.adyacencias[vertice].items():
                    if destino in vertices:
                        subgrafo.add_edge(vertice, destino, arista)
        return subgrafo

    def inverse_graph(self) -> Grafo[V, E]:
        """
        Devuelve el grafo inverso.
        """
        if not self.es_dirigido:
            raise ValueError("El grafo no es dirigido.")
        grafo_inverso = Grafo(self.es_dirigido)
        for origen in self.adyacencias:
            for destino, arista in self.adyacencias[origen].items():
                grafo_inverso.add_edge(destino, origen, arista)
        return grafo_inverso

    def draw(self, titulo: str = "Grafo", 
            lambda_vertice: Callable[[V], str] = str, 
            lambda_arista: Callable[[E], str] = str) -> None:
        """
        Dibuja el grafo utilizando NetworkX y Matplotlib.
        """
        G = nx.DiGraph() if self.es_dirigido else nx.Graph()
    
        for vertice in self.vertices():
            G.add_node(vertice, label=lambda_vertice(vertice))
        for origen in self.adyacencias:
            for destino, arista in self.adyacencias[origen].items():
                G.add_edge(origen, destino, label=lambda_arista(arista))
    
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=500, 
                labels=nx.get_node_attributes(G, 'label'))
        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title(titulo)
        plt.show()

    def __str__(self) -> str:
        """
        Representación textual del grafo.
        """
        result = []
        for origen, destinos in self.adyacencias.items():
            conexiones = ", ".join(f"{destino} ({peso})" for destino, peso in destinos.items())
            result.append(f"{origen} -> {conexiones}")
        return "\n".join(result)

if __name__ == '__main__':
    # Crear un grafo dirigido
    grafo = Grafo.of(es_dirigido=True)
    grafo.add_vertex("A")
    grafo.add_vertex("B")
    grafo.add_vertex("C")
    grafo.add_edge("A", "B", 5)
    grafo.add_edge("B", "C", 3)
    grafo.inverse_graph().draw(titulo="Inverso del Grafo Dirigido")
    
class Recorrido(ABC, Generic[V, E]):
    """
    Representa una estrategia general para recorrer un grafo.
    """
    def __init__(self, grafo: Grafo[V, E]):
        self._tree: Dict[V, Tuple[Optional[V], float]] = {}  # Árbol de recorridos
        self._path: List[V] = []  # Camino recorrido
        self._grafo: Grafo[V, E] = grafo  # Grafo sobre el que se realiza el recorrido

    @abstractmethod
    def recorrer(self, origen: V) -> None:
        """
        Método abstracto para realizar el recorrido desde un nodo de origen.
        """
        pass

    def path_to_origin(self, source: V) -> List[V]:
        """
        Construye el camino hacia el origen a partir de un vértice dado.
        """
        path = []
        actual = source
        while actual is not None:
            path.append(actual)
            actual = self._tree.get(actual, (None, 0))[0]  # Obtener predecesor
        return path[::-1]  # Invertir para obtener desde el origen al destino

    def origin(self, vertice: V) -> Optional[V]:
        """
        Determina el origen de un recorrido a partir de un vértice dado.
        """
        actual = vertice
        while actual in self._tree and self._tree[actual][0] is not None:
            actual = self._tree[actual][0]
        return actual

    def groups(self) -> Dict[V, Set[V]]:
        """
        Organiza los vértices del grafo en grupos basados en su origen.
        """
        grupos: Dict[V, Set[V]] = {}
        for vertice in self._tree:
            origen = self.origin(vertice)
            if origen not in grupos:
                grupos[origen] = set()
            grupos[origen].add(vertice)
        return grupos

    def get_tree(self) -> Dict[V, Tuple[Optional[V], float]]:
        """
        Devuelve el árbol de recorridos.
        """
        return self._tree

    def get_path(self) -> List[V]:
        """
        Devuelve el camino recorrido.
        """
        return self._path
    
    from typing import Set, Dict, List, Optional

class RecorridoProfundidad(Recorrido[V, E]):
    """
    Implementa el algoritmo de búsqueda en profundidad (DFS) para recorrer un grafo.
    """
    @staticmethod
    def of(grafo: Grafo[V, E]) -> RecorridoProfundidad[V, E]:
        """
        Método de factoría para crear una nueva instancia de RecorridoProfundidad.
        """
        return RecorridoProfundidad(grafo)

    def traverse(self, source: V) -> None:
        """
        Realiza un recorrido en profundidad (DFS) desde el vértice source.
        """
        self._tree = {}
        self._path = []
        visitados: Set[V] = set()
        pila: List[V] = [source]

        # Inicializar el árbol con el nodo de origen
        self._tree[source] = (None, 0)  # El origen no tiene predecesor y su costo es 0

        while pila:
            vertice = pila.pop()  # Tomar el último elemento de la pila (LIFO)
            if vertice not in visitados:
                visitados.add(vertice)  # Marcar como visitado
                self._path.append(vertice)  # Registrar en el camino

                for vecino in reversed(list(self._grafo.successors(vertice))):  # Orden inverso para respetar DFS
                    if vecino not in visitados:
                        pila.append(vecino)  # Agregar vecino a la pila
                        # Registrar predecesor y calcular el costo acumulado
                        costo_previo = self._tree[vertice][1]
                        peso_arista = self._grafo.edge_weight(vertice, vecino) or 1  # Peso predeterminado si no está definido
                        self._tree[vecino] = (vertice, costo_previo + peso_arista)

    def __str__(self) -> str:
        """
        Representación textual del recorrido en profundidad.
        """
        return f"Camino recorrido: {self._path}\nÁrbol de recorridos: {self._tree}"

from datetime import date, datetime
from typing import Any


class Usuario:
    """
    Representa un usuario en el sistema con atributos como DNI, nombre, apellidos y fecha de nacimiento.
    """
    def __init__(self, dni: str, nombre: str, apellidos: str, fecha_nacimiento: date):
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento

    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, value: str) -> None:
        """
        Valida el formato del DNI: 8 dígitos seguidos de una letra.
        """
        if not isinstance(value, str) or not value[:-1].isdigit() or not value[-1].isalpha() or len(value) != 9:
            raise ValueError("El DNI debe tener 8 dígitos seguidos de una letra, por ejemplo: '12345678A'.")
        self._dni = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        """
        Valida que el nombre no sea una cadena vacía.
        """
        if not value or not isinstance(value, str):
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = value

    @property
    def apellidos(self) -> str:
        return self._apellidos

    @apellidos.setter
    def apellidos(self, value: str) -> None:
        """
        Valida que los apellidos no sean una cadena vacía.
        """
        if not value or not isinstance(value, str):
            raise ValueError("Los apellidos no pueden estar vacíos.")
        self._apellidos = value

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value: date) -> None:
        """
        Valida que la fecha de nacimiento sea anterior a la fecha actual.
        """
        if not isinstance(value, date):
            raise ValueError("La fecha de nacimiento debe ser una instancia de datetime.date.")
        if value >= date.today():
            raise ValueError("La fecha de nacimiento debe ser anterior a la fecha actual.")
        self._fecha_nacimiento = value

    @staticmethod
    def of(dni: str, nombre: str, apellidos: str, fecha_nacimiento: date) -> Usuario:
        """
        Método de factoría para crear un nuevo usuario.
        """
        return Usuario(dni, nombre, apellidos, fecha_nacimiento)

    @classmethod
    def parse(cls, cadena: str) -> "Usuario":
        dni, nombre, apellidos, fecha_nacimiento = cadena.split(",")
        # Asegurarse de que la fecha sea un objeto `date` y que el DNI esté bien formateado
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        return cls(dni=dni, nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento)

    def __str__(self) -> str:
        """
        Representación como cadena: 'dni - nombre'.
        """
        return f"{self.dni} - {self.nombre}"


class Relacion:
    xx_num = 0  # Contador estático que incrementa para generar un ID único

    def __init__(self, interacciones: int, dias_activa: int):
        Relacion.xx_num += 1  # Incrementa el contador estático
        self.id = Relacion.xx_num  # Asigna un ID único
        self.interacciones = interacciones
        self.dias_activa = dias_activa

    @staticmethod
    def of(interacciones: int, dias_activa: int) -> Relacion:
        return Relacion(interacciones, dias_activa)

    def __str__(self) -> str:
        return f"({self.id} - días activa: {self.dias_activa} - num interacciones {self.interacciones})"


class Red_social(Grafo[Usuario, Relacion]):
    def __init__(self, es_dirigido: bool = False, tipo_recorrido: str = "BACK") -> None:
        super().__init__(es_dirigido)
        self.usuarios_dni: Dict[str, Usuario] = {}  # Diccionario de usuarios indexados por su DNI

    @staticmethod
    def of(es_dirigido: bool = False, tipo_recorrido: str = "BACK") -> Red_social:
        return Red_social(es_dirigido, tipo_recorrido)
    
    @staticmethod
    def parse(usuarios_file: str, relaciones_file: str) -> Red_social:
        red_social = Red_social()
        
        # Leer usuarios
        with open(usuarios_file, 'r') as f:
            for line in f:
                dni, nombre, apellidos, fecha_nacimiento = line.strip().split(',')
                usuario = Usuario.parse(dni, nombre, apellidos, fecha_nacimiento)
                red_social.add_vertex(usuario)  # Añadir el usuario al grafo
        
        # Leer relaciones
        with open(relaciones_file, 'r') as f:
            for line in f:
                dni_origen, dni_destino, interacciones, dias_activa = line.strip().split(',')
                origen = red_social.usuarios_dni[dni_origen]
                destino = red_social.usuarios_dni[dni_destino]
                relacion = Relacion.of(int(interacciones), int(dias_activa))
                red_social.add_edge(origen, destino, relacion)  # Añadir la relación al grafo
        
        return red_social

    def add_vertex(self, usuario: Usuario) -> None:
        super().add_vertex(usuario)
        self.usuarios_dni[usuario.dni] = usuario

    def add_edge(self, origen: Usuario, destino: Usuario, relacion: Relacion) -> None:
        super().add_edge(origen, destino, relacion)

    def __str__(self) -> str:
        resultado = []
        for usuario in self.vertices():
            relaciones = ", ".join([f"{relacion}" for _, relacion in self.adyacencias[usuario].items()])
            resultado.append(f"{usuario} -> {relaciones}")
        return "\n".join(resultado)
