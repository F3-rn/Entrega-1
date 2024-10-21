#EJERCICIO 6
from _csv import reader

def contador(fichero:str, sep:str,cad:str)-> int:
    palabra:int = 0
    with open(fichero) as f:
        lector= reader(f, delimiter=sep)
        for n in lector:
            for y in n:
                if y == cad:
                    palabra = palabra + 1
    return(palabra)



#EJERCICIO 7
def lineas_con_palabra(fichero:str, palabra:str) -> list[str]:
    lista = []
    with open(fichero) as f:
        for linea in f:
            if palabra in linea:
                    lista.append(linea.strip())
    return(lista)



#EJERCICIO 8
def palabras_fichero(fichero:str) -> list[str]:
    lista = []
    with open(fichero) as f:
        lector= reader(f, delimiter=' ')
        for n in lector:
            for y in n:
                if (y not in lista) and (y != ''):
                    lista.append(y)
    return(lista)



#EJERCICIO 9
def longitud_promedio_lineas(file_path: str, sep:str) -> float:
    lista = []
    i:int = 0
    with open(file_path) as f:
        lector= reader((linea.strip() for linea in f), delimiter=sep)
        for n in lector:
            i = 0
            for y in n:
                i= i + 1
            lista.append(i)
    final= sum(lista)/len(lista)
    return(final)


if __name__ == '__main__':
    print(contador('../../resources/lin_quijote.txt',' ','Quijote')) #La función es sensible a mayúsculas y minúsculas
    print(lineas_con_palabra('../../resources/lin_quijote.txt', 'QUIJOTE')) #La función es sensible a mayúsculas y minúsculas
    print(palabras_fichero('../../resources/archivo_palabras.txt'))
    print(longitud_promedio_lineas('../../resources/palabras_random.csv', ','))
