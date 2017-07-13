def funcion(x):
    try:
        if isinstance(x, list):
            for elemento in x:
                funcion(elemento)
        else:
            return print(int(x))
    except ValueError:
        print("pase por ahi")
        exit()


funcion([1, 2, 3, 4, "hola", 6, 0, 10, 8])
print("hola")