from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Generic, List, Tuple

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
    

R = TypeVar('R')
#LISTA ORDENADA
class ListaOrdenada(AgregadoLineal[E], Generic[E, R]):
    def __init__(self, order: Callable[[E], R]):
        super().__init__()
        self._order: Callable[[E], R] = order

    @classmethod
    def of(cls, order: Callable[[E], R]) -> ListaOrdenada[E, R]:
        return cls(order)

    def _index_order(self, e: E) -> int:
        for index, current in enumerate(self._elements):
            if self._order(e) < self._order(current):
                return index
        return len(self._elements)

    def add(self, e: E) -> None:
        index = self._index_order(e)
        self._elements.insert(index, e)

    def __repr__(self) -> str:
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"ListaOrdenada({elements_str})"

#LISTA ORDENADA SIN REPETICIÓN
class ListaOrdenadaSinRepeticion(AgregadoLineal[E], Generic[E, R]):
    def __init__(self, order: Callable[[E], R]):
        super().__init__()
        self._order: Callable[[E], R] = order

    @classmethod
    def of(cls, order: Callable[[E], R]) -> ListaOrdenadaSinRepeticion[E, R]:
        return cls(order)

    def _index_order(self, e: E) -> int:
        for index, current in enumerate(self._elements):
            if self._order(e) < self._order(current):
                return index
        return len(self._elements)

    def add(self, e: E) -> None:
        if e not in self._elements:
            index = self._index_order(e)
            self._elements.insert(index, e)

    def __repr__(self) -> str:
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"ListaOrdenadaSinRepeticion({elements_str})"
    
#COLA
class Cola(AgregadoLineal[E]):
    @classmethod
    def of(cls) -> Cola[E]:
        return cls()

    def add(self, e: E) -> None:
        self._elements.append(e)

    def __repr__(self) -> str:
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"Cola({elements_str})"


#COLA DE PRIORIDAD
P = TypeVar('P')

class ColaPrioridad(AgregadoLineal[E]):
    def __init__(self):
        super().__init__()
        self._priorities: List[P] = []

    @classmethod
    def of(cls) -> ColaPrioridad[E, P]:
        return cls()

    def _index_order(self, priority: P) -> int:
        for index, current_priority in enumerate(self._priorities):
            if current_priority > priority:
                return index
        return len(self._priorities)

    def add(self, e: E, priority: P) -> None:
        index = self._index_order(priority)
        self._elements.insert(index, e)
        self._priorities.insert(index, priority)

    def add_all(self, ls: List[Tuple[E, P]]) -> None:
        for e, priority in ls:
            self.add(e, priority)
    def remove(self) -> E:
        assert len(self._elements) > 0, 'El agregado está vacío'
        self._priorities.pop(0)
        return super().remove()

    def remove_all(self) -> List[E]:
        removed_elements = []
        while not self.is_empty:
            removed_elements.append(self.remove())
        return removed_elements

    def decrease_priority(self, e: E, new_priority: P) -> None:
        if e in self._elements:
            index = self._elements.index(e)
            current_priority = self._priorities[index]
            if new_priority < current_priority:
                self._elements.pop(index)
                self._priorities.pop(index)
                self.add(e, new_priority)

    def __repr__(self) -> str:
        elements_str = ", ".join(f"({e}, {p})" for e, p in zip(self._elements, self._priorities))
        return f"ColaPrioridad[{elements_str}]"
    
#PILA
class Pila(AgregadoLineal[E]):
    @classmethod
    def of(cls) -> Pila[E]:
        """Método de factoría que crea una nueva instancia de Pila."""
        return cls()

    def add(self, e: E) -> None:
        """Añade un elemento al inicio de la pila (LIFO)."""
        self._elements.insert(0, e)
        
    def __repr__(self) -> str:
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"Pila({elements_str})"

# Test_Lista_ordenada.py


