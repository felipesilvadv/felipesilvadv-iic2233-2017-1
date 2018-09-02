# Estructuras de Datos a diseñar/usar
from random import shuffle


class Nodo:

    def __init__(self, valor=None):
        self.valor = valor


class NodoLista(Nodo):

    def __init__(self, siguiente=None, **kwargs):
        super().__init__(**kwargs)
        self.siguiente = siguiente

    def __repr__(self):
        return str(self.valor)


class ListaLigada:

    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        self.largo = 0
        for arg in args:
            self.append(arg)

    def __repr__(self):
        nodo = self.cabeza
        s = "["
        if nodo:
            s += str(nodo.valor) + ", "
        else:
            return "[]"
        while nodo.siguiente:
            nodo = nodo.siguiente
            s += str(nodo.valor) + ", "
        return s.strip(", ") + "]"

    def __iter__(self):
        for i in range(len(self)):
            try:
                yield self[i]
            except IndexError:
                if len(self) < i:
                    break

    def __next__(self):
        return next(self)

    def __getitem__(self, index):
        if isinstance(index, slice):
            lista = ListaLigada()
            if not index.step:
                step = 1
            else:
                step = index.step
            if index.stop:
                stop = index.stop
            else:
                stop = len(self)
            if index.start:
                start = index.start
            else:
                start = 0
            for i in range(start, stop, step):
                lista.append(self[i])
            return lista
        else:
            nodo = self.cabeza
            for i in range(index):
                if nodo:
                    nodo = nodo.siguiente
                else:
                    raise IndexError("La lista no tiene un indice con ese valor")
            if not nodo:
                raise IndexError("La lista no tiene un indice con ese valor")
            else:
                return nodo.valor

    def __setitem__(self, key, value):
        nodo = self.cabeza
        for i in range(key):
            if nodo:
                nodo = nodo.siguiente
            else:
                raise IndexError("La lista no tiene un indice con ese valor")
        if not nodo:
            raise IndexError("La lista no tiene un indice con ese valor")
        else:
            nodo.valor = value

    def __in__(self, valor):
        for elemento in self:
            if elemento == valor:
                return True
        return False

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = NodoLista(valor=valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = NodoLista(valor=valor)
            self.cola = self.cola.siguiente
        self.largo += 1

    def clear(self):
        self.cabeza = None
        self.cola = None
        self.largo = 0

    def count(self, valor):
        contador = 0
        for elemento in self:
            if elemento == valor:
                contador += 1
        return contador

    def __add__(self, other):
        suma = ListaLigada()
        for elemento in self:
            suma.append(elemento)
        for element in other:
            suma.append(element)
        return suma

    def __len__(self):
        return self.largo

    def remove(self, valor):
        if valor not in self:
            raise ValueError("{} no esta en la lista".format(valor))
        if self.cabeza.valor == valor:
            self.cabeza = self.cabeza.siguiente
            self.largo -= 1
            return
        nodo = self.cabeza
        for i in range(len(self)):
            if self[i] == valor:
                break

        for j in range(i - 1):
            if nodo:
                nodo = nodo.siguiente
        nodo.siguiente = nodo.siguiente.siguiente
        self.largo -= 1
        if self.cola.valor != self[len(self)-1]:
            self.cola.valor = self[len(self)-1]

    def pop(self, index=-1):
        nodo = self.cabeza
        if index == -1:
            valor = self.cola.valor
            for i in range(len(self) - 2):
                if nodo:
                    nodo = nodo.siguiente
            nodo.siguiente = None
            self.cola = nodo
            self.largo -= 1
            return valor
        valor = self[index]
        if index == 0:
            self.cabeza = self.cabeza.siguiente
            self.largo -= 1
            return valor
        nodo = self.cabeza
        for i in range(index - 1):
            if nodo:
                nodo = nodo.siguiente
        nodo.siguiente = nodo.siguiente.siguiente
        self.largo -= 1
        return valor

    def msort(self):  # La saque de stackoverflow para tener un sort rápido y me gusta mergesort :)
        # (http://stackoverflow.com/questions/18761766/mergesort-python)
        result = ListaLigada()
        if len(self) < 2:
            return self
        mid = int(len(self) / 2)
        y = self[:mid].msort()
        z = self[mid:].msort()
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        return result

if __name__ == "__main__":
    a = ListaLigada(2, 3, 4, 5, 6)
    a.append(1)
    b = [1, 2, 3, 1, 4, 12, 100]
    b = ListaLigada(*b)
    print(b[0:3])
    print("largo de b : {}".format(len(b)))
    shuffle(b)
    print("largo de b : {}".format(len(b)))
    print(b.cola)
    print(b)
    for element in b:
        print(element)
    a = ListaLigada(*map(lambda x: str(x), a))
    print(",".join(a))
    c = ListaLigada(*(i for i in range(10)))
    c = c.msort()
    print(c)
    print(type((i for i in range(10))))
