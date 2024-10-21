#EJERCICIO 1
from math import factorial

def productorio(n:int,k:int)->int:
    i:int=0
    p:int=1
    if (n <= k):
        raise Exception("El primer número tiene que ser mayor que el segundo")
    else:
        while k>=i:
            p = (n-i+1)*p
            i = i+1
    return(p)



#EJERCICIO 2
def secuencia(a:int, r:int, k:int):
    i:int=1
    producto = list()
    m:int=1
    while i<= k:
        a= a*r**(i-1)
        i = i+1
        producto.append(a)
    for n in producto:
        m= m*n
    return(m)


#EJERCICIO 3
def combinatorio(n:int,k:int):
    if (n < k):
        raise Exception("El primer número tiene que ser mayor o igual que el segundo")
    else:
        return(factorial(n)/(factorial(k)*factorial(n - k)))
        

#EJERCICIO 4
def numeroespecial(n:int,k:int):
    i=0
    parte2=0
    if (n < k):
        raise Exception("El primer número tiene que ser mayor o igual que el segundo")
    else:
        parte1 = 1/factorial(k)
        while i<k:
            parte2 = parte2 + combinatorio(k + 1, i + 1)*(-1)**i*(k - i)**n
            i = i + 1
        return(parte1*parte2)



#EJERCICIO 5
from typing import Callable
def newton(f:Callable[[float],float],d:Callable[[float],float],a:float,e:float)->float:
    while abs(f(a))>e:
        a = a - f(a)/d(a)
    return(a)



if __name__ == '__main__':
    print(productorio(4, 2))
    print(secuencia(3, 5, 2))
    print(combinatorio(4, 2))
    print(numeroespecial(4, 2))
    print(newton(lambda x: 2*x**2, lambda x: 4*x,3,0.001))