#TESTS
def test_lista_ordenada():
    print("TEST DE LISTA ORDENADA:")
    print("################################################")
    
    # Crear lista ordenada con el criterio de ordenación lambda x: x
    lista = ListaOrdenada.of(lambda x: x)
    print("Creación de una lista con criterio de orden lambda x: x")
    print("Se añade en este orden: 3, 1, 2")
    lista.add(3)
    lista.add(1)
    lista.add(2)
    print(f"Resultado de la lista: {lista}")
    print("################################################")
    
    # Eliminar un elemento utilizando remove()
    removed = lista.remove()
    print(f"El elemento eliminado al utilizar remove(): {removed}")
    print("################################################")
    
    # Eliminar todos los elementos utilizando remove_all()
    removed_all = lista.remove_all()
    print(f"Elementos eliminados utilizando remove_all: {removed_all}")
    print("################################################")
    
    # Comprobar si se añaden los números en la posición correcta
    print("Comprobando si se añaden los números en la posición correcta...")
    lista.add(0)
    print(f"Lista después de añadirle el 0: {lista}")
    lista.add(10)
    print(f"Lista después de añadirle el 10: {lista}")
    lista.add(7)
    print(f"Lista después de añadirle el 7: {lista}")
    print("################################################")


def test_lista_ordenada_sin_repeticion():
    print("TEST DE LISTA ORDENADA SIN REPETICIÓN:")
    print("################################################")
    
    # Crear lista ordenada sin repetición con el criterio de ordenación lambda x: -x
    lista = ListaOrdenadaSinRepeticion.of(lambda x: -x)
    print("Creación de una lista con criterio de orden lambda x: -x")
    print("Se añade en este orden: 23, 47, 47, 1, 2, -3, 4, 5")
    lista.add(23)
    lista.add(47)
    lista.add(47)
    lista.add(1)
    lista.add(2)
    lista.add(-3)
    lista.add(4)
    lista.add(5)
    print(f"Resultado de la lista ordenada sin repetición: {lista}")
    print("################################################")
    
    # Eliminar un elemento utilizando remove()
    removed = lista.remove()
    print(f"El elemento eliminado al utilizar remove(): {removed}")
    print("################################################")
    
    # Eliminar todos los elementos utilizando remove_all()
    removed_all = lista.remove_all()
    print(f"Elementos eliminados utilizando remove_all: {removed_all}")
    print("################################################")
    
    # Comprobar si se añaden los números en la posición correcta
    print("Comprobando si se añaden los números en la posición correcta...")
    lista.add(0)
    print(f"Lista después de añadirle el 0: {lista}")
    lista.add(7)
    print(f"Lista después de añadirle el 7: {lista}")
    print("################################################")


def test_cola():
    print("TEST DE COLA:")
    print("################################################")
    
    # Crear una cola vacía y añadir elementos
    cola = Cola.of()
    print("Creación de una cola vacía a la que luego se le añaden con un solo método los números: 23, 47, 1, 2, -3, 4, 5")
    cola.add(23)
    cola.add(47)
    cola.add(1)
    cola.add(2)
    cola.add(-3)
    cola.add(4)
    cola.add(5)
    print(f"Resultado de la cola: {cola}")
    print("################################################")
    
    # Eliminar todos los elementos utilizando remove_all()
    removed_all = cola.remove_all()
    print(f"Elementos eliminados utilizando remove_all: {removed_all}")
    print("################################################")


def test_cola_prioridad():
    cola = ColaPrioridad[str, int]()  # Crear una cola de prioridad para cadenas con prioridades enteras

    # Agregar pacientes
    print("Agregar pacientes a la cola de prioridad:")
    cola.add('Paciente A', 3)  # Dolor de cabeza leve
    cola.add('Paciente B', 2)  # Fractura en la pierna
    cola.add('Paciente C', 1)  # Ataque cardíaco
    
    # Verificar el estado de la cola
    print("Verificar estado de la cola después de añadir pacientes:")
    print(f"Estado de la cola: {cola.elements()}")
    assert cola.elements() == ['Paciente C', 'Paciente B', 'Paciente A'], "El orden de la cola es incorrecto."
    
    # Atender a los pacientes y verificar el orden de atención
    atencion = []
    print("Atendiendo a los pacientes según su prioridad...")
    while not cola.is_empty():
        atencion.append(cola.remove())
    print(f"Pacientes atendidos: {atencion}")
    assert atencion == ['Paciente C', 'Paciente B', 'Paciente A'], "El orden de atención no es correcto."
    
    print("Pruebas superadas exitosamente.")

if __name__ == '__main__':
    test_lista_ordenada()
    test_lista_ordenada_sin_repeticion()
    test_cola()
    test_cola_prioridad()
