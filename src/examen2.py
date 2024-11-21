from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Callable, Optional
E = TypeVar('E')

#AGREGADO LINEAL
class AgregadoLineal(ABC, Generic[E]):
    def __init__(self):
        self._elements: List[E] = []

    @property
    def size(self) -> int:
        return len(self._elements)

    @property
    def is_empty(self) -> bool:
        return len(self._elements) == 0

    @property
    def elements(self) -> List[E]:
        return self._elements

    @abstractmethod
    def add(self, e: E) -> None:
        pass

    def add_all(self, ls: List[E]) -> None:
        for element in ls:
            self.add(element)

    def remove(self) -> E:
        assert len(self._elements) > 0, 'El agregado está vacío'
        return self._elements.pop(0)

    def remove_all(self) -> List[E]:
        removed_elements = []
        while not self.is_empty:
            removed_elements.append(self.remove())
        return removed_elements

#COLA CON LÍMITE
class ColaConLimite(AgregadoLineal[E]):
    def __init__(self, capacidad: int):
        super().__init__()
        self.capacidad = capacidad

    def add(self, e: E) -> None:
        if self.is_full:
            raise OverflowError("La cola está llena.")
        self._elements.append(e)

    @property
    def is_full(self) -> bool:
        return len(self._elements) >= self.capacidad

    @classmethod
    def of(cls, capacidad: int) -> "ColaConLimite":
        return cls(capacidad)


# AGREGADO LINEAL NUEVO
class AgregadoLinealNuevo(ABC, Generic[E]):
    def __init__(self):
        self._elements: List[E] = []

    @property
    def size(self) -> int:
        return len(self._elements)

    @property
    def is_empty(self) -> bool:
        return len(self._elements) == 0

    @property
    def elements(self) -> List[E]:
        return self._elements

    @abstractmethod
    def add(self, e: E) -> None:
        pass

    def add_all(self, ls: List[E]) -> None:
        for element in ls:
            self.add(element)

    def remove(self) -> E:
        assert len(self._elements) > 0, 'El agregado está vacío'
        return self._elements.pop(0)

    def remove_all(self) -> List[E]:
        removed_elements = []
        while not self.is_empty:
            removed_elements.append(self.remove())
        return removed_elements
    
    def contains(self, e: E) -> bool:
        return e in self._elements
    
    def find(self, func: Callable[[E], bool]) -> Optional[E]:
        for element in self._elements:
            if func(element):
                return element
        return None

    def filter(self, func: Callable[[E], bool]) -> List[E]:
        return [element for element in self._elements if func(element)]

#TESTS
def test_cola_con_limite_agregar():
    cola = ColaConLimite.of(3)
    cola.add("Tarea 1")
    cola.add("Tarea 2")
    cola.add("Tarea 3")
    print("Tamaño de la cola:", cola.size)

def test_cola_con_limite_agregar_excepcion():
    cola = ColaConLimite.of(2)
    cola.add("Tarea 1")
    cola.add("Tarea 2")
    try:
        cola.add("Tarea 3")
    except OverflowError as e:
        print(e)

def test_cola_con_limite_eliminar():
    cola = ColaConLimite.of(3)
    cola.add("Tarea 1")
    cola.add("Tarea 2")
    cola.add("Tarea 3")
    print("Elemento removido:", cola.remove())
    print("Tamaño de la cola después de eliminar:", cola.size)

def test_cola_con_limite_remover_cola_vacia():
    cola = ColaConLimite.of(2)
    try:
        cola.remove()
    except AssertionError as e:
        print(e)

if __name__ == "__main__":
    print('Pruebas Cola Con Límite')
    test_cola_con_limite_agregar()
    test_cola_con_limite_agregar_excepcion()
    test_cola_con_limite_eliminar()
    test_cola_con_limite_remover_cola_vacia()

