import threading as th
from random import randint, expovariate, choice
import time


class Laberinto:
    with open("registros.txt", "w"):
        pass

    def __init__(self):
        self.start = None
        self.end = None
        self.nodos = {}
        self.salvados = []

    def add_node(self, n, start=False, end=False):
        if n not in self.nodos:
            new_node = Nodo(n)
            self.nodos[n] = new_node
            if start:
                self.start = new_node
                self.start.start = True
            if end:
                self.end = new_node
                self.end.end = True

    def add_connection(self, x, y):
        for i in self.nodos:
            if i == x:
                if y not in self.nodos[i].siguientes:
                    self.nodos[i].agregar_conexion(y)

    def agregar_persona(self, persona):
        self.start.entrar(persona)




class Nodo:
    def __init__(self, valor, start=False, end=False):
        self.valor = valor
        self.siguientes = []
        self.persona = None
        self.lock_pieza = th.Lock()
        self.start = start
        self.end = end

    def agregar_conexion(self, nodo):
        self.siguientes.append(nodo)

    def entrar(self, persona):
        #if self.end or self.start:
            #if isinstance(self.persona, list):
           #     self.persona.append(persona)
          #  else:
         #       self.persona = [persona]
        #else:
        with self.lock_pieza:
            self.persona = persona
            persona.pieza_actual = self
            time.sleep(randint(1, 3))


def set_id():
    contador = 0
    while True:
        yield contador
        contador += 1
a = set_id()


class Persona(th.Thread):

    def __init__(self, grafo, start=1, hp=None):
        super().__init__()
        if not hp:
            self.hp = randint(80, 120)
        else:
            self.hp = hp
        self.id = next(a)
        self.resistencia = randint(1, 3)
        self.pieza_actual = start
        self.grafo = grafo
        self.daemon = True

    @property
    def muerto(self):
        if self.hp <= 0:
            self.hp = 0
            return True
        else:
            return False

    @property
    def vivo(self):
        if self.hp > 0:
            return True
        else:
            return False

    def sufrir(self):
        self.hp = self.hp - (6 - self.resistencia)
        print("Persona n° {} perdio vida".format(self.id))

    def run(self):
        while self.vivo:
            if len(self.grafo.salvados) >= 3:
                exit()
            time.sleep(1)
            self.sufrir()
            #print(self.grafo.end.valor)
            if self.pieza_actual is self.grafo.end:
                print("LLEGO AL ULTIMO !!! -------------")
                if len(self.grafo.salvados) <= 3:
                    self.grafo.salvados.append(self)
                    self.pieza_actual = None
                    print("Persona n° {} SE SALVO".format(self.id))
                    return
                else:
                    exit()

            elif self.pieza_actual is self.grafo.start:
                print("Estaba en el primero")
                valor = choice(self.grafo.start.siguientes)
                self.grafo.nodos[valor].entrar(self)
                print("Persona n° {0} cambio de pieza".format(self.id))
            else:
                for nodo in self.grafo.nodos.values():
                    if nodo is self.pieza_actual:
                        if nodo.siguientes:
                            valor = choice(nodo.siguientes)
                            self.grafo.nodos[valor].entrar(self)
                            print("Persona n° {0} cambio de pieza de nuevo".format(self.id))

        print("---------{}----------".format(self.pieza_actual.valor))
        print("Murio persona n° {}".format(self.id))


class CreadorPersonas(th.Thread):
    def __init__(self, laberinto):
        super().__init__()
        self.daemon = False
        self.lab = laberinto

    def run(self):
        while len(self.lab.salvados) < 3:
            time.sleep(expovariate(0.2))
            person = Persona(self.lab, start=self.lab.start)
            print("La persona n° {} entro al laberinto".format(person.id))
            self.lab.agregar_persona(person)
            person.start()


class Barrendero(th.Thread):
    def __init__(self, laberinto):
        super().__init__()
        self.lab = laberinto
        self.daemon = True

    def run(self):
        while True:
            for nodo in self.lab.nodos.values():
                try:
                    if nodo.persona.muerto:
                        print("Saco un muerto")
                        nodo.persona = None
                except AttributeError:
                    pass


if __name__ == "__main__":
    laberinto = Laberinto()
    with open("laberinto.txt", "r") as lab:
        laberinto.add_node(int(lab.readline()), start=True)
        laberinto.add_node(int(lab.readline()), end=True)
        for line in lab:
            laberinto.add_node(int(line.split(",")[0]))
            laberinto.add_connection(int(line.split(",")[0]), int(line.split(",")[1]))
    barrendero = Barrendero(laberinto)
    Dios = CreadorPersonas(laberinto)
    Dios.start()
    barrendero.start()



