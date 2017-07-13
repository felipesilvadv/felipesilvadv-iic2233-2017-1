# PRIMERA PARTE: Estructura basica
class Nodo:

    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None


class ListaLigada:

    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for arg in args:
            self.append(arg)

    def __getitem__(self, index):
        nodo = self.cabeza
        for i in range(index):
            if nodo:
                nodo = nodo.siguiente
            else:
                raise IndexError
        if not nodo:
            raise IndexError
        else:
            return nodo.valor

    def __in__(self, valor):
        for elemento in self:
            if elemento == valor:
                return True
        return False

    def __repr__(self):
        s = "["
        if not self.cabeza:
            return "[]"
        else:
            for elemento in self:
                s += str(elemento)+","
            s = s.strip(",")+"]"
            return s

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def __len__(self):
        contador = 0
        for elemento in self:
            contador += 1
        return contador


# SEGUNDA PARTE: Clase Isla
class Isla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conecciones = ListaLigada()
        self.contagiado = False

    def __repr__(self):
        l = "Isla: {} ".format(self.nombre)
        return l


# TERCERA PARTE: Clase Archipielago
class Archipielago:
    def __init__(self, archivo):
        self.islas = ListaLigada()
        self.infectados = ListaLigada()
        self.construir(archivo)

    def __repr__(self):
        l = ""
        for isla in self.islas:
            l += isla.__repr__()
            if len(isla.conecciones) > 0:
                l += "-> (" + ",".join([c.__repr__() for c in isla.conecciones]) + ")"
            l += "\n"
        return l

    def agregar_isla(self, nombre):
        nueva_isla = Isla(nombre)
        self.islas.append(nueva_isla)

    def conectadas(self, nombre_origen, nombre_destino):
        for isla in self.islas:
            if isla.nombre == nombre_destino:
                isla2 = isla
            elif isla.nombre == nombre_origen:
                isla1 = isla
        for elemento in isla1.conecciones:
            if elemento == isla2.nombre:
                return True
        return False

    def agregar_conexion(self, nombre_origen, nombre_destino):
        for isla in self.islas:
            if isla.nombre == nombre_origen:
                isla.conecciones.append(nombre_destino)
            elif isla.nombre == nombre_destino:
                isla.conecciones.append(nombre_origen)

    def construir(self, archivo):
        with open(archivo, "r", encoding="utf8") as f:
            islas = f.readlines()
            for i in range(len(islas)):
                islas[i] = islas[i].strip()
                islas[i] = islas[i].split(",")
            lista_nombres = ListaLigada()
            for relacion in islas:
                algo = Isla(relacion[0])
                if algo.nombre not in lista_nombres:
                    algo.conecciones.append(relacion[1])
                    lista_nombres.append(algo.nombre)
                    self.islas.append(algo)
                else:
                    for isla in self.islas:
                        if isla.nombre == relacion[0]:
                            isla.conecciones.append(relacion[1])

    def propagacion(self, nombre_origen):
        if len(self.infectados) == len(self.islas):
            return self.infectados
        for isla in self.islas:
            if isla.nombre == nombre_origen:
                isla.contagio = True
                self.infectados.append(isla)
                isla_infectada = isla.conecciones
        for nombre in isla_infectada:
            self.propagacion(nombre)



if __name__ == '__main__':
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")  # Instancia y construye
    print(arch) # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    print(arch.propagacion("Pasesterot"))
    print(arch.propagacion("Cartonat"))
    print(arch.propagacion("Womeston"))
else:
    archi = Archipielago("mapa.txt")
    print(archi)
