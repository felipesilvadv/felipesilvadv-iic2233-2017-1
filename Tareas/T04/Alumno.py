from matplotlib import pyplot as plt
import numpy as np
from functools import reduce
class Alumno:
    pass

def factorial(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return reduce(lambda w, z: w * z, range(1, n + 1))

if __name__ == "__main__":
    print(factorial(4))
    x = np.arange(0, 5, 1)
    y = np.array(list(map(lambda a: 2**(factorial(a)), x)))
    plt.plot(x, y)
    plt.show()
