import numpy as np
from matplotlib import pyplot as plt
from math import pi, e
from functools import reduce


def factorial(x):
    if x == 0:
        return 1
    elif x == 1:
        return 1
    return reduce(lambda w, y: w * y, range(1, x + 1))


def crear_funcion(nombre_modelo, *args, **kwargs):
    def normal(x=0.0, u=0.0, s=1.0):
        while True:
            x = yield (1 / (2 * pi * s) ** 0.5) * (
            e ** ((-1 / 2) * (x - u / s) ** 2))

    def exponencial(x=0.0, v=0.5):
        while True:
            x = yield v * e**(-v*x)

    def gamma(x=0.0, v=1, k=1):
        while True:
            x = yield (v**k/factorial(k-1))*x**(k-1)*e**(-v*x)
    dic = {"normal":normal,
           "exponencial":exponencial,
           "gamma":gamma}
    func = dic[nombre_modelo](x=0.0, *args, **kwargs)
    next(func)
    return func



if __name__ == "__main__":
    a = crear_funcion("normal", u=3.0, s=1.0)
    print(a.send(1))
