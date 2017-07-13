from Comandos_booleanos import interpretar_simbolo
import Exception as err
from datetime import datetime
from functools import reduce
from math import e, pi
#import Consultas_numericas as cn
from matplotlib import pyplot as plt
import Data as d
import os


def factorial(x):
    if x == 0:
        return 1
    elif x == 1:
        return 1
    return reduce(lambda x, y: x * y, range(1, x + 1))


def asignar(variable, comando_o_dato, *args):
    if len(args) != 0:
        raise err.ArgumentoInvalido
    variables_RQL= ["asignar",
                 "comparar",
                 "PROM",
                 "DESV",
                 "VAR",
                 "do_if",
                 "extraer_columna",
                 "graficar",
                 "MEDIAN",
                 "comparar_columna",
                 "crear_funcion",
                 "filtrar",
                 "operar",
                 "evaluar",
                 "<", ">", ">=", "<=", "==", "!=", ">=<", "+", "-", "*", "/"]
    if variable in variables_RQL or not isinstance(variable,str):
        raise err.ErrorDeTipo("asignar")
    else:
        d.data[variable] = comando_o_dato


def crear_funcion(nombre_modelo, *args, **kwargs):
    def normal(u=0.0, s=1.0, *args, **kwargs):
        if len(args) or len(kwargs):
            raise err.ArgumentoInvalido("crear funcion")
        x = 0.0
        while True:
            x = yield (1 / (2 * pi * s) ** 0.5) * (
            e ** ((-1 / 2) * (x - u / s) ** 2))

    def exponencial(v=0.5, *args, **kwargs):
        if len(args) or len(kwargs):
            raise err.ArgumentoInvalido("crear funcion")
        x = 0.0
        while True:
            x = yield v * e**(-v*x)

    def gamma(v=1, k=1, *args, **kwargs):
        if len(args) or len(kwargs):
            raise err.ArgumentoInvalido("crear funcion")
        x = 0.0
        while True:
            x = yield (v**k/factorial(k-1))*x**(k-1)*e**(-v*x)
    dic = {"normal":normal,
           "exponencial":exponencial,
           "gamma":gamma}
    func = dic[nombre_modelo](*args, **kwargs)
    next(func)
    return func


def graficar(columna, opcion, *args):
    if len(args):
        raise err.ArgumentoInvalido("graficar")

    if not hasattr(columna, "__iter__"):
        raise err.ErrorDeTipo("graficar")
    if isinstance(columna, str):
        if columna not in d.data.keys():
            raise err.ReferenciaInvalida("graficar")
        else:
            columna = d.data[columna]
    if "rango" in opcion:
        y = list(map(lambda x: float(x), opcion[opcion.find(":")+1:].split(",")))
        inicio, final, intervalo = y[0], y[1], y[2]
        largo = int((final - inicio) / intervalo)
        y = [inicio + i * intervalo for i in range(largo)] + [final]
        plt.title(opcion)
    elif hasattr(opcion, "__iter__") and not isinstance(opcion, str):
        y = opcion

    elif opcion == "numerico":
        variable = list(i for i in range(len(columna)))
        plt.plot(variable, columna)
        plt.title("numerico")
        plt.ylabel("columna")
        plt.show()
        return
    elif opcion == "normalizado":
        n = sum(columna)
        y = list(map(lambda x: x/n, (i for i in range(len(columna)))))
        plt.plot(y, columna)
        plt.title("normalizado")
        plt.ylabel("columna")
        plt.show()
        return
    else:
        raise err.ErrorDeTipo("graficar", "Opcion invalida")
    if len(y) != len(columna):
        raise err.ImposibleProcesar("graficar", "largos distintos")
    else:
        plt.plot(y, columna)
        plt.ylabel("columna")
        plt.show()


