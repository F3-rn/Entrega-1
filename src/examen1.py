from math import factorial
from collections import Counter
import re

#EJERCICIO A
def P2(n:int,k:int,i:int=1)->int:
    p:int=1
    if (n < k):
        raise Exception("El primer número tiene que ser mayor o igual que el segundo")
    elif (i >= k + 1):
        raise Exception("El tercer número tiene que ser menor que el segundo más una unidad")
    elif (i < 0) or (n < 0) or (k < 0):
        raise Exception("Todos los números tienen que ser positivos")
    else:
        while (k - 2)>=i:
            p = (n-i+1)*p
            i = i+1
    return(p)

#EJERCICIO B
def C2(n:int,k:int):
    if (n < k):
        raise Exception("El primer número tiene que ser mayor o igual que el segundo")
    elif (n < 0) or (k < 0):
        raise Exception("Todos los números tienen que ser positivos")
    else:
        k = k+1
        return(factorial(n)/(factorial(k)*factorial(n - k)))
    
#EJERCICIO C
def S2(n:int,k:int):
    i=0
    parte2=0
    if (n < k):
        raise Exception("El primer número tiene que ser mayor o igual que el segundo")
    elif (n < 0) or (k < 0):
        raise Exception("Todos los números tienen que ser positivos")
    else:
        parte1 = factorial(k)/(n*factorial(k+2))
        while i<=k:
            parte2 = parte2 + (-1)**i*(factorial(k)/(factorial(i)*factorial(k - i)))*(k - i)**(n+1)
            i = i + 1
        return(parte1*parte2)

#EJERCICIO D

def palabrasMasComunes(fichero: str, n: int = 5) -> list[tuple[str, int]]:
    if n <= 1:
        raise ValueError("El número introducido debe ser mayor que 1")
    with open(fichero) as f:
        texto = f.read()
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', ' ', texto)
    palabras = texto.split()
    npalabras = Counter(palabras)
    palabrascomunes = npalabras.most_common(n)
    return palabrascomunes

def test_P2():
    print("Pruebas de P2")
    try:
        print(P2(5, 3))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(P2(3, 5))  # n < k
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(P2(5, 3, 4))  # i >= k + 1
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(P2(-2, -5,-7))  # Valores negativos
    except Exception as e:
        print(f"Error: {e}")
    print("    ")

def test_C2():
    print("Pruebas de C2")
    try:
        print(C2(5, 3))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(C2(3, 5))  # n < k
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(C2(-3, -5))  # Valores negativos
    except Exception as e:
        print(f"Error: {e}")
    print("    ")

def test_S2():
    print("Pruebas de S2")
    try:
        print(S2(5, 3))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(S2(3, 5))  # n < k
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(S2(5, -3))  # Valores negativos
    except Exception as e:
        print(f"Error: {e}")
    print("    ")

def test_palabrasMasComunes():
    print("Pruebas de palabrasMasComunes")
    try:
        print(palabrasMasComunes('../resources/archivo_palabras.txt', 3))
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(palabrasMasComunes('archivo_palabras.txt', 1))  # n <= 1
    except Exception as e:
        print(f"Error: {e}")
    print("    ")

if __name__ == "__main__":
    test_P2()
    test_C2()
    test_S2()
    test_palabrasMasComunes()