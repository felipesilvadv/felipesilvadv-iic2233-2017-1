# Todo lo que devuelve booleano
from Consultas_numericas import interpretar_comando
if __name__ == "__main__":
    import Exception as error
from random import uniform, randint
import Data as d

def interpretar_simbolo(simbolo, funcion):
    dic = {"<": lambda x, b: x < b,
           ">": lambda x, b: x > b,
           "==": lambda x, b: x == b,
           ">=": lambda x, b: x >= b,
           "<=": lambda x, b: x <= b,
           "!=": lambda x, b: x != b}
    if simbolo not in dic.keys():
        raise error.ErrorDeTipo(funcion)
    return dic[simbolo]


def comparar_columna(columna_1, simbolo, comando, columna_2, *args):
    if len(args):
        raise error.ArgumentoInvalido("comparar columna")
    # Aplica comando numerico a cada columna y luego usa simbolo sobre lo
    # entregado de cada uno
    if not hasattr(columna_1, "__iter__"):
        raise err.ErrorDeTipo("comparar columna", "Primera columna")
    if isinstance(columna_1, str):
        if columna_1 not in d.data.keys():
            raise err.ReferenciaInvalida("compara columna", "Primera columna")
        else:
            columna_1 = d.data[columna_1]

    if not hasattr(columna_2, "__iter__"):
        raise err.ErrorDeTipo("comparar columna", "Segunda columna")
    if isinstance(columna_2, str):
        if columna_2 not in d.data.keys():
            raise err.ReferenciaInvalida("comparar columna", "Segunda columna")
        else:
            columna_2 = d.data[columna_2]
    c1 = float(interpretar_comando(comando, "comparar columna")(columna_1))
    c2 = float(interpretar_comando(comando, "comparar columna")(columna_2))
    return interpretar_simbolo(simbolo, "comparar columna")(c1, c2)



def comparar(numero1, simbolo, numero2, *args):
    if len(args):
        raise error.ArgumentoInvalido("comparar")
    n1 = float(numero1)
    n2 = float(numero2)
    return interpretar_simbolo(simbolo, "comparar")(n1, n2)




if __name__ == "__main__":
    try:
        a = [uniform(0,1) for i in range(100)]
        b = [uniform(0,1) for i in range(100)]
        print(comparar_columna(a, ">=<", "VAR", b))
        #print(interpretar_simbolo("<")(a, 1))
    except error.MiException as err:
        print(err)



