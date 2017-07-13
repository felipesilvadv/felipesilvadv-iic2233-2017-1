# from math import sqrt
from functools import reduce
import random as r
from datetime import datetime
import Exception as error
import Data as d
if __name__ == "__main__":
    import comandos_datos as cd
# Todo los datos son de la forma [comando, datos], donde datos es un conjunto
# de datos

def interpretar_comando(comando, funcion):
    dic = {"PROM": prom,
           "VAR": var,
           "DESV": desv,
           "MEDIAN": median,
           "LEN": len}
    if comando not in dic.keys():
        raise error.ErrorDeTipo(funcion)
    return dic[comando]

def prom(x, *args):
    if len(args):
        raise error.ArgumentoInvalido("PROM")
    elif not hasattr(x, "__iter__"):
        raise error.ErrorDeTipo("PROM")
    elif isinstance(x, str):
        if x not in d.data.keys():
            raise error.ReferenciaInvalida("PROM")
        else:
            x = d.data[x]
    if len(x) == 0:
        raise error.ErrorMatematico("PROM")
    return sum(x)/len(x)


def var(x, *args):
    if len(args):
        raise error.ArgumentoInvalido("VAR")
    if not hasattr(x, "__iter__"):
        raise error.ErrorDeTipo("VAR")
    if isinstance(x, str):
        if x not in d.data.keys():
            raise error.ReferenciaInvalida("VAR")
        else:
            x = d.data[x]
    if len(x) == 1:
        raise error.ErrorMatematico("VAR")
    mean = prom(x)
    return reduce(lambda z, y: z + y, map(lambda y: (y-mean)**2, x))/(len(x)-1)


def desv(x, *args):
    if len(args):
        raise error.ArgumentoInvalido("DESV")
    if not hasattr(x, "__iter__"):
        raise error.ErrorDeTipo("DESV")
    if isinstance(x, str):
        if x not in d.data.keys():
            raise error.ReferenciaInvalida("DESV")
        else:
            x = d.data[x]
    if len(x) == 1:
        raise error.ErrorMatematico("DESV")
    mean = prom(x)
    return (reduce(lambda z, y: z + y, map(lambda y: (y - mean) ** 2, x)) /
                (len(x) - 1))**0.5

def median(x, *args):
    if len(args):
        raise error.ArgumentoInvalido("MEDIAN")
    if not hasattr(x, "__iter__"):
        raise error.ErrorDeTipo("MEDIAN")
    if isinstance(x, str):
        if x not in d.data.keys():
            raise error.ReferenciaInvalida("MEDIAN")
        else:
            x = d.data[x]
    n = len(x)
    if n == 0:
        raise error.ErrorDeTipo("MEDIAN")
    elif n % 2 == 1:
        return x[n//2]
    else:
        return (x[n//2 - 1] + x[n//2])/2


def probar(x):
    print("Probando")
    inicio = datetime.now()
    print(prom(x))
    print("promedio: ", datetime.now() - inicio)
    a = datetime.now()
    print(median(x))
    print("mediana: ", datetime.now() - a)
    a = datetime.now()
    print(var(x))
    print("varianza: ", datetime.now() - a)
    a = datetime.now()
    print(desv(x))
    print("sd: ", datetime.now() - a)
    a = datetime.now()
    print(len(x))
    print("len: ", datetime.now() - a)
    print("total: ", datetime.now() - inicio)

if __name__ == "__main__":
    X = [i for i in range(11)]
    Y = [r.randint(0, 200) for i in range(500000)]
    #print(interpretar_comando("MAX")([1,2,3,5]))
    probar(X)
    #probar(Y)