def interpretar_operacion(simbolo):
    def division(x, y):
        if int(y) == 0:
            raise err.ErrorMatematico("Intepretar operación")
        else:
            return x / y
    def aprox(x, y):
        if not (isinstance(y, int) or y < 0):
            raise err.ErrorDeTipo("Interpretar operacion", "Para aproximar "
                                                           "debes entregar un "
                                                           "número mayor o "
                                                           "igual a 0")
        return  round(x, y)
    dic = {"+": lambda x, y: x + y,
           "-": lambda x, y: x - y,
           "*": lambda x, y: x * y,
           "/": division,
           ">=<": aprox}
    if simbolo not in dic.keys():
        raise err.ErrorDeTipo("Interpretar operación")
    return dic[simbolo]


def extraer_columna(nombre_archivo, columna, header=False, *args):
    # Todo es str nombre_archivo es de tipo csv
    if len(args):
        raise err.ArgumentoInvalido("extraer columna")
    if not os.path.exists(nombre_archivo + ".csv"):
        raise err.ImposibleProcesar("extraer columna", "No existe el archivo")
    with open(nombre_archivo +".csv", "r") as f:
        headers = f.readline().strip().split(";")
        headers1 = [headers[i][0:headers[i].find(":")] for i in
                    range(len(headers))]
        if columna not in headers and columna not in headers1:
            raise err.ImposibleProcesar("Extraer columna", "El archivo no "
                                                           "tiene esa columna")
        lugar = int(*[i for i in range(len(headers)) if columna in headers[i]])
        archivo = list(map(lambda s: float(s.strip().split(";")[lugar]), f))
        if header:
            archivo = [headers1[lugar]] + archivo
    return archivo

def filtrar(columna, simbolo, valor, *args):
    if len(args):
        raise err.ArgumentoInvalido("filtrar")
    if not hasattr(columna, "__iter__"):
        raise err.ErrorDeTipo("filtrar")
    if isinstance(columna, str):
        if columna not in d.data.keys():
            raise err.ReferenciaInvalida("filtrar")
        else:
            columna = d.data[columna]
    return list(filter(lambda x: interpretar_simbolo(simbolo, "filtrar")(x, valor)
                       , columna))


def operar(columna, simbolo, valor, *args):
    if len(args):
        raise err.ArgumentoInvalido("operar")
    if not hasattr(columna, "__iter__"):
        raise err.ErrorDeTipo("operar")
    if isinstance(columna, str):
        if columna not in d.data.keys():
            raise err.ReferenciaInvalida("operar")
        else:
            columna = d.data[columna]
    return list(map(lambda x: interpretar_operacion(simbolo)(x, valor)
                    , columna))


def evaluar(funcion, inicio, final, intervalo, *args):
    if len(args):
        raise err.ArgumentoInvalido("evaluar")
    if not isinstance(funcion, type((i for i in range(10)))):
        raise err.ErrorDeTipo("evaluar")
    if isinstance(funcion, str):
        if funcion not in d.data.keys():
            raise err.ReferenciaInvalida("evaluar")
        else:
            funcion = d.data[funcion]
    # Retorna los resultados de aplicar la funcion a cada parte
    largo = int((final - inicio)/intervalo)
    lista = [inicio + i*intervalo for i in range(largo)] + [final]
    return [funcion.send(i) for i in lista]




if __name__ == "__main__":
    asignar("x", 1)
    print(d.data)
    a = crear_funcion("normal", u=3.0, s=1.0)
    print(type(a), type(range))
    print(isinstance(a, type((i for i in range(10)))))
    #print(evaluar(a, 0, 10, 0.3))
    inicio = datetime.now()
    a = extraer_columna("registros", "tiempo_sano", header=False)
    print(datetime.now()-inicio)
    #print(a)
    try:
        print(interpretar_operacion("+")(9, 7))
        print(interpretar_operacion("-")(9, 7))
        print(interpretar_operacion("*")(9, 7))
        print(interpretar_operacion("/")(9, 7))
        print(interpretar_operacion("/")(9, 7))
        print(interpretar_operacion(">=<")(9.1241342525235325242,0))
    except err.MiException as error:
        print(error)
